from setuptools import setup, find_packages

VERSION = '0.1' 
DESCRIPTION = 'kinyarwanda keywords extractor'
LONG_DESCRIPTION = 'Packages for extracting keywords from kinyarwanda text'

# Setting up
setup(
        name="nijas_keywords_extractor", 
        version=VERSION,
        author="Janvier Niyitegeka",
        author_email="nijas2012@yahoo.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pandas','numpy','yake'],
        requires_python = ">=3.10.9",
        keywords=['python', 'kinyarwanda','keywords'],
        classifiers= [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ]
)