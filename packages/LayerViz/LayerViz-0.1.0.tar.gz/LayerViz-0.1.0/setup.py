

from setuptools import setup, find_packages
import codecs
import os


with open("README (1).md", "r") as fh:
    long_description = fh.read()


VERSION = '0.1.0'
DESCRIPTION = 'A Python Library for Visualizing Keras Model that covers a variety of Layers'
LONG_DESCRIPTION = long_description

setup(
    name="LayerViz",
    version=VERSION,
    author="Swajay Nandanwade",
    author_email="swajaynandanwade@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',  # This is important if your README is in markdown
    packages=find_packages(),
    install_requires=['graphviz'],
    keywords=['python', 'keras', 'visualize', 'models', 'layers'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
