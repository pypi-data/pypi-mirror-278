from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="wowhmm",
    version="0.1.1",
    description="Who owes whom how much money",
    packages=find_packages(),
    install_requires=[
        "pandas==2.2.2",
    ],
)
