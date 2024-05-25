# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control,-trusted,-editable
#     formats: py:percent
#     notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version,
#       -jupytext.text_representation.format_version,-language_info.version, -language_info.codemirror_mode.version,
#       -language_info.codemirror_mode,-language_info.file_extension, -language_info.mimetype,
#       -toc, -rise, -version
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
#   language_info:
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
#   nbhosting:
#     title: time series
# ---

# %% [markdown]
# # timeseries

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %% [markdown]
# ## the data

# %%
URL = "http://www-sop.inria.fr/members/Arnaud.Legout/formationPython/Exos/covid-hospit-incid-reg-2021-06-08-19h09.csv"

# we extract only 3 columns
try:
    hos = pd.read_csv(URL)
except UnicodeDecodeError as e:
    print(f"decoding exception: {e}")

# %% [markdown]
# There is a decoding error, wich means the csv is not encoded  in utf-8. This is unfortunate and the real encoding is not specified on the site. Instead of making trial and fail attempts, we will use `chardet` to detect the correct encoding.

# %%
# %pip install chardet

import chardet
import urllib.request

rawdata = urllib.request.urlopen(URL).read()
chardet.detect(rawdata)

# %% [markdown]
# The encoding seems to be `ISO-8859-1` with 0.73% confidence. Let's try it

# %%
try:
    hos = pd.read_csv(URL, encoding="ISO-8859-1")
except UnicodeDecodeError as e:
    print(f"decoding exception: {e}")

hos.head(2)

# %% [markdown]
# ## It works, but the csv file was not correctly parsed because the separator is a `;`

# %%
# your code
hos = ...

# %% [markdown]
# ## What is the dtype of each columns?

# %%
# your code


# %% [markdown]
# ## Convert
#
# `jour` and `nomReg` are object. It will be better to have `jour` as a DatetimeIndex and `nomReg` as a category.

# %%
# your code

# %% [markdown]
# ## Compute the sum of `incid_rea` weekly and plot using a bar plot (hint: use `resample`)

# %%
# your code

# %% [markdown]
# ## It works, but the x-axis date representation is messy.
#
# It is an issue specific to the bar plot in pandas. With a regular line plot, the x-axis is automatically optimized.
#
# Let us see the solution together (found on stackoverflow...)

# %% tags=["raises-exception"]
resampled_hos.plot()

# %% [markdown]
# To solve the issue with bar plots, we need to work with matplotlib

# %% tags=["raises-exception"]
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


# %% [markdown]
# ## Rolling
#
# Compute now a rolling average on 14 days of `incid_rea` (hint: use `rolling`) and plot it using a line plot.

# %%
# your code

# %% [markdown]
# ***
