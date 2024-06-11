from __future__ import annotations

import pathlib

from setuptools import find_packages, setup  # type: ignore

# Get the long description from the README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="py_dotenv_safe",
    version="1.0.0",
    description="A robust Python library for managing environment variables with .env files, ensuring they are all present and correctly configured.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jainil Jakasaniya",
    author_email="jainiljakasaniya@gmail.com",
    url="https://github.com/jainiljakasaniya/py_dotenv_safe",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "python-dotenv>=1.0.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "py_dotenv_safe=py_dotenv_safe.config:main",
        ],
    },
)
