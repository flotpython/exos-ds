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
#     title: visualization
# ---

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %% [markdown]
# # pandas visu

# %%
iris = sns.load_dataset("iris")

# %% [markdown]
# ## Explore the dataset with `info()` and `head()`

# %%
# your code

# %%
# prune-cell

iris.info()

# %%
# prune-cell

iris.head(2)

# %% [markdown]
# ## Is there a correlation between any two metrics per species?
#
# (hint: `pairplot`)

# %%
# your code

# %%
# prune-cell

sns.pairplot(data=iris, hue="species");

# %% [markdown]
# ## Is there a correlation between `sepal_length` and `petal_length`
#
# (hint: `relplot`, `lmplot`)

# %%
# your code

# %%
# prune-cell

sns.lmplot(
    data=iris, x="sepal_length", y="petal_length", hue="species", ci=99, n_boot=10_000
);

# %% [markdown]
# ## What is the distribution of the `sepal_width`
#
# (hint: `displot`, `catplot`)

# %%
# your code

# %%
# prune-cell

sns.displot(data=iris, x="sepal_width", hue="species", kind="kde");

# %%
# prune-cell

sns.catplot(data=iris, x="species", y="sepal_width", kind="swarm");

# %% [markdown]
# ***
