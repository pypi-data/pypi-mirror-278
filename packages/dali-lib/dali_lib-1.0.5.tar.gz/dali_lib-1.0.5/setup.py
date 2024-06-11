from setuptools import setup, find_packages

description = None

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name = 'dali_lib',
    version = '1.0.5',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'matplotlib',
        'jinja2'
    ],

    long_description_content_type='text/markdown',
    long_description=description,
)
