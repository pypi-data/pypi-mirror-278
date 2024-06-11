from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Python tools for forensics and crypto'
LONG_DESCRIPTION = 'blem :)'

# Setting up
setup(
    name="Py_RHT",
    version=VERSION,
    author="Jay Feldman",
    author_email="<feldmanjay@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=['src\Py_RHT'] + ['src\Py_RHT.' + pkg for pkg in find_packages('src\Py_RHT')],
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
    ]
)