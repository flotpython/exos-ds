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

## Compute the mean and std for numeric columns

```{code-cell} ipython3
# your code
```

## Put the name of the columns labels in lower case

```{code-cell} ipython3
# your code
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

## Create a columns "poids (kg)" and remove the column weight_in_lbs

Tip: 1lb = 0.454 kg

```{code-cell} ipython3
# your code
```

## Count the number of different origin

```{code-cell} ipython3
# your code
```

## Check the memory usage of the origin column, convert the column 'origin' to category, check the new memory usage*

```{code-cell} ipython3
# your code
```

***
