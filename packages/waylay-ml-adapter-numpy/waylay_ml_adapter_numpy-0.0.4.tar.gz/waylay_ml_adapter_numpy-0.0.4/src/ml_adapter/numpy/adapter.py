"""Numpy ML adapter."""

import ml_adapter.api.types as T
import ml_adapter.base as A
from ml_adapter.api.data import v1 as V1
from ml_adapter.api.data.common import V1_PROTOCOL
from ml_adapter.base.assets.manifest import (
    default_plug_v1_script,
    default_webscript_script,
)

import numpy.typing as npt

from .marshall import V1NumpyMarshaller

NumpyModelInvoker = T.ModelInvoker[npt.ArrayLike, npt.ArrayLike]


NUMPY_REQUIREMENTS = [
    *A.WithManifest.DEFAULT_REQUIREMENTS,
    "numpy>=1.25.0",
    "waylay-ml-adapter-numpy",
    "dill",
    "joblib",
]


class V1NumpyModelAdapter(
    A.TensorModelAdapter[
        npt.ArrayLike,
        V1.V1Request,
        V1.V1PredictionResponse,
    ],
    A.WithModel[NumpyModelInvoker],
    A.WithPython,
    A.WithManifest,
    A.WithOpenapi,
):
    """Adapts a callable with numpy arrays as input and output."""

    DEFAULT_MARSHALLER = V1NumpyMarshaller
    PROTOCOL = V1_PROTOCOL
    DEFAULT_REQUIREMENTS = NUMPY_REQUIREMENTS
    DEFAULT_SCRIPT = {
        "webscript": default_webscript_script,
        "plug": default_plug_v1_script,
    }
