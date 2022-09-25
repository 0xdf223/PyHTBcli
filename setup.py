from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="PyHTBcli",
    version="0.0.7",
    author="0xdf",
    author_email="0xdf.223@gmail.com",
    description="Command line interface for HackTheBox",
    long_description=long_description,
    url="https://github.com/0xdf223/PyHTBcli",
    py_modules=["htbcli"],
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.4",
        "click-shell>=2.1",
        "prettytable>=3.1.1",
        "PyHackTheBox>=0.5.4",
    ],
    entry_points={"console_scripts": ["htb = htbcli.cli:cli"]},
)
