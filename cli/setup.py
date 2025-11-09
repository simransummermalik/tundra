"""
TUNDRA CLI - Setup configuration
Install with: pip install -e .
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.MD"
long_description = readme_path.read_text() if readme_path.exists() else ""

setup(
    name="tundra-cli",
    version="1.0.0",
    description="TUNDRA CLI - Where intelligence learns to self-govern",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="TUNDRA Team",
    author_email="contact@tundra.ai",
    url="https://github.com/yourusername/tundra",
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
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    keywords="ai, marketplace, cli, automation, agents",
)
