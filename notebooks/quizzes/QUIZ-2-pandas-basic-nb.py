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
#     title: primer pandas
# ---

# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# %% [markdown]
# # pandas basics
#
# `california_cities.csv` contains the population and area in km2 for california cities

# %%
URL = "http://www-sop.inria.fr/members/Arnaud.Legout/formationPython/Exos/california_cities.csv"

# we extract only 3 columns
cities = pd.read_csv(URL)[["city", "area_total_km2", "population_total"]]

# %% [markdown]
# ## Explore the dataset with `info()` and `describe()`

# %%
# your code

# %% [markdown]
# ## How many cities with the 25% largest population ?

# %%
# your code

# %% [markdown]
# ## Get the name of the cites with the 25% largest area

# %%
# your code

# %% [markdown]
# ## What is the area and population of Berkeley?

# %%
# your code

# %% [markdown]
# ## Which cities have between 110k and 120k inhabitants?

# %%
# your code
