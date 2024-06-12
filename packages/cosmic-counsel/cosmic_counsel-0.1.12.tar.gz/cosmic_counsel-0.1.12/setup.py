from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cosmic-counsel',
    version='0.1.12',
    author='Collin Paran, Eric Willis',
    url='https://www.boozallen.com/',
    description='Space R&D',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={"cosmic_counsel": ["models/*", "data/*.json", "data/*.pkl"]},
    entry_points={
        'console_scripts': [
            'cosmic-counsel=cosmic_counsel.__main__:main',
        ],
    },
    install_requires=[
        'torch==2.3.0+cu121',
        'transformers==4.41.2',
        'mdurl==0.1.2',
        'numpy==1.25.2',
        'h5py==3.9.0',
        'pandas==2.0.3',
        'uvicorn==0.30.1',
        'bitsandbytes==0.43.1',
        'accelerate==0.31.0',
        'sentence-transformers==3.0.1',
        'nltk==3.8.1',
        'PyPDF2==3.0.1',
        'pydantic==2.7.3',
        'requests==2.31.0',
        'tensorflow==2.15.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='Apache 2.0',
)
