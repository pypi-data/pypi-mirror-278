import logging

import pandas as pd
from cumulative.transforms.transform import Transform
from cumulative.utils.frames import rows_with_prefix

log = logging.getLogger(__name__)


class Apply(Transform):
    def transform_row(self, row: pd.Series, src: str, func: callable = None) -> pd.Series:
        """
        Apply `func` to `row`, with `src` column prefix omitted to increase reusability.
        """

        row = row[rows_with_prefix(row, src)]
        row.index = [col.removeprefix(f"{src}.") for col in row.index]

        return pd.Series(func(row))
