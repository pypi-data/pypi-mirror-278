#!/usr/bin/env python
# -*- coding: utf-8 -*-
import warnings

"""The setup script."""

from setuptools import find_packages, setup

REQUIREMENTS_FILES = ["requirements.txt"]


def load_requirements():
    # TODO -- confirm below works/delete this
    requirements = {"click", "loguru", "requests", "typer"}
    with open("hamilton_ui/requirements-mini.txt") as f:
        requirements.update(line.strip() for line in f)
    return list(requirements)


setup(
    name="sf-hamilton-ui",  # there's already a hamilton in pypi
    version="0.0.1",
    description="Hamilton, the micro-framework for creating dataframes.",
    long_description="""Hamilton tracking server, see [the docs for more](https://github.com/dagworks-inc/hamilton/tree/main/ui/)""",
    long_description_content_type="text/markdown",
    author="Stefan Krawczyk, Elijah ben Izzy",
    author_email="stefan@dagworks.io,elijah@dagworks.io",
    url="https://github.com/dagworks-inc/hamilton",
    packages=find_packages(exclude=["tests"], include=["hamilton_ui", "hamilton_ui.*"]),
    include_package_data=True,
    install_requires=load_requirements(),
    zip_safe=False,
    keywords="hamilton",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    # Note that this feature requires pep8 >= v9 and a version of setup tools greater than the
    # default version installed with virtualenv. Make sure to update your tools!
    python_requires=">=3.6, <4",
    # adding this to slim the package down, since these dependencies are only used in certain contexts.
    extras_require={
        "visualization": ["graphviz", "networkx"],
        "dask": ["dask[complete]"],  # commonly you'll want everything.
        "dask-array": ["dask[array]"],
        "dask-core": ["dask-core"],
        "dask-dataframe": ["dask[dataframe]"],
        "dask-diagnostics": ["dask[diagnostics]"],
        "dask-distributed": ["dask[distributed]"],
        "ray": ["ray>=2.0.0", "pyarrow"],
        "pyspark": [
            # we have to run these dependencies cause Spark does not check to ensure the right target was called
            "pyspark[pandas_on_spark,sql]",
            # This is problematic, see https://stackoverflow.com/questions/76072664/convert-pyspark-dataframe-to-pandas-dataframe-fails-on-timestamp-column
            "pandas<2.0",
        ],  # I'm sure they'll add support soon,
        # but for now its not compatible
        "pandera": ["pandera"],
        "slack": ["slack-sdk"],
        "tqdm": ["tqdm"],
        "datadog": ["ddtrace"],
        "vaex": [
            "pydantic<2.0",  # because of https://github.com/vaexio/vaex/issues/2384
            "vaex",
        ],
        "experiments": [
            "fastapi",
            "fastui",
            "uvicorn",
        ],
        "diskcache": ["diskcache"],
        "cli": ["typer"],
        "sdk": ["sf-hamilton-sdk"],
        "ui": load_requirements(),
    },
    entry_points={
        "console_scripts": [
            "h_experiments = hamilton.plugins.h_experiments.__main__:main",
            "hamilton = hamilton.cli.__main__:cli",
            "hamilton-serve = hamilton.server.__main__:run",
            "hamilton-admin-build-ui = hamilton.admin:build_ui",
            "hamilton-admin-build-and-publish = hamilton.admin:build_and_publish",
        ]
    },
    # Relevant project URLs
    project_urls={  # Optional
        "Bug Reports": "https://github.com/dagworks-inc/hamilton/issues",
        "Source": "https://github.com/dagworks-inc/hamilton",
    },
)
