"""Code generated by Speakeasy (https://speakeasyapi.dev). DO NOT EDIT."""

import setuptools
import re

try:
    with open('README.md', 'r') as fh:
        long_description = fh.read()
        GITHUB_URL = 'https://github.com/Unstructured-IO/unstructured-python-client.git'
        GITHUB_URL = GITHUB_URL[: -len('.git')] if GITHUB_URL.endswith('.git') else GITHUB_URL
        # links on PyPI should have absolute URLs
        long_description = re.sub(
            r'(\[[^\]]+\]\()((?!https?:)[^\)]+)(\))',
            lambda m: m.group(1) + GITHUB_URL + '/blob/master/' + m.group(2) + m.group(3),
            long_description,
        )
except FileNotFoundError:
    long_description = ''

setuptools.setup(
    name='unstructured-client',
    version='0.23.2',
    author='Unstructured',
    description='Python Client SDK for Unstructured API',
    license = 'MIT',
    url='https://github.com/Unstructured-IO/unstructured-python-client.git',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(where='src'),
    install_requires=[
        "certifi>=2023.7.22",
        "charset-normalizer>=3.2.0",
        "dataclasses-json>=0.6.4",
        "deepdiff>=6.0",
        "httpx>=0.27.0",
        "idna>=3.4",
        "jsonpath-python>=1.0.6",
        "marshmallow>=3.19.0",
        "mypy-extensions>=1.0.0",
        "nest-asyncio>=1.6.0",
        "packaging>=23.1",
        "pypdf>=4.0",
        "python-dateutil>=2.8.2",
        "requests>=2.31.0",
        "requests-toolbelt>=1.0.0",
        "six>=1.16.0",
        "typing-inspect>=0.9.0",
        "typing_extensions>=4.7.1",
        "urllib3>=1.26.18",
    ],
    extras_require={
        "dev": [
            "pylint==3.1.0",
        ],
    },
    package_dir={'': 'src'},
    python_requires='>=3.8',
    package_data={
        'unstructured-client': ['py.typed']
    },
)
