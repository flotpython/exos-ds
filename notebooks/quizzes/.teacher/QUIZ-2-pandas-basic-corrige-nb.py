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

# %%
# prune-cell

cities.info()

# %%
# prune-cell

df = cities.describe()
df

# %% [markdown]
# ## How many cities with the 25% largest population ?

# %%
# your code

# %%
# prune-cell 

cities.loc[:, "population_total"].quantile(0.75)

# or 

cities.population_total.quantile(0.75)


# %%
# prune-cell 

# alternatively
# q75 = cities.loc[:, 'population_total'].quantile(0.75)
q75 = df.loc["75%", "population_total"]
mask_25th_largest_pop = cities["population_total"] >= q75
most_polulated_cities = cities.loc[mask_25th_largest_pop, :]
print(
    f"Number of the cities with the 25% largest population: {most_polulated_cities.shape[0]}"
)

# %% [markdown]
# ## Get the name of the cites with the 25% largest area

# %%
# your code

# %%
# prune-cell

q75 = df.loc["75%", "area_total_km2"]
most_largest_cities = cities.loc[cities["area_total_km2"] >= q75, "city"]
most_largest_cities

# %% [markdown]
# ## What is the area and population of Berkeley?

# %%
# your code

# %%
# prune-cell

# When we search for an entry, it is faster (if we make multiple searches) 
# and easier to put this column as the index
indexed_cities = cities.set_index("city").sort_index()

berkeley = indexed_cities.loc["Berkeley", :]
# NOTE that we could also have done more simply
# berkeley = indexed_cities.loc["Berkeley"]

print(
    f"Population of Berkeley: {berkeley.loc['population_total']}\nArea of Berkeley {berkeley.loc['area_total_km2']}km2"
)

# %% [markdown]
# ## Which cities have between 110k and 120k inhabitants?

# %%
# your code

# %%
# prune-cell

mask_pop_range = (cities.loc[:, "population_total"] >= 110_000) & (
    cities.loc[:, "population_total"] <= 120_000
)

list(cities.loc[mask_pop_range, "city"])

# %%
# prune-cell

# or more simply
mask_pop_range = (cities.population_total >= 110_000) & (cities.population_total <= 120_000)

list(cities[mask_pop_range].city)

# %%
# prune-cell

# or yet another version
# note that between is more elegent
mask_pop_range = cities.loc[:, "population_total"].between(110_000, 120_000)
list(cities.loc[mask_pop_range, "city"])
