import os
from setuptools import setup, find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))
# Read the contents of your requirements.txt file
with open(os.path.join(this_directory, 'requirements.txt')) as f:
    required = f.read().splitlines()


setup(
    name='codewords_core',
    version='0.1.0',
    packages=find_packages(),
    entry_points={},
    install_requires=required,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # Replace with your license
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.9',
)
