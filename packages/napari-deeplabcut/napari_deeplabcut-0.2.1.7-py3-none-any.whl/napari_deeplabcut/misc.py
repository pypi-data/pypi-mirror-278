from __future__ import annotations

import os
from enum import Enum, EnumMeta
from itertools import cycle
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
from napari.utils import colormaps


def find_project_config_path(labeled_data_path: str) -> str:
    return str(Path(labeled_data_path).parents[2] / "config.yaml")


def is_latest_version():
    import json
    import urllib.request
    from napari_deeplabcut import __version__

    url = "https://pypi.org/pypi/napari-deeplabcut/json"
    contents = urllib.request.urlopen(url).read()
    latest_version = json.loads(contents)["info"]["version"]
    return __version__ == latest_version, latest_version



def unsorted_unique(array: Sequence) -> np.ndarray:
    """Return the unsorted unique elements of an array."""
    _, inds = np.unique(array, return_index=True)
    return np.asarray(array)[np.sort(inds)]


def encode_categories(
    categories: List[str], return_map: bool = False
) -> Union[List[int], Tuple[List[int], Dict]]:
    unique_cat = unsorted_unique(categories)
    map_ = dict(zip(unique_cat, range(len(unique_cat))))
    inds = np.vectorize(map_.get)(categories)
    if return_map:
        return inds, map_
    return inds


def merge_multiple_scorers(
    df: pd.DataFrame,
) -> pd.DataFrame:
    n_frames = df.shape[0]
    header = DLCHeader(df.columns)
    n_scorers = len(header._get_unique("scorer"))
    if n_scorers == 1:
        return df

    if "likelihood" in header.coords:
        # Merge annotations from multiple scorers to keep
        # detections with highest confidence
        data = df.to_numpy().reshape((n_frames, n_scorers, -1, 3))
        try:
            idx = np.nanargmax(data[..., 2], axis=1)
        except ValueError:  # All-NaN slice encountered
            mask = np.isnan(data[..., 2]).all(axis=1, keepdims=True)
            mask = np.broadcast_to(mask[..., None], data.shape)
            data[mask] = -1
            idx = np.nanargmax(data[..., 2], axis=1)
            data[mask] = np.nan
        data_best = data[
            np.arange(n_frames)[:, None], idx, np.arange(data.shape[2])
        ].reshape((n_frames, -1))
        df = pd.DataFrame(
            data_best,
            index=df.index,
            columns=header.columns[: data_best.shape[1]],
        )
    else:  # Arbitrarily pick data from the first scorer
        df = df.loc(axis=1)[: header.scorer]
    return df


def to_os_dir_sep(path: str) -> str:
    """
    Replace all directory separators in `path` with `os.path.sep`.
    Function originally written by @pyzun:
    https://github.com/DeepLabCut/napari-DeepLabCut/pull/13

    Raises
    ------
    ValueError: if `path` contains both UNIX and Windows directory separators.

    """
    win_sep, unix_sep = "\\", "/"

    # On UNIX systems, `win_sep` is a valid character in directory and file
    # names. This function fails if both are present.
    if win_sep in path and unix_sep in path:
        raise ValueError(f'"{path}" may not contain both "{win_sep}" and "{unix_sep}"!')

    sep = win_sep if win_sep in path else unix_sep

    return os.path.sep.join(path.split(sep))


def guarantee_multiindex_rows(df):
    # Make paths platform-agnostic if they are not already
    if not isinstance(df.index, pd.MultiIndex):  # Backwards compatibility
        path = df.index[0]
        try:
            sep = "/" if "/" in path else "\\"
            splits = tuple(df.index.str.split(sep))
            df.index = pd.MultiIndex.from_tuples(splits)
        except TypeError:  # Ignore numerical index of frame indices
            pass


def build_color_cycle(n_colors: int, colormap: Optional[str] = "viridis") -> np.ndarray:
    cmap = colormaps.ensure_colormap(colormap)
    return cmap.map(np.linspace(0, 1, n_colors))


def build_color_cycles(header: DLCHeader, colormap: Optional[str] = "viridis"):
    label_colors = build_color_cycle(len(header.bodyparts), colormap)
    id_colors = build_color_cycle(len(header.individuals), colormap)
    return {
        "label": dict(zip(header.bodyparts, label_colors)),
        "id": dict(zip(header.individuals, id_colors)),
    }


class DLCHeader:
    def __init__(self, columns: pd.MultiIndex):
        self.columns = columns

    @classmethod
    def from_config(cls, config: Dict) -> DLCHeader:
        multi = config.get("multianimalproject", False)
        scorer = [config["scorer"]]
        if multi:
            columns = pd.MultiIndex.from_product(
                [
                    scorer,
                    config["individuals"],
                    config["multianimalbodyparts"],
                    ["x", "y"],
                ]
            )
            if len(config["uniquebodyparts"]):
                temp = pd.MultiIndex.from_product(
                    [scorer, ["single"], config["uniquebodyparts"], ["x", "y"]]
                )
                columns = columns.append(temp)
            columns.set_names(
                ["scorer", "individuals", "bodyparts", "coords"], inplace=True
            )
        else:
            columns = pd.MultiIndex.from_product(
                [scorer, config["bodyparts"], ["x", "y"]],
                names=["scorer", "bodyparts", "coords"],
            )
        return cls(columns)

    def form_individual_bodypart_pairs(self) -> List[Tuple[str]]:
        to_drop = [
            name
            for name in self.columns.names
            if name not in ("individuals", "bodyparts")
        ]
        temp = self.columns.droplevel(to_drop).unique()
        if "individuals" not in temp.names:
            temp = pd.MultiIndex.from_product([self.individuals, temp])
        return temp.to_list()

    @property
    def scorer(self) -> str:
        return self._get_unique("scorer")[0]

    @scorer.setter
    def scorer(self, scorer: str):
        self.columns = self.columns.set_levels([scorer], level="scorer")

    @property
    def individuals(self) -> List[str]:
        individuals = self._get_unique("individuals")
        if individuals is None:
            return [""]
        return individuals

    @property
    def bodyparts(self) -> List[str]:
        return self._get_unique("bodyparts")

    @property
    def coords(self) -> List[str]:
        return self._get_unique("coords")

    def _get_unique(self, name: str) -> Optional[List]:
        if name in self.columns.names:
            return list(unsorted_unique(self.columns.get_level_values(name)))
        return None


class CycleEnumMeta(EnumMeta):
    def __new__(metacls, cls, bases, classdict):
        enum_ = super().__new__(metacls, cls, bases, classdict)
        enum_._cycle = cycle(enum_._member_map_[name] for name in enum_._member_names_)
        return enum_

    def __iter__(cls):
        return cls._cycle

    def __next__(cls):
        return next(cls.__iter__())

    def __getitem__(self, item):
        if isinstance(item, str):
            item = item.upper()
        return super().__getitem__(item)


class CycleEnum(Enum, metaclass=CycleEnumMeta):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    def __str__(self):
        return self.value
