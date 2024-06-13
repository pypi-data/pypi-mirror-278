from setuptools import setup, find_packages

setup(
    name='quipudigital',
    version='0.1.0',
    description='Una biblioteca de visualización de Quipus con Python',
    url='https://github.com/jgomezz/quipudigital',
    package_data={'mathlib': ['assets/*.*']},  # Include all files in the assets folder
    author='jgomezz',
    packages=find_packages(),
)


