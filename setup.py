# -*- coding: utf-8 -*-
"""Installer for the collective.fieldedit package."""

from setuptools import find_packages
from setuptools import setup


setup(
    name="collective.fieldedit",
    version="1.0a3.dev0",
    description="A flexible form to edit selected fields of a content type.",
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone",
    author="Philip Bauer",
    author_email="bauer@starzel.de",
    url="https://pypi.python.org/pypi/collective.fieldedit",
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        "plone.api",
        "setuptools",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.app.robotframework",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
