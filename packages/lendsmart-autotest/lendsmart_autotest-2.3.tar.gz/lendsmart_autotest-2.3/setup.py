"""
A setuptools based setup module
"""
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

setup(
    name="lendsmart_autotest",
    version="2.3",
    description="The internal SDK for lendsmart autotest",
    url="https://bitbucket.org/lendsmartlabs/lendsmart_py/",
    # Author details
    author="Lendsmart",
    author_email="infos@lendsmart.ai",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    # What does your project relate to?
    keywords="lendsmart autotest",
    packages=find_packages(exclude=["contrib", "tests"]),
    # What do we need for this to run
    install_requires=[
        "selenium==3.8.0",
        "keyboard",
        "pytest",
        "requests",
        "boto3",
        "PyAutoGUI",
        "urllib3",
        "pytest-html",
        "importlib-metadata",
        "Faker",
        "ramda",
        "webdriver_manager",
        "networkx",
    ],
    tests_require=[
        "mock",
    ],
)
