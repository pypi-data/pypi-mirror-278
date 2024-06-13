from setuptools import setup
from setuptools import find_packages


with open("README.md") as f:
    long_description = f.read()

setup(
    package_dir={"": "."},
    packages=find_packages("."),
    package_data={"": ["*.json", "*.yaml", "*.ini"]},
    include_package_data=True,
    entry_points={"console_scripts": ["nexora=nexora.cli.autotuna:main"]},
    long_description=long_description,
    long_description_content_type="text/markdown",
)
