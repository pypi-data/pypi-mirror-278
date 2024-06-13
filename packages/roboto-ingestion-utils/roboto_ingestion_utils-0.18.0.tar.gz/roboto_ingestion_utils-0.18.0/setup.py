from setuptools import setup, find_packages
import os

setup_config = {
        "name": 'roboto_ingestion_utils',
    "author": 'Roboto Technologies',
    "author_email": 'yves@roboto.ai',
    "description": 'Utility functions for roboto data ingestion',
    "long_description": open('README.md').read(),
    "long_description_content_type": 'text/markdown',
    "url": 'https://github.com/roboto-ai/roboto-ingestion-utils',
    "packages": find_packages(),
    "classifiers": [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    "python_requires" : '>=3.8',

    "install_requires": ['roboto', 'pytest', 'mcap', 'genson',],
}

version = os.getenv("GITHUB_REF_NAME")
# only add versioning if ref is a numeric tag
if version:
    if False not in [v.isnumeric() for v in version.split('.')]: 
        print(f"deploying version {version}...")
        setup_config["version"] = version
        setup_config["download_url"] = f"https://github.com/roboto-ai/roboto_ingestion_utils/archive/refs/tags/{version}.tar.gz"
setup(**setup_config)


