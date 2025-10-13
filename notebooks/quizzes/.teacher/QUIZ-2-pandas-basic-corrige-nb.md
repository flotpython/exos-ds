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

```{code-cell} ipython3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
```

# pandas basics

`california_cities.csv` contains the population and area in km2 for california cities

```{code-cell} ipython3
URL = "http://www-sop.inria.fr/members/Arnaud.Legout/formationPython/Exos/california_cities.csv"

# we extract only 3 columns
cities = pd.read_csv(URL)[["city", "area_total_km2", "population_total"]]
```

## Explore the dataset with `info()` and `describe()`

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

cities.info()
```

```{code-cell} ipython3
# prune-cell

df = cities.describe()
df
```

## How many cities with the 25% largest population ?

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3

# prune-cell 

cities.loc[:, "population_total"].quantile(0.75)

# or 

cities.population_total.quantile(0.75)
```

```{code-cell} ipython3
# prune-cell 

# alternatively
# q75 = cities.loc[:, 'population_total'].quantile(0.75)
q75 = df.loc["75%", "population_total"]
mask_25th_largest_pop = cities["population_total"] >= q75
most_polulated_cities = cities.loc[mask_25th_largest_pop, :]
print(
    f"Number of the cities with the 25% largest population: {most_polulated_cities.shape[0]}"
)
```

## Get the name of the cites with the 25% largest area

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

q75 = df.loc["75%", "area_total_km2"]
most_largest_cities = cities.loc[cities["area_total_km2"] >= q75, "city"]
most_largest_cities
```

## What is the area and population of Berkeley?

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
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
```

## Which cities have between 110k and 120k inhabitants?

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

mask_pop_range = (cities.loc[:, "population_total"] >= 110_000) & (
    cities.loc[:, "population_total"] <= 120_000
)

list(cities.loc[mask_pop_range, "city"])
```

```{code-cell} ipython3
# prune-cell

# or more simply
mask_pop_range = (cities.population_total >= 110_000) & (cities.population_total <= 120_000)

list(cities[mask_pop_range].city)
```

```{code-cell} ipython3
# prune-cell

# or yet another version
# note that between is more elegent
mask_pop_range = cities.loc[:, "population_total"].between(110_000, 120_000)
list(cities.loc[mask_pop_range, "city"])
```
