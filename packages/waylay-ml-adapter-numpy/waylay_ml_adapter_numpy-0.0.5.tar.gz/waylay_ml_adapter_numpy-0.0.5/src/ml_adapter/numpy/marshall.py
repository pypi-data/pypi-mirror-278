"""Numpy ML Marshaller."""

from collections.abc import Iterator, Mapping
from typing import Any, cast

import ml_adapter.base.marshall.v1.base as V1B
from ml_adapter.api import types as T
from ml_adapter.api.data import common as C
from ml_adapter.api.data import v1 as V1
from ml_adapter.base.marshall.v1 import list as V1L

import numpy as np
import numpy.typing as npt

NamedArrays = dict[str, npt.ArrayLike]
ArraysOrNamedArrays = npt.ArrayLike | NamedArrays

NUMPY_DATA_TYPES: dict[C.DataType, npt.DTypeLike] = {
    "BOOL": bool,
    "INT8": np.int8,
    "INT16": np.int16,
    "INT32": np.int32,
    "INT64": np.int64,
    "UINT8": np.uint8,
    "UINT16": np.uint16,
    "UINT32": np.uint32,
    "UINT64": np.uint64,
    "FP16": np.float16,
    "FP32": np.float32,
    "FP64": np.float64,
    "BYTES": np.object_,
}

V1_ENCODER = V1L.V1ScalarOrBytesEncoder()


def iter_decode_binary(value: Any) -> Iterator[bytes]:
    """Decode a base64 binary value."""
    if not isinstance(value, list):
        yield V1L.decode_binary(value)
        return
    evidence = value[0]
    if isinstance(evidence, str | dict):
        for v in value:
            yield V1L.decode_binary(v)
        return
    if isinstance(evidence, list):
        for v in value:
            yield from iter_decode_binary(v)
        return
    yield from value


def iter_flattened(value: C.Tensor) -> Iterator[C.Scalar]:
    """Iterate over a lists of lists."""
    if isinstance(value, list | Iterator):
        for v in value:
            yield from iter_flattened(v)
        return
    yield value


def _get_request_dtype(**kwargs) -> npt.DTypeLike | None:
    datatype = kwargs.get("datatype", "_")
    return NUMPY_DATA_TYPES.get(datatype)


class V1NumpyEncoding(V1B.WithV1TensorEncoding[npt.ArrayLike]):
    """Encoding and decoding of v1 tensors to numpy arrays."""

    def decode(
        self,
        value: V1.ValueOrTensor,
        dtype: npt.DTypeLike | None = None,
        datatype: str = C.DataTypes.DEFAULT,
    ) -> npt.ArrayLike:
        """Map a value tensor, decoding binary data."""
        if V1.is_binary(value, datatype):
            dtype = dtype or np.object_
            return np.fromiter(iter_decode_binary(value), dtype=dtype).reshape(
                np.shape(value)
            )
        return np.asarray(value, dtype=dtype)

    def encode(self, data: npt.ArrayLike, **kwargs) -> V1.ValueOrTensor:
        """Encode a numpy array to a value or tensor."""
        values = data.tolist()
        if V1.is_binary(values, **kwargs):
            wrap = kwargs.get("datatype") != C.DataTypes.BYTES
            return V1L.encode_binary(cast(C.BytesTensor, values), wrap=wrap)
        return cast(V1.ValueOrTensor, values)


class V1NumpyMarshaller(
    V1B.V1ValueOrDictRequestMarshallerBase[npt.ArrayLike],
    V1B.V1ValueOrDictResponseMarshallerBase[npt.ArrayLike],
    V1NumpyEncoding,
):
    """Converts v1 payload from and to numpy arrays."""

    def map_decoding_kwargs(
        self, parameters: C.Parameters, **kwargs
    ) -> Mapping[str, Any]:
        """Provide default for dtype."""
        dtype = kwargs.pop("dtype", _get_request_dtype(**kwargs))
        return super().map_decoding_kwargs(parameters, dtype=dtype, **kwargs)

    def map_named_instances(
        self, instances: list[V1.NamedValues], **kwargs
    ) -> ArraysOrNamedArrays:
        """Map named instances request."""
        return self.decode_named_values(instances, **kwargs)

    def map_response_data(
        self, response: ArraysOrNamedArrays, /, **kwargs
    ) -> V1.NamedValues:
        """Map model response to named values."""
        return self.encode_as_named(response, **kwargs)

    def decode_response(
        self, response: V1.V1PredictionResponse, /, **kwargs
    ) -> tuple[ArraysOrNamedArrays, T.Parameters | None]:
        """Decode a v1 inference response."""
        dtype = kwargs.pop("dtype", _get_request_dtype(**kwargs))
        return super().decode_response(response, dtype=dtype, **kwargs)

    def decode_named_values(
        self, response: list[V1.NamedValues], /, **kwargs
    ) -> ArraysOrNamedArrays:
        """Decode a V1 row-formatted response."""
        assert len(response) > 0
        dtype = _get_request_dtype(**kwargs)
        default_dtype = NUMPY_DATA_TYPES.get(self.DEFAULT_INPUT_DATA_TYPE, float)
        evidence = response[0]

        def _extract_np_from_dicts(key):
            shape = (len(response),) + np.shape(evidence[key])
            is_binary = V1.is_binary(evidence[key], **kwargs)
            np_dtype = dtype or (np.object_ if is_binary else default_dtype)
            flat_iter = iter_flattened(
                V1_ENCODER.decode(instance[key], **kwargs) for instance in response
            )
            return np.fromiter(flat_iter, dtype=np_dtype).reshape(shape)

        keys = evidence.keys()
        return {key: _extract_np_from_dicts(key) for key in keys}
