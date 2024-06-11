from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="oveya",
    version="0.1.27",
    description="A nano-framework for deploying Python functions as APIs on AWS Lambda using Function URLs.",
    author="Spencer Porter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'pydantic==2.6.4',
    ],
    packages=find_packages(),
    python_requires='>=3.6',
)
