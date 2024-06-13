from setuptools import setup, find_packages

setup(
    name='quipudigital',
    version='0.1.4',
    package_data={'quipudigital': ['assets/*.*']},  # Include all files in the assets folder
    packages=find_packages(),
    author='Jaime Gomez',
    author_email="jgomezz@gmail.com",
    description='Una biblioteca de visualización de Quipus con Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jgomezz/quipudigital',

)


