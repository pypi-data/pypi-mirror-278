"""Model asset holder."""

import importlib
from typing import Generic

import ml_adapter.api.types as T

from ..assets import WithAssets
from .base import ModelAsset
from .dill import DillModelAsset
from .joblib import JoblibModelAsset
from .serialize import SelfSerializingModelAsset

ModelAssetTypeList = list[type[ModelAsset]]


class WithModel(WithAssets, Generic[T.MI]):
    """Holder of model assets.

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
    """

    MODEL_ASSET_CLASSES = [DillModelAsset, JoblibModelAsset, SelfSerializingModelAsset]
    DEFAULT_MODEL_PATH: str | None = "model.dill"
    MODEL_CLASS: type[T.MI] | None = None

    # TODO: move these attributes to the model asset.
    _model_path: str | None = None
    _model_is_dir: bool = False
    _model_class: type | None = None

    def __init__(
        self,
        model: T.MI | None = None,
        model_path: str | None = None,
        model_class: type[T.MI] | str | None = None,
        is_dir: bool = False,
        **kwargs,
    ):
        """Register the manifest asset classes."""
        super().__init__(**kwargs)
        self.assets.asset_classes.extend(self.MODEL_ASSET_CLASSES)
        self._model_path = model_path
        self._model_class = load_class(model_class)
        self._model_is_dir = is_dir
        if model:
            self.model = model
        self._init_model_asset()

    @property
    def model_class(self) -> type[T.MI] | None:
        """Return the current or supported model class."""
        if self._model_class:
            return self._model_class
        if self.model_asset.content:
            clazz = self.model.__class__
            if _is_allowed_model_clazz(clazz):
                return clazz
        if self.MODEL_CLASS:
            return self.MODEL_CLASS
        return None

    @property
    def model_path(self) -> str:
        """Model path."""
        if self._model_path:
            return self._model_path
        if self.DEFAULT_MODEL_PATH:
            return self.DEFAULT_MODEL_PATH
        patterns = ",".join(
            set(f"'{p}'" for ac in self.MODEL_ASSET_CLASSES for p in ac.PATH_INCLUDES)
        )
        raise AttributeError(
            "No default model_path provided. "
            f"Please provide a path that matches any of {patterns}"
        )

    def _init_model_asset(self):
        model_asset_class = self.assets.asset_class_for(
            self.model_path, is_dir=self._model_is_dir
        )
        if model_asset_class is None:
            raise TypeError(f"Model asset with path '{self.model_path}' not supported.")
        self.assets.add(
            model_asset_class,
            self.model_path,
            model_class=self._model_class or self.MODEL_CLASS,
        )

    @property
    def model_asset(self) -> ModelAsset:
        """The asset holding the model instance."""
        model_asset = self.assets.get(asset_type=ModelAsset)
        if model_asset is not None:
            return model_asset

        # lazy init
        self._init_model_asset()
        return self.assets.get_or_fail(asset_type=ModelAsset)

    @property
    def model(self) -> T.MI:
        """Get the model instance."""
        return self.model_asset.model

    @model.setter
    def model(self, model: T.MI):
        """Set the model instance."""
        if model is not None and _is_allowed_model_clazz(model.__class__):
            self._model_class = model.__class__
        self.model_asset.model = model


def load_class(spec: str | type | None) -> type | None:
    """Load a class by fully qualified module and class name."""
    if not isinstance(spec, str):
        return spec
    spec_els = spec.split(".")
    module_path = ".".join(spec_els[:-1])
    class_name = spec_els[-1]
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def class_fqn(clazz: type) -> str:
    """Render the fully qualified class name."""
    return f"{clazz.__module__}.{clazz.__name__}"


def _is_allowed_model_clazz(clazz: type) -> bool:
    """Return true if we can set the 'model_class' in the adapter to this value."""
    return clazz.__module__ not in ["builtins", "__main__"]
