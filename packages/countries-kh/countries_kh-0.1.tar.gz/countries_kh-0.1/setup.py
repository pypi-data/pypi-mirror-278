# country_package/setup.py

from setuptools import setup, find_packages

setup(
    name='countries_kh',
    version='0.1',
    author='Bharath Reddy',
    description='A package to get Ids of countries',
    packages=find_packages(),
    install_requires=[],  # Add any dependencies here
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
