import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
VERSION = '1.0.11'
PACKAGE_NAME = 'opengate-data'
AUTHOR = 'amplia soluciones'
AUTHOR_EMAIL = 'pipy@amplia.es'

LICENSE = 'Apache License 2.0'
DESCRIPTION = 'description'

INSTALL_REQUIRES = [
    'pandas',
    'requests',
    'jsonpath_ng',
    'numpy',
    'urllib3',
    'configparser',
    'parse',
    'python-dotenv',
    'datetime',
    'flatten-dict'
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    python_requires='>=3.10',
    include_package_data=True,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)