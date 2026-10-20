from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="flipkart Product Recommendation",
    version="0.1.0",
    author="Kareem",
    packages=find_packages(),
    install_requires=requirements,
) 