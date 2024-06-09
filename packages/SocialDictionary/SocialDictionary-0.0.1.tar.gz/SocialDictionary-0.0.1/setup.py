from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Sentiment analysis including emojis'

# Setting up
setup(
    name="SocialDictionary",
    version=VERSION,
    author="Goncalo Silva",
    author_email="gresi2001@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    package_data={
        'SocialDictionary': ['Dados/*']
    },
    install_requires=[
        'pandas',
        'nltk',
    ],
    keywords=['python', 'sentiment analysis', 'emojis'],
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
