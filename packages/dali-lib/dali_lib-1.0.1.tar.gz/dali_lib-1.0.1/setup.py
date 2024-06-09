from setuptools import setup, find_packages

setup(
    name = 'dali_lib',
    version = '1.0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'matplotlib'
    ]
)
