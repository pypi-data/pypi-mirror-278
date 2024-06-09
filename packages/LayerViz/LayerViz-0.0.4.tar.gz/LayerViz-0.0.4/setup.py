

from setuptools import setup, find_packages
import codecs
import os




VERSION = '0.0.4'
DESCRIPTION = 'A Python Library for Visualizing Keras Model that covers a variety of Layers'
LONG_DESCRIPTION = """
# LayerViz

![logo (2)](https://raw.githubusercontent.com/swajayresources/imageresources/main/logo%20(2).png)

A Python Library for Visualizing Keras Models covering a variety of Layers.

## Table of Contents

<!-- TOC -->

* [Keras Visualizer](#LayerViz)
    * [Table of Contents](#table-of-contents)
    * [Installation](#installation)
        * [Install](#install)
        * [Upgrade](#upgrade)
    * [Usage](#usage)
    * [Parameters](#parameters)
    * [Settings](#settings)
    * [Sample Usage](#sample-usage)
    * [Supported layers](#supported-layers)

<!-- TOC -->

## Installation

## Install

Use python package manager (pip) to install Keras Visualizer.

```bash
pip install LayerViz
```

### Upgrade

Use python package manager (pip) to upgrade Keras Visualizer.

```bash
pip install LayerViz --upgrade
```

## Usage

```python


# create your model here
# model = ...

LayerViz(model, file_format='png')
```

## Parameters

```python
LayerViz(model, file_name='graph', file_format=None, view=False, settings=None)
```

- `model` : a Keras model instance.
- `file_name` : where to save the visualization.
- `file_format` : file format to save 'pdf', 'png'.
- `view` : open file after process if True.
- `settings` : a dictionary of available settings.

> **Note :**
> - set `file_format='png'` or `file_format='pdf'` to save visualization file.
> - use `view=True` to open visualization file.
> - use [settings](#settings) to customize output image.

## Settings

you can customize settings for your output image. here is the default settings dictionary:

```python
 recurrent_layers = ['LSTM', 'GRU']
    main_settings = {
        # ALL LAYERS
        'MAX_NEURONS': 10,
        'ARROW_COLOR': '#707070',
        # INPUT LAYERS
        'INPUT_DENSE_COLOR': '#2ecc71',
        'INPUT_EMBEDDING_COLOR': 'black',
        'INPUT_EMBEDDING_FONT': 'white',
        'INPUT_GRAYSCALE_COLOR': 'black:white',
        'INPUT_GRAYSCALE_FONT': 'white',
        'INPUT_RGB_COLOR': '#e74c3c:#3498db',
        'INPUT_RGB_FONT': 'white',
        'INPUT_LAYER_COLOR': 'black',
        'INPUT_LAYER_FONT': 'white',
        # HIDDEN LAYERS
        'HIDDEN_DENSE_COLOR': '#3498db',
        'HIDDEN_CONV_COLOR': '#5faad0',
        'HIDDEN_CONV_FONT': 'black',
        'HIDDEN_POOLING_COLOR': '#8e44ad',
        'HIDDEN_POOLING_FONT': 'white',
        'HIDDEN_FLATTEN_COLOR': '#2c3e50',
        'HIDDEN_FLATTEN_FONT': 'white',
        'HIDDEN_DROPOUT_COLOR': '#f39c12',
        'HIDDEN_DROPOUT_FONT': 'black',
        'HIDDEN_ACTIVATION_COLOR': '#00b894',
        'HIDDEN_ACTIVATION_FONT': 'black',
        'HIDDEN_LAYER_COLOR': 'black',
        'HIDDEN_LAYER_FONT': 'white',
        # RECURRENT LAYERS
        'RECURRENT_LAYER_COLOR': '#9b59b6',
        'RECURRENT_LAYER_FONT': 'white',
        # OUTPUT LAYER
        'OUTPUT_DENSE_COLOR': '#e74c3c',
        'OUTPUT_LAYER_COLOR': 'black',
        'OUTPUT_LAYER_FONT': 'white',
    }


    for layer_type in recurrent_layers:
      main_settings[layer_type + '_COLOR'] = '#9b59b6'
    settings = {**main_settings, **settings} if settings is not None else {**main_settings}
    max_neurons = settings['MAX_NEURONS']
```

**Note**:

* set `'MAX_NEURONS': None` to disable max neurons constraint.
* see list of color names [here](https://graphviz.org/doc/info/colors.html).

```python


my_settings = {
    'MAX_NEURONS': None,
    'INPUT_DENSE_COLOR': 'teal',
    'HIDDEN_DENSE_COLOR': 'gray',
    'OUTPUT_DENSE_COLOR': 'crimson'
}

# model = ...

LayerViz(model, file_format='png', settings=my_settings)
```
## Sample Usage 
📖 **Resource:** The architecture we're using below is a scaled-down version of [VGG-16](https://arxiv.org/abs/1505.06798), a convolutional neural network which came 2nd in the 2014 [ImageNet classification competition](http://image-net.org/).

For reference, the model we're using replicates TinyVGG, the computer vision architecture which fuels the [CNN explainer webpage](https://poloclub.github.io/cnn-explainer/).
```python
from keras import models, layers
import tensorflow as tf
model_1 = tf.keras.models.Sequential([
  tf.keras.layers.Conv2D(filters=10, 
                         kernel_size=3, # can also be (3, 3)
                         activation="relu", 
                         input_shape=(224, 224, 3)), # first layer specifies input shape (height, width, colour channels)
  tf.keras.layers.Conv2D(10, 3, activation="relu"),
  tf.keras.layers.MaxPool2D(pool_size=2, # pool_size can also be (2, 2)
                            padding="valid"), # padding can also be 'same'
  tf.keras.layers.Conv2D(10, 3, activation="relu"),
  tf.keras.layers.Conv2D(10, 3, activation="relu"), # activation='relu' == tf.keras.layers.Activations(tf.nn.relu)
  tf.keras.layers.MaxPool2D(2),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(1, activation="sigmoid") # binary activation output
])

LayerViz(model_1, file_name='sample1', file_format='png')

from IPython.display import Image
Image('sample1.png')
```
![download](https://raw.githubusercontent.com/swajayresources/imageresources/main/download.png)

## Supported layers

[Explore list of **keras layers**](https://keras.io/api/layers/)

1. Core layers
    - [x] Input object
    - [x] Dense layer
    - [x] Activation layer
    - [x] Embedding layer
    - [ ] Masking layer
    - [ ] Lambda layer

2. Convolution layers
    - [x] Conv1D layer
    - [x] Conv2D layer
    - [x] Conv3D layer
    - [x] SeparableConv1D layer
    - [x] SeparableConv2D layer
    - [x] DepthwiseConv2D layer
    - [x] Conv1DTranspose layer
    - [x] Conv2DTranspose layer
    - [x] Conv3DTranspose layer

3. Pooling layers
    - [x] MaxPooling1D layer
    - [x] MaxPooling2D layer
    - [x] MaxPooling3D layer
    - [x] AveragePooling1D layer
    - [x] AveragePooling2D layer
    - [x] AveragePooling3D layer
    - [x] GlobalMaxPooling1D layer
    - [x] GlobalMaxPooling2D layer
    - [x] GlobalMaxPooling3D layer
    - [x] GlobalAveragePooling1D layer
    - [x] GlobalAveragePooling2D layer
    - [x] GlobalAveragePooling3D layer

4. Reshaping layers
    - [ ] Reshape layer
    - [x] Flatten layer
    - [ ] RepeatVector layer
    - [ ] Permute layer
    - [ ] Cropping1D layer
    - [ ] Cropping2D layer
    - [ ] Cropping3D layer
    - [ ] UpSampling1D layer
    - [ ] UpSampling2D layer
    - [ ] UpSampling3D layer
    - [ ] ZeroPadding1D layer
    - [ ] ZeroPadding2D layer
    - [ ] ZeroPadding3D layer

5. Regularization layers
    - [x] Dropout layer
    - [x] SpatialDropout1D layer
    - [x] SpatialDropout2D layer
    - [x] SpatialDropout3D layer
    - [x] GaussianDropout layer
    - [ ] GaussianNoise layer
    - [ ] ActivityRegularization layer
    - [x] AlphaDropout layer

6. Recurrent Layers
    - [x] LSTM
    - [x] GRU
          

"""

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
