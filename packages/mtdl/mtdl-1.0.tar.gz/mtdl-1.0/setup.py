from setuptools import setup
from mtdl.metadata import __version__, __author__, __author_email__

with open("LICENSE-en", "r") as file:
    license = file.read()

setup(
    name="mtdl", 
    version=__version__, 
    author_email=__author_email__, 
    author=__author__, 
    license=license, 
    description="Python multi-thread file downloader.", 
    scripts=["bin/mtdl.py"], 
    install_requires=["colorama", "tqdm"]
)