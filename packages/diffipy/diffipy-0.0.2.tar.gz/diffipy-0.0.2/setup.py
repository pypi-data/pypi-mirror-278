from setuptools import setup, find_packages

setup(
    name='diffipy',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    author='Daniel Roth',
    author_email='danielroth@posteo.eu',
    description='An interface to differentiation backends in Python..',
    long_description_content_type='text/markdown',
    url='https://github.com/da-roth/DiffiPy/src/',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
