import pathlib

import setuptools

setuptools.setup(
    name = "cvrp",
    version= '0.1.0',
    description= 'A Python implementation for solving the Capacitated Vehicle Routing Problem (CVRP) using heuristic and metaheuristic algorithms',
    long_description= pathlib.Path("Readme.md").read_text(),
    long_description_content_type= 'text/markdown',
    author = 'Alikacem Faycal',
    author_email= 'faycal213.dz@gmail.com',
    license = 'The unlicense',
    project_urls = {
        'Source' : 'https://github.com/Faycal214/Vehicle-Routing-Problem'
    },
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
    ],
    python_requires = '>= 3.10, <3.13',
    install_requires = ["numpy",  "random", "matplotlib", "networkx"],
    packages= setuptools.find_packages(),
    include_package_data= True,
    extras_requires = {
        "dev" : ["pytest >= 7.0", "twine >= 4.0.2"]
    },
)