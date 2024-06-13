# waylay-ml-adapter-torch

Provides the `ml_adapter.sklearn` module as [Waylay ML Adapter](https://docs.waylay.io/#/api/sdk/python?id=ml_adapter) for [pytorch](https://pytorch.org/).


## Installation
```
pip install waylay-ml-adapter-torch
```

You might want to install additional libraries such as `torchaudio` or `torchvision`.


## Usage
This _ML Adapter_ uses the standard torch mechanisms to [save and load models](https://pytorch.org/tutorials/beginner/saving_loading_models.html#saving-and-loading-models) within a waylay _plugin_ or _webscript_.
The `model_path` argument defines the file name of the serialized model in the function archive:
* A `model_path` ending in `weights.pt` or `weights.pth` save/loads the model weights using its [state_dict](https://pytorch.org/tutorials/beginner/saving_loading_models.html#save-load-state-dict-recommended).
  It is a recommended, more robust method, but requires you to also specifiy a `model_class`.
* Any other `model_path` with `.pt` or `.pth` suffix save/loads the [entire model](https://pytorch.org/tutorials/beginner/saving_loading_models.html#save-load-entire-model).
  It implicitly saves (references to) the used model class. You'll have to make sure that all dependencies used are also included or declared in the archive. 
* You can also pass an instantiated the `model` directly to the adapter.


### Creating a model for a _webscript
```python
from ml_adapter.torch import V1TorchAdapter

# assuming we save a AutoEncoder torch.nn.Module class in a `autoencoder.py` file
from autoencoder import AutoEncoder
model = AutoEncoder()
# ... train the model ...

# a local directory to prepare the webscript archive
ARCHIVE_LOC='~/webscripts/autoencoder-pytorch'
# use a `weights` model path to use _weights_ serialization
MODEL_PATH='autoencoder.weights.pt'

adapter = V1TorchAdapter(
    model=model,
    model_path='model-weights.pt',
    location=ARCHIVE_LOC,
)

# add our model script to the webscript archive
await adapter.add_script('autoencoder.py')
# write the archive
await adapter.save()
# inspect the archive:
list(adapter.assets)
#> [requirements.txt <ml_adapter.base.assets.python.PythonRequirementsAsset>,
#> main.py <ml_adapter.base.assets.python.PythonScriptAsset>,
#> model-weights.pt <ml_adapter.torch.adapter.TorchModelWeightsAsset>,
#> autoencoder.py <ml_adapter.base.assets.python.PythonScriptAsset>]
```

Upload the adapter archive as webscript using the [`ml_tool` SDK plugin](https://pypi.org/project/waylay-ml-adapter-sdk/)
```
from waylay.sdk import WaylayClient
client = WaylayClient.from_profile('staging')
ref = await client.ml_tool.create_webscript(adapter, name='MyAutoEncoder', version='0.0.1')
ref = await client.ml_tool.wait_until_ready(ref)
await client.ml_tool.test_webscript(ref, [2,3,4])
```

The generated code in `main.py` uses the following to load your model:
```python
MODEL_PATH = os.environ.get('MODEL_PATH', 'model-weights.pt')
MODEL_CLASS = os.environ.get('MODEL_CLASS', 'autoencoder.AutoEncoder')
adapter = V1TorchAdapter(model_path=MODEL_PATH, model_class=MODEL_CLASS)
```
You can modify that loading mechanism, e.g. by creating the model your self, and providing it as
```
adapter = V1TorchAdapter(model=model)
```

## Exported classes

This module exports the following classes:

### `ml_adapter.torch.V1TorchAdapter`

> Adapts a callable with torch arrays as input and output.


### `ml_adapter.torch.V1TorchMarshaller`

> Convert v1 payload from and to torch tensors.



## See also

* [waylay-ml-adapter-sklearn](https://pypi.org/project/waylay-ml-adapter-sklearn/) _ML adapter_ for [scikit-learn](https://scikit-learn.org/stable/) models.
* [waylay-ml-adapter-sdk](https://pypi.org/project/waylay-ml-adapter-sdk/) provides the `ml_tool` extension to the [waylay-sdk](https://pypi.org/project/waylay-sdk/)
* [waylay-ml-adapter-base](https://pypi.org/project/waylay-ml-adapter-base/) provides the basic _ML adapter_ infrastructure.
* [waylay-ml-adapter-api](https://pypi.org/project/waylay-ml-adapter-api/) defines the remote data interfaces.
