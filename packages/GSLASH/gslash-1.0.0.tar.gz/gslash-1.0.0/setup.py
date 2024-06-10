from setuptools import setup, find_packages
import os

# Wczytanie zawartości readme.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="GSLASH",
    version="1.0.0",
    author="GSLASH Development",
    description="This is cython but other rules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        # tutaj wpisz wymagane biblioteki, np.
        # 'numpy',
        # 'requests',
    ],
)
