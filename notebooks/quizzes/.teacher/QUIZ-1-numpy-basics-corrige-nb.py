# -*- coding: utf-8 -*-
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
#     title: basic numpy
# ---

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %% [markdown]
# # data loading

# %% [markdown]
# Let's load a dataset on rain precipitations on Seattle on 2014

# %%
# we download the file from Internet and save it
# easiest way, we can pass a URL to read_csv (or a local file)
URL = "http://www-sop.inria.fr/members/Arnaud.Legout/formationPython/Exos/Seattle2014.csv"

# don't worry, we will come back to this line when we will talk about pandas.
# for now it just load a ndarray
rainfall = pd.read_csv(URL)["PRCP"].to_numpy()

# other solution to get the remote file with urllib
# from urllib.request import urlopen
# with open("Seattle2014.csv", "w", encoding='utf-8') as f:
#    with urlopen(URL) as u:
#        f.write(u.read().decode('utf-8'))

# we extract with pandas the precipitation column
# rainfall is an array of precipitation per day 
# for each day of 2014
# rainfall = pd.read_csv('Seattle2014.csv')['PRCP'].to_numpy()


# %% [markdown]
# ## Let's visualize

# %% [markdown]
# **[assignement]**: plot the amount of rain (in mm) over time; make sure you put a proper label on both axes, and on the global figure
#

# %%
# your code here

# %% tags=[]
# prune-cell 

plt.plot(rainfall)
plt.xlabel("days")
plt.ylabel("mm")
plt.title("Rainy days in 2014 at Seattle")

# %% [markdown]
# ## Let's answer the following questions

# %% [markdown]
# **What is the shape and dype of the ndarray?**

# %%
# your code here

# %%
# prune-cell 
print(f"{rainfall.shape=}\n{rainfall.dtype=}")

# %% [markdown]
# **How many rainy days?**

# %%
# your code here

# %%
# prune-cell 
rainy_days = np.sum(rainfall > 0)
print(f"{rainy_days=} days")

# %% [markdown]
# **Average precipitation on the year?**

# %%
# your code here

# %%
# prune-cell 
ave_precip_year = np.mean(rainfall)
print(f"{ave_precip_year=:.2f}mm")

# %% [markdown]
# **Average precipitation on the rainy days?**

# %%
# your code here

# %%
# prune-cell 
ave_precip_rainy = np.mean(rainfall[rainfall > 0])
print(f"{ave_precip_rainy=:.2f}mm")

# %% [markdown]
# **Mean precipitation on January?**

# %%
# your code here

# %%
# prune-cell 

# let's build expressive masks
day = np.arange(1, rainfall.shape[0] + 1)
january = day <= 31
rainy = rainfall > 0

# mean precipitation on January
mean_jan = np.mean(rainfall[january])
print(f"{mean_jan=:.2f}mm")

# %% [markdown]
# **Mean precipitation on January on the rainy days?**

# %%
# your code here

# %%
# prune-cell

mean_jan_rainy = np.mean(rainfall[january & rainy])
print(f"{mean_jan_rainy=:.2f}mm")

# %% [markdown]
# # A transition to pandas

# %%
# But in practice we don’t do that. Here is what we do…
# We start to convert to a pandas Series
s = pd.Series(rainfall)

# then we convert the index to the real dates
s.index = pd.to_datetime(s.index, unit='D',
                         origin=pd.Timestamp('1/1/2004'))

# possibly resample per month to get the total monthly rain
s = s.resample('m').max()

# %%
# then plot

# %matplotlib ipympl

s.plot.bar()
plt.xlabel('month')
plt.ylabel('mm')
plt.title('Rainy days in 2014 at Seattle')
fig = plt.gcf()
fig.autofmt_xdate()
# plt.show() # if in a terminal

# %% [markdown]
# ***
