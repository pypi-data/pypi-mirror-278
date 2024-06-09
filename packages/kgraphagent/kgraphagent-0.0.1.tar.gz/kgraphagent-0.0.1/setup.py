from setuptools import setup, find_packages

setup(
    name='kgraphagent',
    version='0.0.1',
    author='Marc Hadfield',
    author_email='marc@vital.ai',
    description='KGraph Agent',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vital-ai/kgraphagent',
    packages=find_packages(exclude=["test", "test_output"]),
    license='Apache License 2.0',
    install_requires=[
            'requests>=2.31.0',
            'vital-ai-vitalsigns>=0.1.17',
            'vital-ai-domain>=0.1.4',
            'six',
            'pyyaml',
            'vital-ai-haley-kg>=0.1.4',
            'kgraphmemory>=0.0.5',
            'kgraphgen>=0.0.1',
            'rdflib==7.0.0',
            'SPARQLWrapper==2.0.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
