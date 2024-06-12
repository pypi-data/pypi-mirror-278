import json
from copy import deepcopy
from typing import Any, Dict, Generator, List, Optional, Tuple, Union

import requests
from jsonschema import Draft7Validator
from jsonschema import exceptions as jsonschema_exceptions
from jsonsubschema import isSubschema
from pydantic import BaseModel, Extra, Field, root_validator, validator
from requests.exceptions import InvalidSchema, InvalidURL, MissingSchema, RequestException

ALLOWED_FILE_FORMATS = [
    "`text`",
    "`html`",
    "`image`",
    "`audio`",
    "`video`",
    "`gif`",
    "`csv`",
    "`ics`",
    "`tsv`",
    "`docx`",
    "`xlsx`",
    "`pptx`",
    "`pdf`",
    "`json`",
    "`zip`",
    "`xml`",
    "`yaml`",
]


NON_TEXTUAL_FILE_FORMATS = [
    "`image`",
    "`audio`",
    "`video`",
    "`gif`",
    "`docx`",
    "`xlsx`",
    "`pptx`",
    "`pdf`",
    "`zip`",
]


EXAMPLE_URLS = [
    "html/website: `https://filesamples.com/samples/code/html/sample1.html`",
    "pdf: `https://filesamples.com/samples/document/pdf/sample2.pdf`",
    "image: `https://filesamples.com/samples/image/png/sample_640%C3%97426.png`",
    "csv: `https://filesamples.com/samples/document/csv/sample3.csv`",
    "audio: `https://filesamples.com/samples/audio/mp3/sample1.mp3`",
    "video: `https://filesamples.com/samples/video/mp4/sample_640x360.mp4`",
]


def add_pattern_field(schema):
    """Add pattern field to the schema if it's a URI."""
    # Base case for recursion
    if not isinstance(schema, dict):
        return schema

    # Add 'pattern' if conditions are met
    if schema.get("type") == "string" and schema.get("format") == "uri":
        schema["pattern"] = r"^((https?|wss?|ftp)://|www\.)"
        schema["message"] = {"pattern": "Must be a valid URI, e.g. https://example.com"}

    # Recurse for 'items' and 'properties' if they exist
    if "items" in schema and schema["items"] is not None:
        schema["items"] = add_pattern_field(schema["items"])

    if "properties" in schema and schema["properties"] is not None:
        for key, value in schema["properties"].items():
            schema["properties"][key] = add_pattern_field(value)

    return schema


