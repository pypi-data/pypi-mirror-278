from setuptools import setup, find_packages
import os


os.system("rm -rf build dist")

setup(
    name="state_graph",
    version="0.1.8",
    packages=find_packages(),
    install_requires=[
        "pydantic",
        "networkx",
        "matplotlib",
        "beartype",
        "rich",
        "ipython",
        "resend",
    ],
)
