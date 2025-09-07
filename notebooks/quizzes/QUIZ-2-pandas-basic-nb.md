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
  title: primer pandas
---

# pandas basics

`california_cities.csv` contains the population and area in km2 for california cities

```{code-cell} ipython3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
```

```{code-cell} ipython3
URL = "http://www-sop.inria.fr/members/Arnaud.Legout/formationPython/Exos/california_cities.csv"

# we extract only 3 columns
cities = pd.read_csv(URL)[["city", "area_total_km2", "population_total"]]
```

## Explore the dataset with `info()` and `describe()`

```{code-cell} ipython3
# your code
```

## How many cities with the 25% largest population ?

```{code-cell} ipython3
# your code
```

## Get the name of the cites with the 25% largest area

```{code-cell} ipython3
# your code
```

## What is the area and population of Berkeley?

```{code-cell} ipython3
# your code
```

## Which cities have between 110k and 120k inhabitants?

```{code-cell} ipython3
# your code
```
