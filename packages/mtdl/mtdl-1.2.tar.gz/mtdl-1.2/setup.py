from setuptools import setup
from mtdl.metadata import __version__, __author__, __author_email__

with open("LICENSE-en", "r") as file:
    license = file.read()
    
with open("README.md", "r") as f2:
    desp = f2.read()

setup(
    name="mtdl", 
    version=__version__, 
    author_email=__author_email__, 
    author=__author__, 
    license=license, 
    description="Python multi-thread file downloader.", 
    long_description=desp, 
    long_description_content_type= "text/markdown",
    install_requires=["colorama", "tqdm"]
)