from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.0'
DESCRIPTION = 'Easy CLI\'s'
LONG_DESCRIPTION = 'PyLine is a Python package to easily create interactive CLI\'s.'

# Setting up
setup(
    name="pyline-cli",
    version=VERSION,
    author="Heavy Lvy",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['fuzzywuzzy'],
    keywords=['python', 'cli'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
