from setuptools import setup, find_packages

setup(
    name="GazooResearchUtils",
    version="1.5.9",
    description="Analysis of GazooResearch Data",
    package_dir={"":"app"},
    packages=find_packages(where="app"),
    url="https://gazooresearch.com/",
    author='Andrew Lim MD, Megan Lim MD, Christopher Lim MD, Robert Lim MD',
    install_requires=["lifelines >= 0.28.0"],
    python_requires=">=3.10"
)
