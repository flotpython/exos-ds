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

## Is there a correlation between any two metrics per species?

(hint: `pairplot`)

```{code-cell} ipython3
# your code
```

## Is there a correlation between `sepal_length` and `petal_length`

(hint: `relplot`, `lmplot`)

```{code-cell} ipython3
# your code
```

## What is the distribution of the `sepal_width`

(hint: `displot`, `catplot`)

```{code-cell} ipython3
# your code
```

***
