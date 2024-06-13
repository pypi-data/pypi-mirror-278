from setuptools import setup, find_packages

setup(
    name='quipudigital',
    version='0.1.2',
    package_data={'mathlib': ['assets/*.*']},  # Include all files in the assets folder
    packages=find_packages(),
    author='jgomezz',
    author_email="jgomezz@gmail.com",
    description='Una biblioteca de visualización de Quipus con Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jgomezz/quipudigital',
    
)


