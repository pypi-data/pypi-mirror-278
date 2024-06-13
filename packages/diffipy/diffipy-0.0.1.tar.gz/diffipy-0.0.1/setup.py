from setuptools import setup, find_packages
import os

# Determine the directory of setup.py
base_dir = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(base_dir, '..\..', 'README.md')

# Read the contents of your README file for the long description
with open(readme_path, 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='diffipy',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    author='Daniel Roth',
    author_email='danielroth@posteo.eu',
    description='DiffiPy offers a versatile interface to multiple automatic (adjoint) differentiation (AAD) backends in Python. It utilizes a syntax inspired by numpy, ensuring straightforward integration and enhanced computational graph analysis.',
    long_description_content_type='text/markdown',
    url='https://github.com/da-roth/DiffiPy/src/',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
