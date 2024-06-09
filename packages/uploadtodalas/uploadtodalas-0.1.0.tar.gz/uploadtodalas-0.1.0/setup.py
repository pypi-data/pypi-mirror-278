from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='uploadtodalas',  
    version='0.1.0', 
    author='Dalas', 
    author_email='email@uploadgroup.site', 
    description='A package for uploading files to Dalas service', 
    long_description=long_description,  
    long_description_content_type='text/markdown',  
    url='https://api.uploadgroup.site/docs', 
    packages=find_packages(),  
    install_requires=[
        'aiohttp>=3.7.4',  
        'loguru>=0.5.3',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)
