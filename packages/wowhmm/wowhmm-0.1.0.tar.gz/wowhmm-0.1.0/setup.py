from setuptools import find_packages, setup

setup(
    name="wowhmm",
    version="0.1.0",
    description="Who owes whom how much money",
    packages=find_packages(),
    install_requires=[
        "pandas==2.2.2",
    ],
)
