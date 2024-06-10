# my_module/setup.py
from setuptools import setup, find_packages

setup(
    name="gamesnakenrx2",
    version="0.1.0",
    description="U can run snake game in 1 sec",
    author="NRx",
    packages=find_packages(),
    install_requires=[
        'pygame',
    ],
)
