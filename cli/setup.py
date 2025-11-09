"""
TUNDRA CLI - Setup configuration
Install with: pip install -e .
"""
from setuptools import setup

setup(
    name="tundra-cli",
    version="1.0.0",
    description="TUNDRA CLI - Where intelligence learns to self-govern",
    author="TUNDRA Team",
    py_modules=["tundra_cli", "config", "utils"],
    install_requires=[
        "typer[all]>=0.9.0",
        "requests>=2.31.0",
        "rich>=13.7.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "tundra=tundra_cli:main",
        ],
    },
    python_requires=">=3.8",
)
