import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stattotex",
    version="0.0.1",
    author="Isaac Liu",
    author_email="ijyliu@gmail.com",
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
