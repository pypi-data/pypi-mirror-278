"""Setup file"""

from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='mpyez',
    version='0.0.4',
    packages=find_packages(where="src", exclude=['*tests*']),
    url='https://github.com/syedalimohsinbukhari/mpyez',
    license='MIT',
    author='Syed Ali Mohsin Bukhari, Astrophysics and Python',
    author_email='syedali.b@outlook.com, astrophysicsandpython@gmail.com',
    description='Common use utilities for python done easy.',
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">3.9, <3.12",
    # install_requires=["astropy~=4.3.1", "numpy~=1.21.6", "setuptools~=59.6.0",
    # "pillow~=9.1.1"],
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
)
