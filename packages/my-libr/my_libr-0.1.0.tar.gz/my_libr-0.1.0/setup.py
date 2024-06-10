

from setuptools import find_packages, setup


setup(
    name="my_libr",
    version="0.1.0",
    author="Petr Gregor (SDA)",
    autho_email="pe.gregor@gmail.com",
    packages=find_packages(),
    licence="Open-source",
    include_package_data=True,
    description="Super useful library"
)