import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stattotex",
    author="Isaac Liu",
    author_email="ijyliu@gmail.com",
    release="0.1.1",
    description="A simple function for automatically updating LaTeX documents with numbers from Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ijyliu/stattotex-python",
    packages=setuptools.find_packages(),
    license='GPLv3',
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)
