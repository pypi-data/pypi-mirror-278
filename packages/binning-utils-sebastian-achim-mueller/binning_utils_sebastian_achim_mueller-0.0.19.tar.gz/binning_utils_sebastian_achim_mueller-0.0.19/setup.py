import setuptools
import os


with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()


with open(os.path.join("binning_utils", "version.py")) as f:
    txt = f.read()
    last_line = txt.splitlines()[-1]
    version_string = last_line.split()[-1]
    version = version_string.strip("\"'")


setuptools.setup(
    name="binning_utils_sebastian-achim-mueller",
    version=version,
    description="Helps you with bin-edges, -centers, and more.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/cherenkov-plenoscope/binning_utils",
    author="Sebastian Achim Mueller",
    author_email="sebastian-achim.mueller@mpi-hd.mpg.de",
    packages=[
        "binning_utils",
    ],
    package_data={"binning_utils": []},
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
    ],
)
