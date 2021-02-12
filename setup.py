"""
Setup script for the four package.
"""

import setuptools
import os


long_description = 'Unable to access README.md during setup!'
if os.path.exists('README.md'):
    with open('README.md', 'r') as readme:
        long_description = readme.read()

setuptools.setup(
    name='four',
    version='0.0',
    author='Kevin Turner',
    author_email='kct0004@auburn.edu',
    description='A module for calculating four-chains',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/KCATurner/four.git',
    packages=setuptools.find_packages(
        exclude=['tests*', ],
    ),
    install_requires=[
        'conwech',
    ],
    entry_points={
        'console_scripts': [
            'four = four.__main__:main',
        ],
    },
    python_requires='>=3.4',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
