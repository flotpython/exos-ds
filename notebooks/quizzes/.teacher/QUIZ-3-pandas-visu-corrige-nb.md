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
  title: visualization
---

```{code-cell} ipython3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
```

# pandas visu

```{code-cell} ipython3
iris = sns.load_dataset("iris")
```

## Explore the dataset with `info()` and `head()`

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

iris.info()
```

```{code-cell} ipython3
# prune-cell

iris.head(2)
```

## Is there a correlation between any two metrics per species?

(hint: `pairplot`)

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

sns.pairplot(data=iris, hue="species");
```

## Is there a correlation between `sepal_length` and `petal_length`

(hint: `relplot`, `lmplot`)

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

sns.lmplot(
    data=iris, x="sepal_length", y="petal_length", hue="species", ci=99, n_boot=10_000
);
```

## What is the distribution of the `sepal_width`

(hint: `displot`, `catplot`)

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

sns.displot(data=iris, x="sepal_width", hue="species", kind="kde");
```

```{code-cell} ipython3
# prune-cell

sns.catplot(data=iris, x="species", y="sepal_width", kind="swarm");
```

***
