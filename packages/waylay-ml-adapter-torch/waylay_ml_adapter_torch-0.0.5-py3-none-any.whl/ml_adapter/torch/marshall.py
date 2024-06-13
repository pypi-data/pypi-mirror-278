"""Pytorch ML Marshaller."""

import ml_adapter.base.marshall.v1.base as V1B
import numpy.typing as npt
from ml_adapter.api.data import common as C
from ml_adapter.api.data import v1 as V1
from ml_adapter.numpy.marshall import V1NumpyEncoding

import torch

TorchTensor = torch.Tensor
NamedArrays = dict[str, TorchTensor]
ArraysOrNamedArrays = TorchTensor | NamedArrays

TORCH_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
TORCH_DEFAULT_DTYPE = "float32"


class V1TorchEncoding(V1B.WithV1TensorEncoding[TorchTensor]):
    """Encoding and decoding of v1 tensors to pytorch arrays."""

    _numpy = V1NumpyEncoding()

    def decode(
        self,
        value: V1.ValueOrTensor,
        dtype: npt.DTypeLike | None = TORCH_DEFAULT_DTYPE,
        datatype: str = C.DataTypes.DEFAULT,
        **kwargs,
    ) -> TorchTensor:
        """Map a value tensor, decoding binary data."""
        return torch.from_numpy(self._numpy.decode(value, dtype, datatype)).to(
            TORCH_DEVICE
        )

    def encode(self, data: TorchTensor, **kwargs) -> V1.ValueOrTensor:
        """Encode a pytorch array to a value or tensor."""
        force = kwargs.pop("force", False)
        return self._numpy.encode(data.detach().numpy(force=force), **kwargs)


class V1TorchMarshaller(
    V1B.V1ValueOrDictRequestMarshallerBase[TorchTensor],
    V1B.V1ValueOrDictResponseMarshallerBase[TorchTensor],
    V1TorchEncoding,
):
    """Convert v1 payload from and to torch tensors."""
