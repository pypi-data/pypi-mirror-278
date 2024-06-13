# waylay-ml-adapter-numpy

This provides the `ml_adapter.numpy` module as [Waylay ML Adapter](https://docs.waylay.io/#/api/sdk/python?id=ml_adapter) for models that use numpy as data representation.

This `waylay-ml-adapter-numpy` module provides marshalling for (custom) models that use [numpy](https://numpy.org/) as native data representation.

```
pip install waylay-ml-adapter-numpy
```

## Exported classes

This module exports the following classes:

### `ml_adapter.numpy.V1NumpyModelAdapter`

> Adapts a callable with numpy arrays as input and output.


### `ml_adapter.numpy.V1NumpyMarshaller`

> Converts v1 payload from and to numpy arrays.

