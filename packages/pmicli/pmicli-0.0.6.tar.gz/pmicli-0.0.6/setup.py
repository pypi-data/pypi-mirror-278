"""Package setup"""

import os
import pkg_resources
import subprocess
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install


def post_install_script():
    python_distribution = pkg_resources.get_distribution("pmicli").location
    conan_config = os.path.join(
        python_distribution, "pmicli", "data", "conan_config"
    )
    subprocess.run(["conan", "config", "install", conan_config], check=True, shell=True)


class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        post_install_script()


with open("README.md", "r") as f:
    long_description = f.read()

with open("pmicli/requirements.txt", "r") as f:
    requirements = f.read().splitlines()


setup(
    cmdclass={"install": CustomInstallCommand},
    name="pmicli",
    version="0.0.6",
    author="walid.boussafa@dotmatics.com",
    description="pmicli helper scripts",
    packages=find_packages(exclude=["dist", "build", "*.egg-info", "tests"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    setup_requires=requirements,
    include_package_data=True,
    entry_points={"console_scripts": ["pmicli = pmicli.main:pmicli"]},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning ",
    ],
)
