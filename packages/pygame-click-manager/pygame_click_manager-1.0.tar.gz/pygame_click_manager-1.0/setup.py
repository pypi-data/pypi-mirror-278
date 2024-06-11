from setuptools import setup, find_packages

VERSION = '1.0'
NAME = "pygame_click_manager"
AUTHOR = "FrickTzy (Kurt Arnoco)"
DESCRIPTION = 'A package for managing clicks in pygame.'

with open("README.md", "r") as file:
    long_description = file.read()

URL = 'https://github.com/FrickTzy/Pygame-Click-Manager'

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    url=URL,
    keywords=['python', 'pygame', 'python game', 'python game development', 'pygame button'],
)