'''Installer for the package.'''

import pathlib
from setuptools import find_packages, setup

PATH = pathlib.Path(__file__).parent

README = (PATH / "README.md").read_text()

setup(
	name = 'py-tkoverlay',
	version = '1.1.0',
	description = 'A package that creates and manipulates screen overlays based on tkinter.',
	long_description = README,
	long_description_content_type = "text/markdown",
	url = 'https://github.com/KavyanshKhaitan2/py-tkoverlay',
	author = 'Kavyansh Khaitan',
	author_email = "kavyanshkhaitan11@gmail.com",
	license = 'MIT',
	packages = find_packages(),
	include_package_data = True,
)
