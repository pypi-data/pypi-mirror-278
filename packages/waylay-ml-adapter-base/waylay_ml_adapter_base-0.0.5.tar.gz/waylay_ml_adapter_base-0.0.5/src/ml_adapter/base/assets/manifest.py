"""Utility functions for accessing a function manifest."""

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any, Literal, Self, Union

from .base import AssetsFolder
from .json import JsonAsset
from .mixin import WithAssets
from .python import PythonRequirementsAsset, PythonScriptAsset
from .script import default_plug_v1_script, default_webscript_script

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
    DEFAULT_MANIFEST: ManifestSpec | None = None
    FUNCTION_TYPE: FunctionType
    MERGE_SPEC: ManifestMergeSpec = {}

    def __init__(
        self, parent: AssetsFolder, manifest: ManifestSpec | None = None, **kwargs
    ):
        """Create the function manifest asset."""
        super().__init__(parent, **kwargs)
        if manifest:
            self.json = manifest
        elif self.DEFAULT_MANIFEST:
            self.json = json.loads(json.dumps(self.DEFAULT_MANIFEST))

    def merge(self, manifest: ManifestSpec) -> ManifestSpec:
        """Merge the existing manifest with new overrides."""
        self.json = merge_manifest(self.content, manifest, self.MERGE_SPEC)
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
        "webscript": default_webscript_script,
        "plug": default_plug_v1_script,
    }
    DEFAULT_MANIFEST: dict[FunctionType, ManifestSpec] = {
        "webscript": DEFAULT_WEBSCRIPT_MANIFEST_V1,
        "plug": DEFAULT_PLUG_MANIFEST_V1,
    }
    MAIN_SCRIPT_NAME = "main.py"

    def default_script(self, function_type: FunctionType = "plug") -> Callable:
        """Get a default main script for a webscript."""
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
        manifest: FunctionManifestAsset | None = None
        for asset in self.assets.iter(asset_type=FunctionManifestAsset):
            if asset.has_content():
                if manifest and manifest.has_content():
                    raise IndexError(
                        f"Multiple non empty manifest assets found:"
                        f" {[asset.path, manifest.path]}"
                    )
                manifest = asset
            manifest = manifest or asset
        if manifest is None:
            return self.assets.get_or_add(self.DEFAULT_MANIFEST_CLASS)
        return manifest

    def _assure_manifest_type(self, manifest_type: type[FunctionManifestAsset]):
        manifest_asset = self.manifest
        if manifest_asset is not None:
            if isinstance(manifest_asset, manifest_type):
                return manifest_asset
            # reset manifest and main script when switching manifest type
            manifest_asset.content = None
            script = self.assets.get(PythonScriptAsset, self.MAIN_SCRIPT_NAME)
            if script:
                script.content = None
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
        script_asset = self.assets.get_or_add(PythonScriptAsset, self.MAIN_SCRIPT_NAME)
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
        requirements_asset = self.assets.get_or_add(PythonRequirementsAsset)
        requirements_asset.add_default(*self.default_requirements())
        return self

    def as_webscript(self, manifest: ManifestSpec, **_kwargs) -> Self:
        """Make sure a webscript manifest is present."""
        return self._as_function(manifest, "webscript")

    def as_plug(self, manifest: ManifestSpec, **_kwargs) -> Self:
        """Make sure that a plug manifest is present."""
        return self._as_function(manifest, "plug")


def merge_manifest(
    default: ManifestSpec | None, overrides: ManifestSpec, paths: ManifestMergeSpec
) -> ManifestSpec:
    """Merge a default and override manifest, with deep merge at the indicated paths."""
    if default is None:
        return overrides
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
