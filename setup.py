import os

from setuptools import find_packages, setup

# https://packaging.python.org/single_source_version/
base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, "pyfvm", "__about__.py")) as f:
    exec(f.read(), about)


setup(
    name="pyfvm",
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    packages=find_packages(),
    description="Finite volume discretizations for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nschloe/pyfvm",
    license=about["__license__"],
    platforms="any",
    install_requires=["sphinxcontrib-bibtex", "meshplex", "numpy", "scipy", "sympy"],
    python_requires=">=3.6",
    classifiers=[
        about["__license__"],
        about["__status__"],
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
)
