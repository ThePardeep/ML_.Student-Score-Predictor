from setuptools import setup, find_packages
from typing import List

HYPEN_E_DOT = "-e ."


def getPackagesList(file_name: str) -> List[str]:
    """
    This function read packages file and return list of packages.
    """
    with open(file_name) as f:
        packages = []
        packages = f.read().splitlines()
        if HYPEN_E_DOT in packages:
            packages.remove(HYPEN_E_DOT)
        return packages


setup(
    name="Predict student score",
    author="Pardeep Saini",
    version="0.0.1",
    author_email=["pardeepsaini54321@gmail.com"],
    description="Predict student score.",
    packages=find_packages(),
    install_requires=getPackagesList("requirements.txt"),
)
