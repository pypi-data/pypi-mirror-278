from setuptools import setup, find_packages

setup(
    name = 'dali_lib',
    version = '0.2',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'matplotlib'
    ]
)
