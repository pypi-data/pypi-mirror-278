from setuptools import setup, find_packages

setup(
    name='graphmemory',
    version='0.2',
    author='BradAGI',
    author_email='cavemen_summary_0f@icloud.com',
    packages=find_packages(),
    url='https://github.com/bradAGI/GraphMemory',
    license='LICENSE.txt',
    description='A package for creating a hybrid graph / vector database for use with GraphRAG.',
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    install_requires=[
        'duckdb==1.0.0',
        'pydantic==2.7.3'
    ],
    keywords='graphrag graph database rag vector database'
)

