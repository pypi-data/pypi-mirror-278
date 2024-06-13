from setuptools import find_packages, setup

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dummypackage12624",
    version="0.0.14",
    author="ronilpatil",
    author_email="xyz@gmail.com",
    description="creating dummy pyton package",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/ronylpatil/test_package",
    project_urls={
        "Bug Tracker": f"https://github.com/ronylpatil/test_package/issues",
    },
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src")
)
