import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="hybrid-garden",
    version="0.1.0",
    description="A garden of scikit-learn compatible trees constructed with genetic algorithm",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/iloncka/hybrid-garden",
    author="Ilona Kovaleva",
    author_email="iloncka.ds@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),    
    include_package_data=True,
    install_requires=["numpy", "scikit-learn", "pygad", "randomname"],
    
)
