# waylay-ml-adapter-base

Provides the `ml_adapter.base` module for the [Waylay ML Adapter](https://docs.waylay.io/#/api/sdk/python?id=ml_adapter) solution.

To use an _ML Adapter_ in a Waylay _plugin_ or _webscript_, use the adapter relevant to your machine learning framework:
* [waylay-ml-adapter-numpy](https://pypi.org/project/waylay-ml-adapter-numpy/) for generic models that use [numpy](https://numpy.org/) data representation
* [waylay-ml-adapter-sklearn](https://pypi.org/project/waylay-ml-adapter-sklearn/) for [scikit-learn](https://scikit-learn.org/stable/) models.
* [waylay-ml-adapter-torch](https://pypi.org/project/waylay-ml-adapter-torch/) for [pytorch](https://pytorch.org/) models.

This `waylay-ml-adapter-base` module provides the framework for these adapters.
Only if you would need to create an adapter utility for another
framework, you would install this module separately:

```
pip install waylay-ml-adapter-base
```

## Exported classes

This module exports the following classes:

### `ml_adapter.base.ModelAdapter`

> Model Adapter base.

Provides the basic contract for exposing
a model to a waylay _plugin_ or _webscript_.
* delegates to a `marshaller` to map the remote,
  json-compatible python data structures
  from and to the native tensor data structures for the ML framework.
* delegates to a `invoker` to find the model method to be called
* the `call` method maps remote requests and invokes the model method
* the `call_remote` method tests the round trip serialization, encoding
  native data request to remotable and back before invoking `call`



### `ml_adapter.base.TensorModelAdapter`

> Model adapter that uses (dicts of) tensors as inputs and outputs.

Requests are mapped to the model invocation using named parameters,
falling back to mapping the "main" entry to the first positional parameter.



### `ml_adapter.base.WithAssets`

> Mixin for a configuration backed by assets.

Manages _assets_ of the the _plugin_ or _webscript_.

Used read-only within a deployed _adapter_ to e.g. load the model definition.

Used read/write within the `ml_tool` to edit
the assets of a _plugin_ or _webscript_.



### `ml_adapter.base.WithManifest`

> Mixin for a configuration that has a waylay _function_ manifest file and script.

Adds methods to a `WithAssets` adapter to manage the function _manifest_ of
waylay _plugin_ or _webscript_.

* `manifest` returns the manifest asset of the function archive
    at `plug.json` or `webscript.json`.
* `as_webscript()` initializes the manifest
    and script for a _webscript_ that uses an ML Adapter.
* `as_plug()` initializes the manifest and script for
    a rule _plugin_ that uses an ML Adapter.



### `ml_adapter.base.WithOpenapi`

> Mixin for a configuration that has an openapi description.

Adds methods to a `WithAssets` adapter to manage the
openapi description of waylay _plugin_ or _webscript_.

* `openapi` returns an asset of type `OpenApiAsset` (normally at `openapi.json`)




### `ml_adapter.base.WithPython`

> Handles assets specific to python-based functions.

* `requirements` handles the dependency file (at `requirements.txt`)
* `lib` handles the libraries that are uploaded with
   the function archive itself. (at `lib/*.tar.gz`)
* `main_script` handles the main script of the function (`main.py`)
* `scripts` handles other utility scripts of the function (`*.py`)



### `ml_adapter.base.WithModel`

> Holder of model assets.

Adds methods to a `WithAssets` adapter to manage the model instance.
A model can either be:
* given as `model` in the constructor of the adapter
* loaded from `model_path` in the assets
* loades from `model_path` using a `model_class`

The `MODEL_ASSET_CLASSES` configured on the adapter
define the methods to load a model.
Defaults are
* `DillModelAsset`
* `JoblibModelAsset`
* `SelfSerializingModelAsset`



### `ml_adapter.base.SelfSerializingModelAsset`

> Model asset with own serialization methods.

Reads/writes the model from `model.sav` using the `save` and `load` methods
defined on the `model_class`.



### `ml_adapter.base.DillModelAsset`

> Model asset for dill-serialized models.

Reads/writes the model from paths like `model.dill`, `model.pkl`, `model.pickle`
using [dill](https://pypi.org/project/dill/) serialisation.



### `ml_adapter.base.JoblibModelAsset`

> Model asset with joblib serialization.

Reads/writes the model from `model.joblib` or `model.joblib.gz`
using [joblib](https://pypi.org/project/joblib/) serialisation.



### `ml_adapter.base.Marshaller`

> Abstract base class to marshall inference requests and responses.

Methods used to invoke the model in a _plugin_ or _webscript_:
* `map_request()` maps remote requests (generic type `RREQ`)
to native requests (generic type `MREQ`)
* `map_response()` maps native responses (generic type `MRES`)
to remote a response (generic type `RRES`)

Methods used to test roundtrip encoding in a client:
* `encode_request()` encodes a native request
to a remote request that can be sent to a waylay function.
* `decode_response()` decodes a remote response from a function
to native a response.



