from setuptools import setup, find_packages

setup(
    name="tundra-cli",
    version="1.0.0",
    py_modules=["cli"],
    install_requires=[
        "click>=8.0.0",
        "requests>=2.31.0",
        "fastapi>=0.115.0",
        "uvicorn>=0.31.0",
        "motor>=3.3.2",
        "openai>=2.7.1",
        "playwright>=1.48.0",
        "beautifulsoup4>=4.14.2",
        "python-dotenv>=1.0.1",
        "pydantic>=2.8.2",
    ],
    entry_points={
        "console_scripts": [
            "tundra=cli:cli",
        ],
    },
    python_requires=">=3.8",
    author="Tundra Team",
    description="Command-line interface for Tundra A2A marketplace",
    long_description=open("../README.md").read() if __file__ else "",
    long_description_content_type="text/markdown",
)
