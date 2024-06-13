from setuptools import find_packages, setup

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()
setup(
    name="dummypackage12624",
    version="0.0.23",
    author="ronilpatil",
    author_email="xyz@gmail.com",
    description=("Dummy python package"),
    keywords=["package", "python", "pytest"],
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/ronylpatil/test_package",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Topic :: Communications :: Chat",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization"
    ],
    python_requires=">=3.9",
    project_urls={
        "Bug Tracker": f"https://github.com/ronylpatil/test_package/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),  
)

# ref. for classifiers: https://pypi.org/classifiers/