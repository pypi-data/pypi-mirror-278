from setuptools import setup, find_packages
from typing import List

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

__version__ = "0.0.2"
REPO_NAME = "Mongodb_Connector_Package"
PKG_NAME = "pymongo-connector"
AUTHOR_USER_NAME = "chaitanya-24"
AUTHOR_EMAIL = "csawant2407@gmail.com"

setup(
    name=PKG_NAME,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A python package for connecting with database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pymongo",
        "pymongo[srv]",
        "dnspython",
        "pandas",
        "numpy",
        "ensure",
        "pytest"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)