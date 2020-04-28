from setuptools import setup
from setuptools import find_packages

setup(
    name='pyform',
    version='0.1',
    description='Python formal languages library',
    url='https://github.com/dportin/pyform',
    author='Daniel Portin',
    author_email='portin.daniel@protonmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['bidict']
)   
