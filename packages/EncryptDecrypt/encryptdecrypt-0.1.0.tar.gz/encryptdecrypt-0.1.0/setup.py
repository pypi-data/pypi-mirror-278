from setuptools import setup, find_packages

setup(
    name='EncryptDecrypt',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
    ],
    author='Shan Konduru',
    author_email='ShanKonduru@email.com',
    description='THis package encrypts and decrypts a string',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ShanKonduru/EncryptDecryptPy',
    license='MIT',
)

