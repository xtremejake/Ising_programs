import setuptools
from os import path

FILE_DIR = path.dirname(path.abspath(__file__))
README_FILE = path.join(path.dirname(FILE_DIR), 'README.md')
REQUIREMENTS_FILE = path.join(path.dirname(FILE_DIR), 'requirements.txt')

# description
with open(README_FILE, "r") as fh:
    long_description = fh.read()

# package requirements
with open(REQUIREMENTS_FILE, 'r') as fh:
    requirements = fh.read()

setuptools.setup(
    name='ising',
    version='0.1',
    description='For global fitting of systems represented by 1D Ising Models',
    url='https://github.com/barricklab-at-jhu/Ising_programs',
    author='barricklab-at-jhu, xtremejake',
    author_email='barrick@jhu.edu, xtremejake.usa@gmail.com',
    license='Apache-2.0',
    #install_requires=[] # specifies dependencies of python packages in pip
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)