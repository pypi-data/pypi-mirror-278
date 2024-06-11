"""Utility functions for accessing a function manifest."""

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any, Literal, Self, Union

from .base import AssetsFolder
from .cached import CachedFileAsset
from .json import JsonAsset
from .mixin import WithAssets
from .python import PythonRequirementsAsset

WEBSCRIPT_MANIFEST_NAME = "webscript.json"
PLUG_MANIFEST_NAME = "plug.json"

ManifestSpec = dict[str, Any]
ManifestMergeSpec = dict[str, Union[str, "ManifestMergeSpec"]]

PLUG_MERGE_SPEC: ManifestMergeSpec = {
    "interface": {
        "states": "REPLACE",
        "input": "OVERWRITE_BY_NAME",
        "output": "OVERWRITE_BY_NAME",
    },
    "metadata": {
        "tags": "OVERWRITE_BY_NAME",
        "documentation": {
            "states": "REPLACE",
            "input": "OVERWRITE_BY_NAME",
            "output": "OVERWRITE_BY_NAME",
        },
    },
}


FunctionType = Literal["webscript"] | Literal["plug"]


class FunctionManifestAsset(JsonAsset):
    """An asset that represents a function manifest."""

    PATH_INCLUDES = []
    DEFAULT_MANIFEST: ManifestSpec = {"version": "0.0.1"}
    FUNCTION_TYPE: FunctionType
    MERGE_SPEC: ManifestMergeSpec = {}

    def __init__(
        self, parent: AssetsFolder, manifest: ManifestSpec | None = None, **kwargs
    ):
        """Create the function manifest asset."""
        super().__init__(parent, **kwargs)
        manifest = manifest or {**self.DEFAULT_MANIFEST}
        self.json = manifest

    def merge(self, manifest: ManifestSpec) -> ManifestSpec:
        """Merge the existing manifest with new overrides."""
        self.json = merge_manifest(self.json, manifest, self.MERGE_SPEC)
        return self.json


def _read_json(name: str):
    location = Path(__file__).parent.joinpath(name)
    with open(location, encoding="utf-8") as f:
        return json.load(f)


DEFAULT_PLUG_MANIFEST_V1 = _read_json("default.v1.plug.json")
DEFAULT_PLUG_MANIFEST_V2 = _read_json("default.v2.plug.json")
DEFAULT_WEBSCRIPT_MANIFEST_V1 = _read_json("default.v1.webscript.json")


class WebscriptManifestAsset(FunctionManifestAsset):
    """An asset that represents the webscript manifest."""

    FUNCTION_TYPE = "webscript"
    DEFAULT_PATH = WEBSCRIPT_MANIFEST_NAME
    PATH_INCLUDES = [DEFAULT_PATH]


class PlugManifestAsset(FunctionManifestAsset):
    """An asset that represents the webscript manifest."""

    FUNCTION_TYPE = "plug"
    DEFAULT_PATH = PLUG_MANIFEST_NAME
    PATH_INCLUDES = [DEFAULT_PATH]
    MERGE_SPEC: ManifestMergeSpec = PLUG_MERGE_SPEC


def no_script(adapter: type, **kwargs):
    """Produce a placeholder script."""
    return """
# Script not provided, please use the correct ML Adapter.
"""


class WithManifest(WithAssets):
    """Mixin for a configuration that has a waylay _function_ manifest file and script.

    Adds methods to a `WithAssets` adapter to manage the function _manifest_ of
    waylay _plugin_ or _webscript_.

    * `manifest` returns the manifest asset of the function archive
        at `plug.json` or `webscript.json`.
    * `as_webscript()` initializes the manifest
        and script for a _webscript_ that uses an ML Adapter.
    * `as_plug()` initializes the manifest and script for
        a rule _plugin_ that uses an ML Adapter.
    """

    MANIFEST_ASSET_CLASSES = [WebscriptManifestAsset, PlugManifestAsset]
    DEFAULT_MANIFEST_CLASS = WebscriptManifestAsset
    DEFAULT_REQUIREMENTS = ["starlette"]
    DEFAULT_SCRIPT: dict[FunctionType, Callable] = {
        "webscript": no_script,
        "plug": no_script,
    }
    DEFAULT_MANIFEST: dict[FunctionType, ManifestSpec] = {
        "webscript": DEFAULT_WEBSCRIPT_MANIFEST_V1,
        "plug": DEFAULT_PLUG_MANIFEST_V1,
    }

    def default_script(self, function_type: FunctionType = "plug") -> Callable:
        """Get a default main.py script for a webscript."""
        return self.DEFAULT_SCRIPT[function_type]

    def default_requirements(self) -> list[str]:
        """Get the default requirements for this archive."""
        return self.DEFAULT_REQUIREMENTS

    def default_manifest(self, function_type: FunctionType = "plug") -> ManifestSpec:
        """Get a default manifest for this archive."""
        return self.DEFAULT_MANIFEST[function_type]

    def __init__(
        self,
        manifest_path: str | None = None,
        manifest: ManifestSpec | None = None,
        **kwargs,
    ):
        """Register the manifest asset classes."""
        super().__init__(**kwargs)
        self.assets.asset_classes.extend(self.MANIFEST_ASSET_CLASSES)
        asset_class = WebscriptManifestAsset
        if manifest_path:
            asset_class = (
                self.assets.asset_class_for(manifest_path, is_dir=False) or asset_class
            )
        self.assets.add(asset_class, manifest_path, manifest=manifest, **kwargs)

    @property
    def manifest(self) -> FunctionManifestAsset:
        """The manifest of the function that uses this adapter."""
        return self.assets.get_or_fail(asset_type=FunctionManifestAsset)

    def _assure_manifest_type(self, manifest_type: type[FunctionManifestAsset]):
        manifest_asset = self.assets.get(asset_type=FunctionManifestAsset)
        if manifest_asset is not None and not isinstance(manifest_asset, manifest_type):
            self.assets.children.remove(manifest_asset)
            manifest_asset = None
        if manifest_asset is None:
            manifest_asset = self.assets.add(manifest_type, manifest_type.DEFAULT_PATH)
        return manifest_asset

    def _as_function(self, manifest: ManifestSpec, function_type: FunctionType) -> Self:
        # switch function type if neccessary
        manifest_asset = self._assure_manifest_type(
            WebscriptManifestAsset
            if function_type == "webscript"
            else PlugManifestAsset
        )
        manifest_asset.merge(self.default_manifest(function_type))
        manifest_asset.merge(manifest)
        # default script (no not overwrite existing script)
        script_asset = self.assets.get_or_fail(CachedFileAsset, "main.py")
        model_path = None
        model_class = None
        from ..model import WithModel

        if isinstance(self, WithModel):
            model_path = self.model_path
            model_class = self.model_class
        if not script_asset.content:
            script_asset.content = self.default_script(function_type)(
                self.__class__,
                model_path=model_path,
                model_class=model_class,
            )
        # update default requirements (do not overwrite existing deps)
        requirements_asset = self.assets.get_or_fail(PythonRequirementsAsset)
        requirements_asset.add_default(*self.default_requirements())
        return self

    def as_webscript(self, manifest: ManifestSpec, **_kwargs) -> Self:
        """Make sure a webscript manifest is present."""
        return self._as_function(manifest, "webscript")

    def as_plug(self, manifest: ManifestSpec, **_kwargs) -> Self:
        """Make sure that a plug manifest is present."""
        return self._as_function(manifest, "plug")


