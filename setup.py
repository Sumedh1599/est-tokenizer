#!/usr/bin/env python3
"""
Setup script for EST (English → Sanskrit Tokenizer)
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

# Read version from package
version_file = Path(__file__).parent / "est" / "__init__.py"
version = "1.0.0"
if version_file.exists():
    for line in version_file.read_text().splitlines():
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break

setup(
    name="SanskritTokenizer",
    version=version,
    author="Sumedh Patil",
    author_email="sumedh1599@gmail.com",
    description="English → Sanskrit Tokenizer - Semantic tokenization engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sumedh1599/est-tokenizer",
    packages=find_packages(),
    package_data={
        'est': [],
    },
    data_files=[
        ('data', ['data/check_dictionary.csv']),
    ],
    include_package_data=True,
    install_requires=[
        # No external dependencies - pure Python
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="sanskrit tokenization nlp semantic linguistics",
    project_urls={
        "Bug Reports": "https://github.com/sumedh1599/est-tokenizer/issues",
        "Source": "https://github.com/sumedh1599/est-tokenizer",
        "Documentation": "https://github.com/sumedh1599/est-tokenizer#readme",
    },
)

