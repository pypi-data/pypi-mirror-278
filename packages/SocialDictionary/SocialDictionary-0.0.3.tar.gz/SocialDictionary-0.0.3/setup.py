from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'This package is used to analyse sentiment, and emojis are also included in this sentiment analysis. The package uses a pre-trained model to assign an emotion to the emojis '

with open('README.md', 'r') as arq:
	readme = arq.read()

# Setting up
setup(
    name="SocialDictionary",
    version=VERSION,
    author="Goncalo Silva",
    author_email="gresi2001@gmail.com",
    description=DESCRIPTION,
    long_description = readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={
        'SocialDictionary': ['Dados/*']
    },
    install_requires=[
        'pandas',
        'nltk',
	'emoji',
	'googletrans'
    ],
    keywords=['python', 'text', 'EmoRoBERTa','sentiment analysis', 'emojis'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
