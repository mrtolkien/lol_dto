import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="lol_dto",
    version="0.0.1",
    packages=setuptools.find_packages(),
    url="https://github.com/mrtolkien/lol_dto",
    license="MIT",
    author='Gary "Tolki" Mialaret',
    author_email="gary.mialaret+pypi@gmail.com",
    description="A unified representation of League of Legends-related information.",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
