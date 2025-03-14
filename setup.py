# Standard Library
from os import chdir, pardir, path

# Third-Party
from setuptools import setup

with open(path.join(path.dirname(__file__), "README.md"), encoding="utf-8") as readme:
    README = readme.read()

# allow setup.py to be run from any path
chdir(path.normpath(path.join(path.abspath(__file__), pardir)))

setup(
    name="EAS2Text-Remastered",
    packages=["EAS2Text"],
    package_data={'EAS2Text': ['templates/*.json']},
    version="0.1.24.4",
    description="A Python library to convert raw EAS header data to a human readable text - Remastered",
    author="secludedhusky",
    author_email="secludedhusky@chesbaycommunications.com",
    license="ODbL-1.0",
    install_requires=[],
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Newton-Communications/E2T",
    keywords="eas alerting emergency-alert-system",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: Other/Proprietary License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    include_package_data=True,  # Ensure non-Python files are included
)
