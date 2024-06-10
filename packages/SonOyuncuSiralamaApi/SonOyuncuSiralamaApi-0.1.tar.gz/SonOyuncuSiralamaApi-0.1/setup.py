from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='SonOyuncuSiralamaApi',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)
