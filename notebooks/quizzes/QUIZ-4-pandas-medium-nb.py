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

# %% [markdown]
# ## Compute the mean and std for numeric columns

# %%
# your code

# %% [markdown]
# ## Put the name of the columns labels in lower case

# %%
# your code

# %%
# check it
cars.head(2)

# %% [markdown]
# ## Create a column "consommation (l/km)", and remove the column miles_per_gallon
#
# Tip: miles_per_gallon/235.2 = litre_per_100km

# %%
# your code

# %% [markdown]
# ## Create a columns "poids (kg)" and remove the column weight_in_lbs
#
# Tip: 1lb = 0.454 kg

# %%
# your code

# %% [markdown]
# ## Count the number of different origin

# %%
# your code

# %% [markdown]
# ## Check the memory usage of the origin column, convert the column 'origin' to category, check the new memory usage*

# %%
# your code

# %% [markdown]
# ***
