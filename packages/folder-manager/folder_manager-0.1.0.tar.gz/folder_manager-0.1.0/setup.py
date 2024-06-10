# setup.py
from setuptools import setup, find_packages

setup(
    name="folder_manager",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Add any dependencies here
    ],
    entry_points={
        "console_scripts": [
            # Add any command line scripts here
            "folder-manager=folder_manager:main",
        ],
    },
    author="Javer Valino",
    description="A simple folder management library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/phintegrator/folder_manager", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
