from setuptools import setup, find_packages
from viggoprecificacao._version import version

REQUIRED_PACKAGES = [
    'viggocore>=1.0.0,<2.0.0',
    'flask-cors'
]

setup(
    name="viggoprecificacao",
    version=version,
    summary='ViggoPrecificacao Module Framework',
    description="ViggoPrecificacao Backend Flask REST service",
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIRED_PACKAGES
)
