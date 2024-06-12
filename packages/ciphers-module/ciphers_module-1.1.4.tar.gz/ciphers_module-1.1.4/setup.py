from setuptools import setup, find_packages

VERSION = '1.1.4'

with open("README.md", "r") as f:
    long_description = f.read()

# Setting up
setup(
    name="ciphers_module",
    version=VERSION,
    author="Avyukt27",
    author_email="<avyukt.aggarwal007@gmail.com>",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'cipher', 'encode', 'encrypt', 'decrypt', 'decode'],
)