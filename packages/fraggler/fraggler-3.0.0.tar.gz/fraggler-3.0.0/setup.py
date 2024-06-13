import setuptools
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setuptools.setup(
    name="fraggler",
    version="3.0.0",
    description="Fragment Analysis package in python!",
    url="https://github.com/willros/fraggler",
    author="William Rosenbaum and Pär Larsson",
    author_email="william.rosenbaum@umu.se",
    license="MIT",
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.10",
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "matplotlib",
        "lmfit",
        "scipy",
        "biopython",
        "panel",
        "altair",
        "setuptools",
        "pandas-flavor",
    ],
    entry_points={"console_scripts": ["fraggler=fraggler.fraggler:cli"]},
)
