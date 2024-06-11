from pandas.core.base import PandasObject
import pandas as pd
from pandas.core.frame import DataFrame, Series, Index

try:
    from .cythonprinter import printdf as pdp
except Exception:
    import subprocess, os, sys

    oldworkingdict = os.getcwd()
    this_folder = os.sep.join(__file__.split(os.sep)[:-1])
    os.chdir(this_folder)
    compilefile = os.path.join(this_folder, "cythonprintercompile.py")
    subprocess.run(
        [sys.executable, compilefile, "build_ext", "--inplace"],
        env=os.environ.copy(),
        shell=True,
    )
    os.chdir(oldworkingdict)
    from .cythonprinter import printdf as pdp


def print_col_width_len(df):
    try:
        pdp(
            pd.DataFrame(
                [df.shape[0], df.shape[1]], index=["rows", "columns"]
            ).T.rename(
                {0: "DataFrame"},
            ),
        )
    except Exception:
        pdp(
            pd.DataFrame([df.shape[0]], index=["rows"]).T.rename({0: "Series"}),
        )


def pandasprintcolor(self):
    pdp(pd.DataFrame(self.__array__(), columns=[str(x) for x in self.columns]))
    print_col_width_len(self.__array__())

    return ""


def copy_func(f):
    # https://stackoverflow.com/a/67083317/15096247
    # Create a lambda that mimics f
    g = lambda *args: f(*args)
    # Add any properties of f
    t = list(filter(lambda prop: not ("__" in prop), dir(f)))
    i = 0
    while i < len(t):
        setattr(g, t[i], getattr(f, t[i]))
        i += 1
    return g


def pandasprintcolor_s(self):
    print("")
    try:
        pdp(pd.DataFrame(self.__array__(), columns=[self.name]))
    except Exception:
        pdp(pd.DataFrame(self.__array__()))
    print_col_width_len(self.__array__())

    return ""


def pandasindexcolor(self):
    pdp(pd.DataFrame(self.__array__()[: self.print_stop].reshape((-1, 1))))
    return ""


def reset_print_options():
    PandasObject.__str__ = copy_func(PandasObject.old__str__)
    PandasObject.__repr__ = copy_func(PandasObject.old__repr__)
    DataFrame.__repr__ = copy_func(DataFrame.old__repr__)
    DataFrame.__str__ = copy_func(DataFrame.old__str__)
    Series.__repr__ = copy_func(Series.old__repr__)
    Series.__str__ = copy_func(Series.old__str__)
    Index.__repr__ = copy_func(Index.old__repr__)
    Index.__str__ = copy_func(Index.old__str__)


def substitute_print_with_color_print(
    print_stop: int = 69, max_colwidth: int = 300, repeat_cols: int = 70
):
    if not hasattr(pd, "color_printer_active"):
        PandasObject.old__str__ = copy_func(PandasObject.__str__)
        PandasObject.old__repr__ = copy_func(PandasObject.__repr__)
        DataFrame.old__repr__ = copy_func(DataFrame.__repr__)
        DataFrame.old__str__ = copy_func(DataFrame.__str__)
        Series.old__repr__ = copy_func(Series.__repr__)
        Series.old__str__ = copy_func(Series.__str__)
        Index.old__repr__ = copy_func(Index.__repr__)
        Index.old__str__ = copy_func(Index.__str__)

    PandasObject.__str__ = lambda x: pandasprintcolor(x)
    PandasObject.__repr__ = lambda x: pandasprintcolor(x)
    PandasObject.print_stop = print_stop
    PandasObject.max_colwidth = max_colwidth
    PandasObject.repeat_cols = repeat_cols
    DataFrame.__repr__ = lambda x: pandasprintcolor(x)
    DataFrame.__str__ = lambda x: pandasprintcolor(x)
    DataFrame.print_stop = print_stop
    DataFrame.max_colwidth = max_colwidth
    DataFrame.repeat_cols = repeat_cols
    Series.__repr__ = lambda x: pandasprintcolor_s(x)
    Series.__str__ = lambda x: pandasprintcolor_s(x)
    Series.print_stop = print_stop
    Series.max_colwidth = max_colwidth
    Series.repeat_cols = repeat_cols
    Index.__repr__ = lambda x: pandasindexcolor(x)
    Index.__str__ = lambda x: pandasindexcolor(x)
    Index.print_stop = print_stop
    Index.max_colwidth = max_colwidth
    Index.repeat_cols = 10000000
    pd.color_printer_activate = substitute_print_with_color_print
    pd.color_printer_reset = reset_print_options
    pd.color_printer_active = True


def qq_ds_print_nolimit(self, **kwargs):
    try:
        pdp(
            pd.DataFrame(self.__array__(), columns=[str(x) for x in self.columns]),
            max_lines=0,
            **kwargs,
        )
        print_col_width_len(self.__array__())
    except Exception:
        try:
            pdp(
                pd.DataFrame(self.__array__(), columns=[self.name]),
                max_lines=0,
            )
        except Exception:
            pdp(
                pd.DataFrame(self.__array__()),
                max_lines=0,
            )
        print_col_width_len(self.__array__())
    return ""


def qq_d_print_columns(self, **kwargs):
    pdp(
        pd.DataFrame(self.columns.__array__().reshape((-1, 1))),
        max_colwidth=0,
        **kwargs,
    )
    return ""


def qq_ds_print_index(self, **kwargs):
    pdp(pd.DataFrame(self.index.__array__().reshape((-1, 1))), max_colwidth=0, **kwargs)
    return ""


def add_printer(overwrite_pandas_printer=False):

    PandasObject.ds_color_print_all = qq_ds_print_nolimit
    DataFrame.d_color_print_columns = qq_d_print_columns
    DataFrame.d_color_print_index = qq_ds_print_index
    if overwrite_pandas_printer:
        substitute_print_with_color_print()
