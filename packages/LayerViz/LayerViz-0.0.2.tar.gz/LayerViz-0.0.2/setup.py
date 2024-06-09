

from setuptools import setup, find_packages
import codecs
import os

# Read the contents of the README file
def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()

VERSION = '0.0.2'
DESCRIPTION = 'A Python Library for Visualizing Keras Model that covers a variety of Layers'
LONG_DESCRIPTION = read('README.md')

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
