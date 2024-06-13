# setup.py
from setuptools import setup, find_packages

setup(
    name="deezvoice",
    version="0.1",
    author="Your Name Here",
    description="An API to clone voice and read text in the copied voice.",
    packages=find_packages(),
    install_requires=[
        "librosa",
        "scipy",
        "numpy"
    ],
)
