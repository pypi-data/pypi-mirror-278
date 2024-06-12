import re
import os
from distutils.command.register import register as register_orig
from distutils.command.upload import upload as upload_orig
from setuptools import setup,find_packages

# Read version from file without loading the module
with open('src/WatchagornCommonLibrary/version.py', 'r') as version_file:
    version_match = re.search(r"^VERSION ?= ?['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    long_description=open('README.md').read(),
if version_match:
    VERSION=version_match.group(1)
else:
    VERSION='0.1'

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'robotframework==5.0',
    'robotframework-browsermobproxylibrary==0.1.3',
    'robotframework-seleniumlibrary==5.1.3',
    'robotframework-seleniumtestability==1.1.0',
    'robotframework-pdf2textlibrary==1.0.1',
    'robotframework-pabot==2.5.3',
    'robotframework-jsonlibrary==0.3.1',
    'robotframework-imaplibrary2==0.4.0',
    'robotframework-excellib==2.0.1',
    'robotframework-appiumlibrary==1.6.3',
    'PyYAML==5.3.1',
    'DateTime==4.3',
    'openpyxl==3.0.9',
    'opencv-python==4.5.5.62'
]

test_requirements = [
    # TODO: put package test requirements here
]


CLASSIFIERS = """
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Framework :: Robot Framework
Framework :: Robot Framework :: Library
"""[1:-1]


setup(
    name='Robotframework-WatchagornCommonLibrary',
    version=VERSION,
    description="Watchagorn common library for robot framework",
    author="Watchagorn Pattummee",
    author_email='wpchagorn24@gmail.com',
    url='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='WatchagornWebCommon, WatchagornCommon, WatchagornAppCommon,WatchagornCommonLibrary',
    classifiers=CLASSIFIERS.splitlines(),
    test_suite='tests',
    tests_require=test_requirements
)