from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='carbon-registry-indexer',
    version='0.1.39',
    license='MIT',
    description='A Python library designed to streamline the aggregation of carbon data from multiple registries, each with its own data format, into a unified schema in CSV/Parquet formats.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/CarbonMarketsHQ/Carbon-Registry-Indexer', 
    download_url='https://github.com/CarbonMarketsHQ/Carbon-Registry-Indexer/archive/refs/tags/v_0.1.7.tar.gz',
    author='Gautam P',
    author_email='gautam@carbonmarketshq.com',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy',
        'pandas',
        'openpyxl',
        'strawberry-graphql',
        'azure-storage-blob'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
)
