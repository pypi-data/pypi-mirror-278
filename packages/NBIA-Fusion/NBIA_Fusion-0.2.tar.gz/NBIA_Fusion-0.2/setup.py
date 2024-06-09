from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="NBIA_Fusion",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        # "numpy",
        # "torch",
        # "open3d",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
