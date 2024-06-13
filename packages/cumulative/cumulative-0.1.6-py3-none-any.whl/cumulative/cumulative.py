import logging

import pandas as pd

from cumulative.opts import options
from cumulative.plot import Plot
from cumulative.transforms.frame.cluster import Cluster
from cumulative.transforms.frame.copy import Copy
from cumulative.transforms.frame.drop import Drop
from cumulative.transforms.frame.sample import Sample
from cumulative.transforms.frame.score import Score
from cumulative.transforms.frame.sort import Sort
from cumulative.transforms.row.apply import Apply
from cumulative.transforms.row.bin import Bin
from cumulative.transforms.row.cumsum import CumSum
from cumulative.transforms.row.diff import Diff
from cumulative.transforms.row.interpolate import Interpolate
from cumulative.transforms.row.scale import Scale
from cumulative.transforms.transform import Transform
from cumulative.utils.frames import columns_with_prefix
from cumulative.utils.lineage import Lineage

log = logging.getLogger(__name__)


class Cumulative:
    def __init__(self, df: pd.DataFrame):
        """
        Instantiate a new Cumulative interface to dataframe `df`.
        """

        self.df = df

        # Transforms
        self.scale = Scale(self)
        self.diff = Diff(self)
        self.cumsum = CumSum(self)
        self.interpolate = Interpolate(self)
        self.score = Score(self)
        self.copy = Copy(self)
        self.sort = Sort(self)
        self.cluster = Cluster(self)
        self.bin = Bin(self)
        self.drop = Drop(self)
        self.apply = Apply(self)
        self.sample = Sample(self)

        # Utilities
        self.plot = Plot(self)
        self.lineage = Lineage()
        self.explain = self.lineage.explain

    def register_transform(self, name: str, cls: Transform):
        """
        Register a new transform named `name`, implemented by class `cls`.
        """
        self.__dict__[name] = cls(self)

    def frame(self, src: str | None = None) -> pd.DataFrame:
        """
        Return dataframe with `src` as column prefix.
        """

        src = options().default_if_null(src, "transforms.src")
        return self.df[columns_with_prefix(self.df, src)]

    def describe(self, src: str | None = None):
        """
        Print basic statistics about the collection in the `src` dimension.
        """

        src = options().default_if_null(src, "transforms.src")

        def min_max_diff(values):
            return f"min={values.min()} max={values.max()} diff={values.max() - values.min()}"

        print(f"Count...: {len(self.df)}")
        print(f"Length..: {min_max_diff(self.df[f'{src}.x'].apply(len))}")
        print(f"X min...: {min_max_diff(self.df[f'{src}.x'].apply(min))}")
        print(f"X max...: {min_max_diff(self.df[f'{src}.x'].apply(max))}")
        print(f"Y min...: {min_max_diff(self.df[f'{src}.y'].apply(min))}")
        print(f"Y max...: {min_max_diff(self.df[f'{src}.y'].apply(max))}")
