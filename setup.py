# -*- coding: utf-8 -*-
"""Setup configuration."""
from setuptools import find_packages
from setuptools import setup


setup(
    name="immutable_data_validation",
    version="0.2.1",
    description="Validating basic Python data types.",
    url="https://github.com/CuriBio/immutable-data-validation",
    author="Curi Bio",
    author_email="contact@curibio.com",
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["validator-collection>=1.3.5"],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Scientific/Engineering",
    ],
)
