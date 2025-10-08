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
  title: basic pandas
---

# basic medium

```{code-cell} ipython3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from vega_datasets import data

# if vega_datasets is not installed, you can install it from the
# notebook with
# %pip install vega_datasets
# restart the kernel after installation
```

## let's load the cars dataset

```{code-cell} ipython3
cars = data.cars()
```

## Explore the shape and first few lines of the dataset

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

cars.shape
```

```{code-cell} ipython3
# prune-cell

cars.head(2)
```

## Compute the mean and std for numeric columns

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

cars.loc[:, "Miles_per_Gallon":"Acceleration"].agg([np.mean, np.std])

# alternatives
# cars.iloc[:, 1:7].agg([np.mean, np.std])
# cars.std(numeric_only=True)
# cars.mean(numeric_only=True)
```

## Put the name of the columns labels in lower case

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

cars.columns = cars.columns.str.lower()
```

```{code-cell} ipython3
# check it
cars.head(2)
```

## Create a column "consommation (l/km)", and remove the column miles_per_gallon

Tip: miles_per_gallon/235.2 = litre_per_100km

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

cars = (
    cars.assign(conso=lambda df: 235.2 / df.loc[:, "miles_per_gallon"])
    .rename(columns={"conso": "consommation (l/km)"})
    .drop(columns="miles_per_gallon")
)
cars.head()
```

## Create a columns "poids (kg)" and remove the column weight_in_lbs

Tip: 1lb = 0.454 kg

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

cars = (
    cars.assign(poids=lambda df: 0.454 * df.loc[:, "weight_in_lbs"])
    .rename(columns={"poids": "poids (Kg)"})
    .drop(columns="weight_in_lbs")
)
```

## Count the number of different origin

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

unique_origin = cars.loc[:, "origin"].unique()
print(unique_origin, len(unique_origin))
```

## Check the memory usage of the origin column, convert the column 'origin' to category, check the new memory usage*

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

cars.memory_usage(deep=True)
```

```{code-cell} ipython3
# prune-cell

cars.loc[:, "origin"] = cars.loc[:, "origin"].astype("category")
cars.memory_usage(deep=True)
```

```{code-cell} ipython3
# prune-cell

cars.dtypes
```

***
