"""Torch ML adapter."""

import ml_adapter.api.types as T
import ml_adapter.base as A
import ml_adapter.base.model as M
from ml_adapter.api.data import v1 as V1
from ml_adapter.api.data.common import V1_PROTOCOL
from ml_adapter.base.assets import AssetsFolder
from ml_adapter.base.assets.manifest import (
    default_plug_v1_script,
    default_webscript_script,
)

import torch
from torch import nn

from .marshall import TorchTensor, V1TorchMarshaller

TorchModelInvoker = T.ModelInvoker[TorchTensor, TorchTensor]

TORCH_REQUIREMENTS = [
    *A.WithManifest.DEFAULT_REQUIREMENTS,
    "torch",
    "waylay-ml-adapter-torch",
]

TORCH_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


class TorchModelAsset(M.ModelAsset[nn.Module]):
    """Model asset for pytorch models (fully serialized)."""

    PATH_INCLUDES = ["*.pt", "*.pth"]
    DEFAULT_PATH = "model.pt"

    async def load_content(self, **kwargs):
        """Load a dill model."""
        with open(self.location, "rb") as f:
            model = torch.load(f)  # type: ignore
            # torch evaluation mode
            model.eval()
            model.to(TORCH_DEVICE)
            self.content = model

    async def save_content(self, **kwargs):
        """Save a dill model."""
        with open(self.location, "wb") as f:
            torch.save(self.content, f)


class TorchModelWeightsAsset(M.ModelAsset[nn.Module]):
    """Model asset for pytorch models (only weights serialized)."""

    PATH_INCLUDES = ["*weights.pt", "*weights.pth", "*Weights.pt", "*Weights.pth"]
    DEFAULT_PATH = "model_weights.pt"
    MODEL_CLASS: type[nn.Module] | None = None

    model_class: type[nn.Module]

    def __init__(
        self,
        parent: AssetsFolder,
        model_class: type[nn.Module] | None = None,
        **kwargs,
    ):
        """Create a model loading weights."""
        super().__init__(parent, **kwargs)
        model_class = model_class or self.MODEL_CLASS
        if not model_class:
            raise TypeError(
                'Loading a torch model using weights requires a "model_class" argument.'
            )
        self.model_class = model_class

    async def load_content(self, **kwargs):
        """Load a dill model."""
        with open(self.location, "rb") as f:
            weights = torch.load(f)  # type: ignore
            model = self.model_class()
            model.load_state_dict(weights)
            model.eval()
            model.to(TORCH_DEVICE)
            # torch evaluation mode
            self.content = model

    async def save_content(self, **kwargs):
        """Save a dill model."""
        model = self.content
        if model is None:
            return
        with open(self.location, "wb") as f:
            torch.save(model.state_dict(), f)


class V1TorchAdapter(
    A.TensorModelAdapter[
        TorchTensor,
        V1.V1Request,
        V1.V1PredictionResponse,
    ],
    A.WithModel[TorchModelInvoker],
    A.WithPython,
    A.WithManifest,
    A.WithOpenapi,
):
    """Adapts a callable with torch arrays as input and output."""

    DEFAULT_MARSHALLER = V1TorchMarshaller
    MODEL_ASSET_CLASSES = [TorchModelWeightsAsset, TorchModelAsset]
    DEFAULT_MODEL_PATH = "model.pt"
    PROTOCOL = V1_PROTOCOL
    DEFAULT_REQUIREMENTS = TORCH_REQUIREMENTS
    DEFAULT_SCRIPT = {
        "webscript": default_webscript_script,
        "plug": default_plug_v1_script,
    }

    @property
    def invoker(self) -> T.ModelInvoker:
        """Natively invoke the torch model without gradients calculation."""
        return torch.no_grad(super().invoker)
