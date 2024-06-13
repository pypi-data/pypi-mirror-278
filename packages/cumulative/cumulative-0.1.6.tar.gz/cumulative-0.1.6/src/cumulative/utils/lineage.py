import inspect

from cumulative.opts import options


def get_kwargs() -> dict:
    """
    Return kwargs passed to funcion calling get_kwargs().
    """

    frame = inspect.currentframe().f_back
    keys, _, _, values = inspect.getargvalues(frame)
    kwargs = {}
    for key in keys:
        if key != "self":
            kwargs[key] = values[key]
    return kwargs


class Lineage:
    """
    Handling of lineage of operations.
    """

    def __init__(self):
        self.steps = []

    def track(self, name: str, dst: str | None = None, kwargs: dict | None = None):
        """
        Track transform call `name` to `dst` with `kwargs`.
        """

        if kwargs is None:
            kwargs = {}

        kwargs = kwargs.copy()
        src = options().default_if_null(kwargs.pop("src", None), "transforms.src")
        dst = options().default_if_null(kwargs.pop("dst", None), "transforms.dst")
        drop = options().default_if_null(kwargs.pop("drop", None), "transforms.drop")

        self.steps.append({"name": name, "src": src, "dst": dst, "drop": drop, "kwargs": kwargs})

    def explain(self, max_len: int = 20, reverse: bool = False):
        """
        Print operations applied to data frame.
        """

        steps = list(enumerate(self.steps))

        if reverse:
            steps = steps[::-1]

        for idx, transform in steps:
            name = transform["name"]

            def stringify(v):
                if isinstance(v, str):
                    v = f'"{v}"'
                v = str(v)
                if len(v) > max_len:
                    v = v[:max_len] + ".."
                return v

            d = "(d)" if transform["drop"] else ""

            kwargs = ", ".join([f"{k}={stringify(v)}" for k, v in transform["kwargs"].items()])
            if idx > 0:
                srcdst = f"{stringify(transform['src'])} -> {stringify(transform['dst'])} {d}"
            else:
                srcdst = f"-> {stringify(transform['dst'])} {d}"

            print(f"[{idx}] {name}({kwargs}): {srcdst}")