def default_webscript_script(
    adapter_class: type, model_path=None, model_class=None
) -> str:
    """Get a default model loading script for webscripts."""
    adapter_fqn = f"{adapter_class.__module__}.{adapter_class.__name__}"
    model_class_ref = (
        f"'{model_class.__module__}.{model_class.__name__}'" if model_class else "None"
    )
    model_path_ref = f"'{model_path}'" if model_path else "None"
    return f"""
# {adapter_fqn} model adapter
import os
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from {adapter_class.__module__} import {adapter_class.__name__}

MODEL_PATH = os.environ.get('MODEL_PATH', {model_path_ref})
MODEL_CLASS = os.environ.get('MODEL_CLASS', {model_class_ref})

# Initialize the model adapter.
# Provide a `model` argument if you want to create/load the model yourself.
adapter = {adapter_class.__name__}(
    model_path=MODEL_PATH, model_class=MODEL_CLASS
)

# Webscript handler
async def execute(request: Request):
    if request.method == 'GET':
        return JSONResponse(adapter.openapi)
    if request.method != 'POST':
        raise HTTPException(
            status_code=405,
            detail='This webscript only accepts `POST` calls.',
        )
    # use request body as input
    request_json = await request.json()
    # call the model adapter using the V1
    response_json = await adapter.call(request_json)
    return JSONResponse(response_json)
"""


def default_plug_v1_script(
    adapter_class: type,
    model_path: str | None = None,
    model_class: type | None = None,
    state_ok="PREDICTED",
    state_nok="FAILED",
) -> str:
    """Get a default model loading script for plugs."""
    adapter_fqn = f"{adapter_class.__module__}.{adapter_class.__name__}"
    model_class_ref = (
        f"'{model_class.__module__}.{model_class.__name__}'" if model_class else "None"
    )
    model_path_ref = f"'{model_path}'" if model_path else "None"
    return f"""
# {adapter_fqn} model adapter
import os
from ml_adapter.api.data import v1 as V1
from {adapter_class.__module__} import {adapter_class.__name__}

# optional type alias for plug response
StatusAndRawData = tuple[str, V1.V1PredictionResponse|V1.V1ErrorResponse]

STATE_OK = '{state_ok}'
STATE_NOK = '{state_nok}'

MODEL_PATH = os.environ.get('MODEL_PATH', {model_path_ref})
MODEL_CLASS = os.environ.get('MODEL_CLASS', {model_class_ref})

# Initialize the model adapter.
# Provide a `model` argument if you want to create/load the model yourself.
adapter = {adapter_class.__name__}(
    model_path=MODEL_PATH, model_class=MODEL_CLASS
)

async def execute(properties: V1.V1Request, console, logger) -> StatusAndRawData:
    try:
        result = await adapter.call(properties)
        return (STATE_OK, result)
    except Exception as err:
        logger.exception(err)
        error_message = str(err)
        console.error(error_message)
        return (STATE_NOK, {{ 'error': error_message, 'predictions': [] }})
"""


def merge_manifest(
    default: ManifestSpec, overrides: ManifestSpec, paths: ManifestMergeSpec
) -> ManifestSpec:
    """Merge a default and override manifest, with deep merge at the indicated paths."""
    merged = {**default, **overrides}
    for key, paths_at_key in paths.items():
        if key in overrides and key in default:
            if isinstance(paths_at_key, dict):
                merged[key] = merge_manifest(default[key], overrides[key], paths_at_key)
            if paths_at_key == "UNION":
                merged[key] = list(set(default[key]).union(overrides[key]))
            if paths_at_key == "OVERWRITE_BY_NAME":
                merged[key] = list(
                    merge_manifest(
                        {val["name"]: val for val in default[key]},
                        {val["name"]: val for val in overrides[key]},
                        {},
                    ).values()
                )
    return merged
