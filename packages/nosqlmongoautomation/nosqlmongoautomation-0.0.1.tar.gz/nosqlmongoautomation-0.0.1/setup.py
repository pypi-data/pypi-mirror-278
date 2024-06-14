from setuptools import setup, find_packages
from typing import List
import os

HYPEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    requirements = []
    if os.path.exists(file_path):
        with open(file_path) as f:
            requirements = f.readlines()
            requirements = [req.strip() for req in requirements]

            if HYPEN_E_DOT in requirements:
                requirements.remove(HYPEN_E_DOT)
    return requirements

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

__version__ = "0.0.1"
REPO_NAME = "mongodb_connector"
PKG_NAME = "nosqlmongoautomation"
AUTHOR_USER_NAME = "abhishek"
AUTHOR_EMAIL = "nishkarina@protonmail.com"

requirements = get_requirements('requirements.txt')

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
    install_requires=requirements,
)
