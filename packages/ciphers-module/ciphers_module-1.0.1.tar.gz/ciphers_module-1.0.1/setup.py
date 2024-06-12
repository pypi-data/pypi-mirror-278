from setuptools import setup, find_packages

VERSION = '1.0.1'
DESCRIPTION = 'Encrypt and Decrypt text'
LONG_DESCRIPTION = 'A package that allows encryption and decryption of text using methods.'

# Setting up
setup(
    name="ciphers-module",
    version=VERSION,
    author="Avyukt27",
    author_email="<avyukt.aggarwal007@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'cipher', 'encode', 'encrypt', 'decrypt', 'decode'],
)