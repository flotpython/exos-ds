---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
language_info:
  name: python
  nbconvert_exporter: python
  pygments_lexer: ipython3
nbhosting:
  title: time series
---

# timeseries

```{code-cell} ipython3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
```

## the data

```{code-cell} ipython3
URL = "http://www-sop.inria.fr/members/Arnaud.Legout/formationPython/Exos/covid-hospit-incid-reg-2021-06-08-19h09.csv"

# we extract only 3 columns
try:
    hos = pd.read_csv(URL)
except UnicodeDecodeError as e:
    print(f"decoding exception: {e}")
```

There is a decoding error, wich means the csv is not encoded  in utf-8. This is unfortunate and the real encoding is not specified on the site. Instead of making trial and fail attempts, we will use `chardet` to detect the correct encoding.

```{code-cell} ipython3
%pip install chardet

import chardet
import urllib.request

rawdata = urllib.request.urlopen(URL).read()
chardet.detect(rawdata)
```

The encoding seems to be `ISO-8859-1` with 0.73% confidence. Let's try it

```{code-cell} ipython3
try:
    hos = pd.read_csv(URL, encoding="ISO-8859-1")
except UnicodeDecodeError as e:
    print(f"decoding exception: {e}")

hos.head(2)
```

## It works, but the csv file was not correctly parsed because the separator is a `;`

```{code-cell} ipython3
# your code
hos = ...
```

```{code-cell} ipython3
# prune-cell

hos = pd.read_csv(URL, encoding="ISO-8859-1", sep=";")
hos.head()
```

## What is the dtype of each columns?

```{code-cell} ipython3

# your code
```

```{code-cell} ipython3
:tags: [raises-exception]

# prune-cell

hos.dtypes
```

## Convert

`jour` and `nomReg` are object. It will be better to have `jour` as a DatetimeIndex and `nomReg` as a category.

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

hos = (
    # create a new column date and make it a datetime64
    hos.assign(date=lambda df: pd.to_datetime(df.loc[:, "jour"]))
    # drop the old columns jour
    .drop(columns="jour")
    # set the new column date as the index and sort it
    .set_index("date")
    .sort_index()
    # create a new columns nomReg_cat with category dtype
    .assign(nomReg_cat=lambda df: df.loc[:, "nomReg"].astype("category"))
    # drop the old column
    .drop(columns="nomReg")
)
hos.info()
```

## Compute the sum of `incid_rea` weekly and plot using a bar plot (hint: use `resample`)

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

resampled_hos = hos.resample('w')['incid_rea'].sum()
resampled_hos.plot.bar()
```

## It works, but the x-axis date representation is messy.

It is an issue specific to the bar plot in pandas. With a regular line plot, the x-axis is automatically optimized.

Let us see the solution together (found on stackoverflow...)

```{code-cell} ipython3
:tags: [raises-exception]

resampled_hos.plot()
```

To solve the issue with bar plots, we need to work with matplotlib

```{code-cell} ipython3
:tags: [raises-exception]

from matplotlib.dates import AutoDateLocator, ConciseDateFormatter, AutoDateFormatter

locator = AutoDateLocator()
# ConciseDateFormatter will infer the most compact date representation
formatter = ConciseDateFormatter(locator)

# AutoDaAutoDateFormatter gives another representation
# formatter = AutoDateFormatter(locator)
ax=plt.gca()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

resampled_hos = hos.resample('w')['incid_rea'].sum()
# we need to plot directly with matplotlib otherwise dates representation will not be taken into account.
ax.bar(resampled_hos.index, resampled_hos, width=5)

# To uncomment if we use the AutoAutoDateFormatter
# fig = plt.gcf()
# fig.autofmt_xdate()
```

## Rolling

Compute now a rolling average on 14 days of `incid_rea` (hint: use `rolling`) and plot it using a line plot.

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

hos_rolling = hos.rolling('14d')['incid_rea'].mean()
hos_rolling.plot()
```

***
