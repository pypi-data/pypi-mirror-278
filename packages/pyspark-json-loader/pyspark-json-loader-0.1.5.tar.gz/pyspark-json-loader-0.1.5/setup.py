from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pyspark-json-loader',
    version='0.1.5',  # Increment the version number
    packages=find_packages(),
    install_requires=[
        'pyspark',
        'py4j',
    ],
    author='Chaudary Atif Raza Warraich',
    author_email='atifr454@gmail.com',
    description='A package to load and preprocess JSON data using PySpark',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AtifChaudary/pyspark-json-loader',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
