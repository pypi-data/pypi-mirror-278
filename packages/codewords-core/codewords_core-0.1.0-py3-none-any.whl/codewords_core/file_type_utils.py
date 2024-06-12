"""A place for all things file-type related."""
import asyncio
import os
from copy import deepcopy
from typing import Any, Dict, List
from urllib.parse import urlparse

import aiohttp
from .io_metadata import paths_to_filenames, set_at_path, InputOutputMetadata, get_with_path


async def upload_file(upload_url: str, file_path: str):
    filename = os.path.basename(file_path)
    
    async with aiohttp.ClientSession() as session:
        with open(file_path, 'rb') as file:
            # Create the payload with the file data
            data = file.read()
            # Define headers including Content-Disposition
            headers = {
                'Content-Disposition': f'attachment; filename="{filename}"'
            }
            # Execute a PUT request to upload the file with headers
            async with session.put(upload_url, data=data, headers=headers) as response:
                # Check if the upload was successful
                response.raise_for_status()


async def download_file(url, destination_folder):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()  # This will raise an exception for HTTP errors

            # Extract filename from Content-Disposition header if present
            content_disposition = response.headers.get('Content-Disposition')
            if content_disposition:
                filename = get_filename_from_content_disposition(content_disposition)
            else:
                parsed_url = urlparse(url)
                filename = parsed_url.path.split('/')[-1] if parsed_url.path else 'downloaded_file'

            # Check if file already exists and rename if necessary
            original_filename = filename
            base, extension = os.path.splitext(original_filename)
            i = 1
            full_path = os.path.join(destination_folder, filename)
            while os.path.exists(full_path):
                filename = f"{base} ({i}){extension}"
                full_path = os.path.join(destination_folder, filename)
                i += 1

            # Ensure the directory exists
            os.makedirs(destination_folder, exist_ok=True)
            with open(full_path, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)

    # Return the relative path to the downloaded file from the working directory
    relative_path = os.path.relpath(full_path, destination_folder)
    return relative_path


def get_filename_from_content_disposition(content_disposition: str) -> str:
    """
    Extract filename from Content-Disposition header.
    """
    import re
    filename_match = re.search(r'filename="(.+?)"', content_disposition)
    if filename_match:
        return filename_match.group(1)

    raise ValueError(f"Could not extract filename from Content-Disposition header: {content_disposition}")

async def _default_get_urls_fn(files_to_upload: List[str]):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=os.environ['CWR_HTTPS_URL'],
            json={"action": "get_upload_download_files_urls", "filenames": list(files_to_upload)},
            # add the api key to the headers
        ) as resp:
            resp.raise_for_status()
            urls = await resp.json()
            return urls


async def upload_files_and_update_variables(
    variables: Dict[str, Any], 
    variables_metadata: List[InputOutputMetadata],
    working_directory: str,
    get_urls_fn=_default_get_urls_fn,
):
    variable_types = {i.name: i for i in variables_metadata}

    # get the mapping from DictPaths to filenames to upload
    variable_file_mapping = {
        variable_name: paths_to_filenames(
            variable_types[variable_name].jsonschema,
            variables[variable_name]
        )
        for variable_name in variable_types.keys()
    }

    files_to_upload = list(set(
        path
        for path_to_filename in variable_file_mapping.values()
        for path in path_to_filename.values()
    ))

    def _trim_working_directory(path):
        trimmed = [
            path[len(working_directory):].lstrip('/') 
            if path.startswith(working_directory) else path
        ]
        # remove any leading ./ from the path
        return [x[2:] if x.startswith('./') else x for x in trimmed]

    # if the path starts with the working directory or a ./, trim it
    files_to_upload = [_trim_working_directory(path) for path in files_to_upload]

    if len(files_to_upload) > 0:
        urls = await get_urls_fn(files_to_upload)

        import json
        print('🔗', json.dumps(urls))

        # upload each file in parallel
        tasks = []
        for filename, url in urls.items():
            file_path = os.path.join(working_directory, filename)
            tasks.append(upload_file(url['upload_url'], file_path))

        await asyncio.gather(*tasks)

        # update the variable dict to have the download url for each file
        variables = deepcopy(variables)
        for variable_name, file_mapping in variable_file_mapping.items():
            for path, filename in file_mapping.items():
                filename = _trim_working_directory(filename)

                download_url = urls[filename]['download_url']
                set_at_path(variables, (variable_name,) + path, download_url)
        
    return variables


async def download_files_and_update_variables(
    variables: Dict[str, Any],
    variables_metadata: List[InputOutputMetadata],
    working_directory: str,
):
    variable_types = {i.name: i for i in variables_metadata}
    # get the mapping from DictPaths to filenames to upload
    variable_file_mapping = {
        variable_name: paths_to_filenames(
            variable_types[variable_name].jsonschema,
            variables[variable_name]
        )
        for variable_name in variable_types.keys()
    }

    files_to_download = [
        get_with_path(variables[variable_name], path)
        for variable_name, path_to_filename in variable_file_mapping.items()
        for path in path_to_filename.keys()
    ]
    # check all the files are urls
    if not all(isinstance(file, str) for file in files_to_download):
        raise ValueError(f"All files to download should be URLs, found:\n{files_to_download}")

    # remove duplicates
    files_to_download = list(set(files_to_download))

    if len(files_to_download) > 0:
        # download the files given their urls to the working directory
        tasks = []
        for download_url in files_to_download:
            tasks += [download_file(download_url, working_directory)]

        downloaded_files = await asyncio.gather(*tasks)
        assert len(downloaded_files) == len(files_to_download)
        download_url_to_path = {url: path for url, path in zip(files_to_download, downloaded_files)}

        # update the variable dict with the local paths to the downloaded files
        variables = deepcopy(variables)
        for variable_name, file_mapping in variable_file_mapping.items():
            for path, url in file_mapping.items():
                set_at_path(variables, (variable_name,) + path, download_url_to_path[url])

    return variables
