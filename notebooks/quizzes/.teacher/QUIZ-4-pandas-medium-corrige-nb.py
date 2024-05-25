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
#     title: basic pandas
# ---

# %% [markdown]
# # basic medium

# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from vega_datasets import data

# if vega_datasets is not installed, you can install it from the
# notebook with
# # %pip install vega_datasets
# restart the kernel after installation

# %% [markdown]
# ## let's load the cars dataset

# %%
cars = data.cars()

# %% [markdown]
# ## Explore the shape and first few lines of the dataset

# %%
# your code

# %%
# prune-cell

cars.shape

# %%
# prune-cell

cars.head(2)

# %% [markdown]
# ## Compute the mean and std for numeric columns

# %%
# your code

# %%
# prune-cell

cars.loc[:, "Miles_per_Gallon":"Acceleration"].agg([np.mean, np.std])

# alternatives
# cars.iloc[:, 1:7].agg([np.mean, np.std])
# cars.std(numeric_only=True)
# cars.mean(numeric_only=True)

# %% [markdown]
# ## Put the name of the columns labels in lower case

# %%
# your code

# %%
# prune-cell

cars.columns = cars.columns.str.lower()

# %%
# check it
cars.head(2)

# %% [markdown]
# ## Create a column "consommation (l/km)", and remove the column miles_per_gallon
#
# Tip: miles_per_gallon/235.2 = litre_per_100km

# %%
# your code

# %%
# prune-cell

cars = (
    cars.assign(conso=lambda df: 235.2 / df.loc[:, "miles_per_gallon"])
    .rename(columns={"conso": "consommation (l/km)"})
    .drop(columns="miles_per_gallon")
)
cars.head()

# %% [markdown]
# ## Create a columns "poids (kg)" and remove the column weight_in_lbs
#
# Tip: 1lb = 0.454 kg

# %%
# your code

# %%
# prune-cell

cars = (
    cars.assign(poids=lambda df: 0.454 * df.loc[:, "weight_in_lbs"])
    .rename(columns={"poids": "poids (Kg)"})
    .drop(columns="weight_in_lbs")
)

# %% [markdown]
# ## Count the number of different origin

# %%
# your code

# %%
# prune-cell

unique_origin = cars.loc[:, "origin"].unique()
print(unique_origin, len(unique_origin))

# %% [markdown]
# ## Check the memory usage of the origin column, convert the column 'origin' to category, check the new memory usage*

# %%
# your code

# %%
# prune-cell

cars.memory_usage(deep=True)

# %%
# prune-cell

cars.loc[:, "origin"] = cars.loc[:, "origin"].astype("category")
cars.memory_usage(deep=True)

# %%
# prune-cell

cars.dtypes

# %% [markdown]
# ***
