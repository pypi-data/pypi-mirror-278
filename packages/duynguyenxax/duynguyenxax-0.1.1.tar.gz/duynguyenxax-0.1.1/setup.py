from setuptools import setup, find_packages

setup(
    name="duynguyenxax",
    version="0.1.1",
    author="DuySota",
    author_email="duy.hoang@sotatek.com",
    description="A simple example library",
    packages=find_packages(include=("inference.py")),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
