from __future__ import annotations
from setuptools import setup

setup(
    name="excelize",
    version="0.0.1",
    license="BSD",
    description="A Python library for reading and writing Excel files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="xuri",
    author_email="xuri.me@gmail.com",
    zip_safe=False,
    include_package_data=True,
    python_requires='>=3.7',
)