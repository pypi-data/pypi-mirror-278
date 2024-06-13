import pandas as pd
from cumulative.transforms.transform import Transform


class Sample(Transform):
    def apply(self, src: str, n: int = None, frac: float = None) -> pd.DataFrame:
        """
        Sample dataset, either with a fixed number `n` of rows, or a
        percentage `frac`.
        """

        self.c.df = self.c.df.sample(frac=frac, n=n, random_state=123)
