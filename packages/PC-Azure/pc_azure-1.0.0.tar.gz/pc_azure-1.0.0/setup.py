from setuptools import setup, find_packages

def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()

def read_file(file):
   with open(file) as f:
        return f.read()
    
long_description = read_file("README.md")
version = read_file("VERSION")
requirements = read_requirements("requirements.txt")

setup(
    name = 'PC_Azure',  # Official name of the package in the registry, for example on PyPI (pypi.org)
    version = version,
    author = 'Marcos E. Mercado',
    author_email = 'marcos.mercado@activision.com',
    url = '', # URL to the GitHub repository
    description = 'This package includes modules to interact with Microsoft Azure.',
    keywords = ['Azure', 'Key Vault', 'secret'],    # Keywords users can search on registry, for example on pypi.org
    long_description_content_type = "text/markdown", # "text/x-rst",  # If this causes a warning, upgrade your setuptools package
    long_description = long_description,
    license = "MIT license",
    packages = find_packages(exclude=["tests"]),  # Don't include tests directory in binary distribution
    install_requires = requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]  # Update these accordingly
)