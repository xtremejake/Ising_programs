import setuptools

setuptools.setup(
    name="ising",
    version="0.1",
    description="For global fitting of systems represented by 1D Ising Models",
    url="https://github.com/barricklab-at-jhu/Ising_programs",
    author="barricklab-at-jhu, xtremejake",
    author_email="barrick@jhu.edu, xtremejake.usa@gmail.com",
    license="Apache-2.0",
    include_package_metadata=True,
    install_requires=[
        "black==19.10b0",
        "jupyter==1.0.0",
        "lmfit==1.0.1",
        "numpy==1.18.5",
        "pandas==1.0.4",
        "sympy==1.6",
    ],  # specifies dependencies of python packages in pip
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