def modify_schema_for_file_type(schema_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Modify the schema to represent a file type."""
    # Check for the specific file object structure
    if schema_dict.get("type") == "object" and "properties" in schema_dict:
        properties = schema_dict["properties"]
        if "filename" in properties and "content" in properties:
            if (
                properties["filename"].get("type") == "string"
                and properties["content"].get("type") == "string"
            ):
                # Return modified file representation
                return {"type": "string", "format": "file-path"}

    # Recursively process 'items' if it's a nested schema
    if "items" in schema_dict and schema_dict["items"] is not None:
        schema_dict["items"] = modify_schema_for_file_type(schema_dict["items"])

    # Recursively process 'properties' if they are nested schemas
    if "properties" in schema_dict:
        schema_dict["properties"] = {
            key: modify_schema_for_file_type(value)
            for key, value in schema_dict["properties"].items()
        }

    return schema_dict


def transform_file_object_to_path(json_obj):
    """Transform a file object to a path."""
    # Check for the specific file object structure
    if isinstance(json_obj, dict) and "filename" in json_obj and "content" in json_obj:
        # Example transformation: keep only the filename
        return json_obj["filename"]

    # If the object is a dictionary, recursively process its values
    if isinstance(json_obj, dict):
        return {key: transform_file_object_to_path(value) for key, value in json_obj.items()}

    # If the object is a list, recursively process its elements
    if isinstance(json_obj, list):
        return [transform_file_object_to_path(element) for element in json_obj]

    # If the object is neither a dictionary nor a list, return it as is
    return json_obj


DictPath = tuple[str | None | int]


class CWModel(BaseModel):

    # pylint: disable=W0102
    @classmethod
    def schema_description(cls, prefix: Optional[str] = None, exclude: List[str] = []) -> str:
        """Generate a description of the schema of the model."""
        schema = cls.schema()
        description = schema.get("description", "a JSON object")
        if prefix is None:
            prefix = f"{description} with the following fields:\n"

        def get_type(v):
            if v.get("type", "JSON object") == "array":
                return f"{v['type']} of {v['items'].get('type', 'JSON object')}"
            return v.get("type", "JSON object")

        return (
            prefix
            + "\n".join(
                [
                    f"- `{k}`: {v['description']} as {get_type(v)}"
                    for k, v in schema["properties"].items()
                    if k not in exclude
                ]
            )
            + "\n"
        )

    def to_example(self, extra_params={}, as_json=False) -> Union[str, Dict[str, Any]]:
        """Convert the model to an example."""
        if hasattr(self, "to_partial_example"):
            output = getattr(self, "to_partial_example")()
        else:
            output = self.dict(exclude_defaults=True, exclude_none=True)
        output.update(extra_params)
        if as_json:
            return json.dumps(output, indent=4)
        return output

    def dict(self, *args, **kwargs):
        """Override the default dict method to remove None values."""
        if "exclude_none" not in kwargs:
            kwargs["exclude_none"] = True

        if "exclude_defaults" not in kwargs:
            kwargs["exclude_defaults"] = True

        return super().dict(*args, **kwargs)


def validate_uri(uri: str):
    # Validate URI is gives a valid response
    try:
        response = requests.get(uri, timeout=5)
        # Only raise error based on status code if not 403
        if response.status_code not in [403, 400]:
            response.raise_for_status()
    except (InvalidSchema, InvalidURL, MissingSchema) as err:
        raise ValueError(
            str(err.__class__(f"Invalid URI: {uri}. Provide a valid URI", response=err.response))
        )
    except RequestException as err:
        urls = "\n".join(EXAMPLE_URLS)
        err_message = str(err) + f"\nUse from the available uri samples for different formats:\n{urls}"
        raise ValueError(str(err.__class__(err_message, response=err.response)))


class JsonSchemaLite(CWModel):
    """JSON Schema object that only has a subset of the fields."""

    # The order of the fields is important for the validation
    type: Union[str, List[str]]  # e.g. "string", "number", ["string", "null"]
    items: Optional["JsonSchemaLite"] = None # for type "array"
    properties: Optional[Dict[str, "JsonSchemaLite"]] = None # for type "object"
    format: Optional[str] = None
    description: Optional[str] = None

    def dict(self, *args, add_pattern: bool = False, **kwargs):
        schema = super().dict(*args, **kwargs)
        # Add format pattern validation
        # Currently only for URI
        if add_pattern:
            schema = add_pattern_field(schema)
        return schema

    @validator("type", pre=True, always=True)
    def check_valid_type(cls, value):
        """Validate the type field."""
        valid_types = [
            "string",
            "number",
            "integer",
            "boolean",
            "array",
            "object",
            "null",
        ]
        if isinstance(value, list):
            if not all(item in valid_types for item in value):
                raise ValueError("Invalid type specified in list")
        elif value not in valid_types:
            raise ValueError("Invalid type specified")
        return value

    @validator("format", pre=True, always=True)
    def check_valid_format(cls, value, values):
        """Validate the format field."""
        # Make sure if we have a file, the format is valid
        if values.get("type") == "object":

            if values.get("properties") is None:
                if value is not None and f"`{value}`" in ALLOWED_FILE_FORMATS:
                    values["properties"] = {"filename": {"type": "string"}, "content": {"type": "string"}}

            elif (
                values["properties"].get("filename") is not None
                and values["properties"].get("content") is not None
            ):
                if value is None:
                    raise ValueError(
                        f"Format must be specified for file with schema: {values},"
                        + " can be one of:"
                        + ", ".join(ALLOWED_FILE_FORMATS)
                    )
                if f"`{value}`" not in ALLOWED_FILE_FORMATS:
                    raise ValueError(
                        f"Invalid format `{value}` for file with schema: {values},"
                        + " can be one of:"
                        + ", ".join(ALLOWED_FILE_FORMATS)
                    )
        # If the type is string and format has `file` in raise an error
        if value is not None and values.get("type") == "string":
            if f"`{value}`" in NON_TEXTUAL_FILE_FORMATS:
                raise ValueError(
                    f"Invalid format specified for string: {value}, cannot be a file format"
                    + ", use `object` instead with a `filename` and `content` fields."
                )

        return value

    @validator("items", pre=True, always=True)
    def check_items_for_array_type(cls, value, values):
        """Validate the items field."""
        if value and values.get("type") != "array":
            raise ValueError("'items' can only be specified if type is 'array'")
        return value

    @validator("properties", pre=True, always=True)
    def check_properties_for_object_type(cls, value, values):
        """Validate the properties field."""
        if value and values.get("type") != "object":
            raise ValueError("'properties' can only be specified if type is 'object'")
        # If we have `filename` in properties, make sure it's a string and
        # we have a `content` field that is also a string
        if value is not None and "filename" in value:
            filename = value["filename"]
            if filename.get("type") != "string":
                raise ValueError(
                    f"Invalid type for filename: {filename.get('type')}, must be 'string'"
                )
            if "content" not in value:
                raise ValueError("Missing 'content' field for filename")
            content = value["content"]
            if content.get("type") != "string":
                raise ValueError(
                    f"Invalid type for content: {content.get('type')}, must be 'string'"
                )
        return value

    class Config:
        """Config for the model."""

        arbitrary_types_allowed = True

    @root_validator(pre=True)
    def validate_with_jsonschema(cls, values):
        """Validate the schema with jsonschema."""
        # Convert Pydantic models to dictionaries
        values = {
            k: (
                v.dict(exclude_defaults=True, exclude_none=True)
                if isinstance(v, BaseModel)
                else v
            )
            for k, v in values.items()
            if v is not None
        }
        # also do this with everything in properties
        if len(values.get("properties", {})) > 0:
            values["properties"] = {
                k: (
                    v.dict(exclude_defaults=True, exclude_none=True)
                    if isinstance(v, BaseModel)
                    else v
                )
                for k, v in values["properties"].items()
                if v is not None
            }

        values = pop_none_values(values)
        try:
            Draft7Validator.check_schema(values)
        except jsonschema_exceptions.SchemaError as err:
            raise ValueError(f"JSON Schema validation error: {err}") from err
        return values

    def walk(self, example=None, dict_path=()) -> Generator[Tuple["JsonSchemaLite", Any, DictPath], None, None]:
        """
        Recursively walks through the JSON schema object and yields each instance of JsonSchemaLite.

        Args:
            example (Any, optional): An example value for the input/output. Defaults to None.

        Yields:
            all JsonSchemaLite instances in the schema and their corresponding example values with a path
        """
        # Yield the current instance
        yield self, example, dict_path

        # If this instance represents an array, yield items
        if self.type == "array" and self.items:
            yield from self.items.walk(
                example=example[0] if example else None,
                dict_path=dict_path + (None,)
            )

        # If this instance represents an object, yield properties
        if self.type == "object" and self.properties:
            for prop_key, prop_schema in self.properties.items():

                # super odd bug where sometimes the schema is still a dict here
                if isinstance(prop_schema, dict):
                    print(('🙀' * 10) + f' woaaaaa what happened! Sub schema is a dict, jsonshema is {self}')
                    prop_schema = JsonSchemaLite.parse_obj(prop_schema)

                yield from prop_schema.walk(
                    example=example.get(prop_key) if example else None,
                    dict_path=dict_path + (prop_key,)
                )

    def is_file_type(self):
        return (
            self.type == "object" and
            self.properties is not None and
            "filename" in self.properties and self.properties["filename"].type == "string" and
            "content" in self.properties and self.properties["content"].type == "string"
        )

    def paths_to_file_types(self):
        for schema, _, path in self.walk():
            if schema.is_file_type():
                yield path


# some utilities for working with DictPaths
def concrete_file_paths(dict_path: DictPath, input_value: list | dict) -> list[DictPath]:
    """Get the concrete file paths from a path and an input dictionary (i.e. flatten [:])"""
    if dict_path == ():
        return [()]  # type: ignore

    head, *rest = dict_path
    rest = tuple(rest)

    # if it's a list, we need to get the concrete file paths for each item
    if head is None and isinstance(input_value, list):
        return [
            (i,) + p for i, elem in enumerate(input_value) for p in concrete_file_paths(rest, elem)
        ]  # type: ignore

    # at this point, we know it's a dictionary
    if isinstance(input_value, dict):
        return [(head,) + p for p in concrete_file_paths(rest, input_value[head])]  # type: ignore

    raise ValueError(f"Cannot get concrete file paths for {dict_path} and {input_value}")


def get_with_path(obj, path):
    if None in path:
        raise ValueError(f'Cannot have None in path when calling get_with_path: {path}')

    if path == ():
        return obj

    head, *rest = path
    return get_with_path(obj[head], tuple(rest))


def set_at_path(obj, path, value):
    if len(path) == 0:
        raise ValueError('Cannot set at empty path')

    if len(path) == 1:
        obj[path[0]] = value
        return

    head, *rest = path
    set_at_path(obj[head], rest, value)


def paths_to_filenames(jsonschema, input_value) -> dict[DictPath, str]:
    """Get a dictionary mapping paths to filenames in the input dict."""
    file_paths = jsonschema.paths_to_file_types()
    concrete_paths = [
        p
        for file_path in file_paths
        for p in concrete_file_paths(file_path, input_value)
    ]
    return {
        p: get_with_path(input_value, p) for p in concrete_paths
    }


class InputOutputMetadata(CWModel, extra=Extra.allow):
    """Metadata for an input or output of a node in the workflow."""

    name: str = Field(description="The name of the field")
    jsonschema: JsonSchemaLite = Field(
        description="A concise JSON Schema object describing the "
        + f"type of the input/output only has {', '.join(JsonSchemaLite.__fields__.keys())} as keys."
        + " Files are represented as an object with `filename` (string), `content` (string)."
        + " For `xlsx` files, the `content` field should be a CSV string.\n"
        + "The available file formats are: "
        + ", ".join(ALLOWED_FILE_FORMATS),
    )
    example: Any = Field(description="An example value for the input/output.")
    required: bool = Field(
        description="Whether the input/output is required or not should be lower case, e.g. true or false",
        default=True,
    )

    def to_string(self, multiline=False, convert_file_types=False) -> str:
        """Convert the metadata to a string."""
        schema = self.jsonschema.dict(exclude_defaults=True, exclude_none=True)
        example = self.example
        suffix = ""
        if convert_file_types:
            schema = modify_schema_for_file_type(schema)
            example = transform_file_object_to_path(example)
            if "file-path" in json.dumps(schema):
                suffix = ". Note: this is a string representing the file path NOT the actual file content."
        schema_str = json.dumps(schema)
        # schema_str = self.jsonschema.json(exclude_defaults=True, exclude_none=True)
        sep = "\n" if multiline else " "
        return (
            f"Name {self.name},{sep}Schema: {schema_str},{sep}Example: {json.dumps(example)},{sep}Required: {str(self.required).lower()}"
            + suffix
        )

    @root_validator(pre=True)
    def validate_example_against_schema(cls, values):
        """Validate the example against the schema."""
        return cls._validate(values)

    @classmethod
    def _validate(cls, values, validate_uris=False):
        # copy the values so following mutations don't affect original
        values = deepcopy(values)

        schema = values["jsonschema"]
        if isinstance(schema, JsonSchemaLite):
            schema = schema.dict(exclude_defaults=True, exclude_none=True, add_pattern=True)

        if "example" not in values:
            # Check if it's in the schema
            if "example" in schema:
                values["example"] = schema.pop("example")
            else:
                raise ValueError(
                    f"Input/Output with the name `{values.get('name', '')}` is missing an example"
                )

        example = values["example"]

        try:
            schema = pop_none_values(schema)
            # Ensure the schema is correct first
            schema_obj = JsonSchemaLite.parse_obj(schema)
            Draft7Validator(schema).validate(instance=example)
        except jsonschema_exceptions.ValidationError as err:
            name = values.get("name", "")
            raise ValueError(
                f"The Example of `{name}`: ```json {json.dumps(example)}``` does not adhere"
                + f" to its JSON Schema {schema}.\nValidation Error: {err.message}"
            ) from err

        if validate_uris:
            # Extra checks for URIs
            for schema, value, _ in JsonSchemaLite.parse_obj(schema_obj).walk(example):
                if schema.format == "uri" and value is not None:
                    validate_uri(value)
        return values

    def check_compatibility(
        self, other: "InputOutputMetadata", self_prefix: str, other_prefix: str
    ):
        """check that this input/output is compatible with another input/output

        NOTE: this function is not symmetric, i.e. self.check_compatibility(other) != other.check_compatibility(self)
        """
        errors = []
        if self.name != other.name:
            errors += [f"Names do not match: {self.name} != {other.name}"]

        schema_this = self.jsonschema.dict(exclude_defaults=True, exclude_none=True)
        schema_other = other.jsonschema.dict(exclude_defaults=True, exclude_none=True)
        # by the _validate method of this class we know that the examples are valid
        # is the other schema the same or more specific than this schema?
        if not isSubschema(schema_other, schema_this):
            errors += [
                f"Cannot convert from {json.dumps(schema_other)} to {json.dumps(schema_this)}"
            ]

        if len(errors):
            errors_str = "\n".join([f"* {e}" for e in errors])
            raise ValueError(
                f"{self_prefix.capitalize()} {self.name} is not compatible with {other_prefix} {other.name}:\n{errors_str}"
            )


def pop_none_values(d):
    """
    Recursively removes keys with None values from a dictionary.
    """
    keys_to_pop = [key for key, value in d.items() if value is None]
    for key in keys_to_pop:
        d.pop(key)

    for key, value in d.items():
        if isinstance(value, dict):
            pop_none_values(value)

    return d
