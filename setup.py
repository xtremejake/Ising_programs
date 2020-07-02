import setuptools
import itertools

INSTALL_REQUIRES = [
        "jupyter==1.0.0",
        "lmfit==1.0.1",
        "numpy==1.18.5",
        "pandas==1.0.4",
        "matplotlib",
        "sympy==1.6",
        "pingouin",
]

EXTRAS_REQUIRE = {
    "dev": [],
    "test": [
        "pytest==5.4.3",
        "black==19.10b0"
    ]
}

# populate dev from specified deps
EXTRAS_REQUIRE["dev"] = list(itertools.chain.from_iterable(EXTRAS_REQUIRE.values()))

setuptools.setup(
    name="ising",
    version="0.1",
    description="For global fitting of systems represented by 1D Ising Models",
    url="https://github.com/barricklab-at-jhu/Ising_programs",
    author="barricklab-at-jhu, xtremejake",
    author_email="barrick@jhu.edu, xtremejake.usa@gmail.com",
    license="Apache-2.0",
    include_package_metadata=True,
    include_package_data=True,
    package_dir={"ising": "ising"},
    package_data={
        "ising": [
            "data/T4V_data/*.csv",
            "data/NRC_data/*.dat",
            "data/NRC_data/*.csv",
        ]
    },
    install_requires=INSTALL_REQUIRES,  # specifies dependencies of python packages in pip
    extras_require=EXTRAS_REQUIRE,
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
