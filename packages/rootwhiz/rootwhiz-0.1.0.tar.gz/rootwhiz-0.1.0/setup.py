from setuptools import setup, find_packages

setup(
    name="rootwhiz",
    version="0.1.0",
    author="Til Schwarze",
    author_email="til@alatorgenesis.com",
    description="RootWhiz is a Python package that simplifies directory navigation and path manipulation.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/justTil/RootWhiz",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "setuptools"
    ],
)
