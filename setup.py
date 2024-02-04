"""Setup for the project's package."""

from setuptools import find_packages, setup

REQUIREMENTS = []

requirements_file = 'requirements.txt'

# Open and read the requirements.txt file
with open(requirements_file, 'r') as file:
    for line in file:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        REQUIREMENTS.append(line)

setup(
    name="maze-solvers",
    version="0.1.0",
    description="This package contains the implementation of the search algorithms, solving a random nxn maze.",
    author="Zaid Ghazal",
    python_requires=">=3.9",
    packages=find_packages(include=["src", "src.*"]),
    install_requires=REQUIREMENTS,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "search-algorithms=src.cli:app",
        ]
    },
)
