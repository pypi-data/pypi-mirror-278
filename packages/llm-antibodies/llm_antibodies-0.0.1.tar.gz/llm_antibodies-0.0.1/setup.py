from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="antibodies-rafaelsandroni",
    version="0.0.1",
    author="rafaelsandroni",
    author_email="rafael@metatext.io",
    description="Antibodies for LLM hallucinations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rafaelsandroni/antibodies",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)