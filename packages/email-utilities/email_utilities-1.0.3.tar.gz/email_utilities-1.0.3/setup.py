

from setuptools import setup # type: ignore

 
from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="email_utilities",
    version="1.0.3",
    description="collection of utilities for email-related tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="Felix Otoo",
    author_email="felixotoo75@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["email_utilities"],
    include_package_data=True,
    install_requires=[]
)
