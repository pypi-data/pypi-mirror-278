# setup.py
from setuptools import setup, find_packages

setup(
    name="fa-cli",
    version="1.1.4",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer[all]",
        "rich",
        "gitpython"
    ],
    entry_points={
        "console_scripts": [
            "fa=fa_cli.main:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
