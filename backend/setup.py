"""
Setup script for Steam Config Analyzer Backend.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="steam-config-analyzer",
    version="2.0.0",
    author="grimm00",
    author_email="",
    description="User-friendly tool for Steam Deck configuration management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grimm00/steam-config-analyzer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "Topic :: Games/Entertainment",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.13",
    install_requires=[
        "vdf>=3.4",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "steam-config-analyzer=cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
