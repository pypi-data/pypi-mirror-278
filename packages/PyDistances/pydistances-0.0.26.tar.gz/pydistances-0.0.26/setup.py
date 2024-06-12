from setuptools import setup, find_packages

##
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PyDistances",
    version="0.0.26",
    author="Fabio Scielzo Ortiz",
    author_email="fabioscielzo98@gmail.com",
    description="PyDistances is a Python package for computing classic statistical distances as well as new proposals suitable for mixed multivariate data, even with outliers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FabioScielzoOrtiz/Distances_Package",  # add your project URL here
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pandas','numpy'],
    python_requires=">=3.7"
)
