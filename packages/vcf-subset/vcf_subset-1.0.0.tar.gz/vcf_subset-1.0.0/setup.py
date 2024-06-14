# Based on example https://github.com/pybind/python_example
from pybind11.setup_helpers import Pybind11Extension
from setuptools import setup
import os

__version__ = "v1.0.0"

long_description = "Efficient VCF subsetting by genome position."

files = sorted(["vcf_subset.cpp"])

ext_modules = [
    Pybind11Extension(
        "vcf_subset",
        files,
        include_dirs=[],
        extra_compile_args=["-std=c++2a", "-O3"],
        # Example: passing in the version to the compiled code
        define_macros=[("VERSION_INFO", __version__)],
    ),
]

setup(
    name="vcf_subset",
    version=__version__,
    author="Jeremy Westhead",
    author_email="jeremy.westhead@ndm.ox.ac.uk",
    url="https://github.com/GlobalPathogenAnalysisService/vcf_subset",
    description="Efficient VCF subsetting by genome position.",
    ext_modules=ext_modules,
    zip_safe=False,
    python_requires=">=3.7",
    license="MIT",
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={'vcf_subset': ['./**']}
)