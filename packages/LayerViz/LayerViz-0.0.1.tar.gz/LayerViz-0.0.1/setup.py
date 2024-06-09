from setuptools import setup, find_packages
import codecs
import os
VERSION = '0.0.1'
DESCRIPTION = 'A Python Library for Visalizing Keras Model that covers a variety of Layers '
setup(
name="LayerViz",
version=VERSION,
author="Swajay Nandanwade",
author_email="swajaynandanwade@gmail.com",
description=DESCRIPTION,
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
