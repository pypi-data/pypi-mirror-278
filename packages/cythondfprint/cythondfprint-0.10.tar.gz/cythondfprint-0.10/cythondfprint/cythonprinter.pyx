import cython
cimport cython
import numpy as np
cimport numpy as np
import pandas as pd

asciifunc = np.frompyfunc(ascii, 1, 1)
ResetAll = "\033[0m"

Bold = "\033[1m"
Dim = "\033[2m"
Underlined = "\033[4m"
Blink = "\033[5m"
Reverse = "\033[7m"
Hidden = "\033[8m"

ResetBold = "\033[21m"
ResetDim = "\033[22m"
ResetUnderlined = "\033[24m"
ResetBlink = "\033[25m"
ResetReverse = "\033[27m"
ResetHidden = "\033[28m"

Default = "\033[39m"
Black = "\033[30m"
Red = "\033[31m"
Green = "\033[32m"
Yellow = "\033[33m"
Blue = "\033[34m"
Magenta = "\033[35m"
Cyan = "\033[36m"
LightGray = "\033[37m"
DarkGray = "\033[90m"
LightRed = "\033[91m"
LightGreen = "\033[92m"
LightYellow = "\033[93m"
LightBlue = "\033[94m"
LightMagenta = "\033[95m"
LightCyan = "\033[96m"
White = "\033[97m"

BackgroundDefault = "\033[49m"
BackgroundBlack = "\033[40m"
BackgroundRed = "\033[41m"
BackgroundGreen = "\033[42m"
BackgroundYellow = "\033[43m"
BackgroundBlue = "\033[44m"
BackgroundMagenta = "\033[45m"
BackgroundCyan = "\033[46m"
BackgroundLightGray = "\033[47m"
BackgroundDarkGray = "\033[100m"
BackgroundLightRed = "\033[101m"
BackgroundLightGreen = "\033[102m"
BackgroundLightYellow = "\033[103m"
BackgroundLightBlue = "\033[104m"
BackgroundLightMagenta = "\033[105m"
BackgroundLightCyan = "\033[106m"
BackgroundWhite = "\033[107m"



cpdef str printdf(
    df,
    Py_ssize_t column_rep=70,
    Py_ssize_t max_lines=70,
    Py_ssize_t max_colwidth=300,
    Py_ssize_t ljust_space=2,
    str sep=" | ",
    cython.bint vtm_escape=True,
):
    cdef:
        dict[Py_ssize_t, np.ndarray] stringdict
        dict[Py_ssize_t, Py_ssize_t] stringlendict
        list[str] df_columns, allcolumns_as_string, colors2rotate
        Py_ssize_t i, len_a, len_df_columns, lenstr, counter, j, len_stringdict0, k, len_stringdict
        str stringtoprint, dashes, dashesrep, string2print, string2printcolored
        np.ndarray a
    colors2rotate = [
        LightRed,
        LightGreen,
        LightYellow,
        LightBlue,
        LightMagenta,
        LightCyan,
        White,
    ]
    if vtm_escape:
        print('\033[12:2p')
    stringdict = {}
    if len(df) > max_lines and max_lines > 0:
        a = df.iloc[:max_lines].reset_index(drop=False).T.__array__()
    else:
        a = df.reset_index(drop=False).T.__array__()
    stringlendict = {}
    try:
        df_columns = ["index"] + [str(x) for x in df.columns]
    except Exception:
        try:
            df_columns = ["index",str(df.name)]
        except Exception:
            df_columns = ["index",str(0)]
    len_a=len(a)
    for i in range(len_a):
        try:
            stringdict[i] = a[i].astype("U")
        except Exception:
            stringdict[i] = asciifunc(a[i]).astype("U")
        stringlendict[i] = (stringdict[i].dtype.itemsize // 4) + ljust_space
    for i in range(len_a):
        lenstr = len(df_columns[i])
        if lenstr > stringlendict[i]:
            stringlendict[i] = lenstr + ljust_space
        if max_colwidth > 0:
            if stringlendict[i] > max_colwidth:
                stringlendict[i] = max_colwidth

    allcolumns_as_string = []
    len_df_columns=len(df_columns)
    for i in range(len_df_columns):
        stringtoprint = str(df_columns[i])[: stringlendict[i]].ljust(stringlendict[i])
        allcolumns_as_string.append(stringtoprint)
    allcolumns_as_string_str = sep.join(allcolumns_as_string) + sep
    dashes = "-" * (len(allcolumns_as_string_str) + 2)
    dashesrep = dashes + "\n" + allcolumns_as_string_str + "\n" + dashes
    counter = 0
    len_stringdict0 = len(stringdict[0])
    len_stringdict=len(stringdict)
    for j in range(len_stringdict0):
        if column_rep > 0:
            if counter % column_rep == 0:
                print(dashesrep)
        counter += 1
        for k in range(len_stringdict):
            string2print = stringdict[k][j][: stringlendict[k]].replace("\n",
            "\\n").replace("\r", "\\r").ljust(stringlendict[k])
            string2printcolored = (
                colors2rotate[k % len(colors2rotate)] + string2print + ResetAll
            )
            print(string2printcolored, end=sep)
        print()
    return ""


