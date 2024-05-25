---
jupytext:
  cell_metadata_filter: all, -hidden, -heading_collapsed, -run_control, -trusted
  notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version, -jupytext.text_representation.format_version,
    -language_info.version, -language_info.codemirror_mode.version, -language_info.codemirror_mode,
    -language_info.file_extension, -language_info.mimetype, -toc
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
  title: des groupby un peu chauds
---

# some grouping tricks

```{code-cell} ipython3
import numpy as np
import pandas as pd
```

## dataset 1

+++

we have the following dataset, these are the results of a survey
there is one line per answer, and each person participating has answered 3 questions

* what is the overall rating of the trademark
* what are the most-liked and least-liked site (among a finite list)

```{code-cell} ipython3
df1 = pd.read_excel('data/groupby-ratings.xlsx')
df1.head()
```

we want to compute, for each rating, the number of occurrences of each site among the `favorite` and `least-liked` columns

```{code-cell} ipython3
:tags: [level_basic]

# here the dataset is a little small

grouped = df1.groupby('rating')

grouped.size()
```

this is a good opportunity to see that when calling `GroupBy.aggregrate`, **one can pass a dictionary**, that says how to deal with each column

```{code-cell} ipython3
# grouped.aggregate?
```

```{code-cell} ipython3
:tags: [level_basic]

# note that this is rather fragile though, 
# any variation around that theme is likely to break
# e.g. replacing one value_counts with something like 'sum' issues a RuntimeWarning...

counts = grouped.aggregate({
    # this refers to Series.values_count()
    'favorite':    ['value_counts'],
    'least-liked': ['value_counts'], 
})
counts
```

```{code-cell} ipython3
:tags: [level_basic]

# as always, the resulting dataframe has both its indexes that are multiindexes

len(counts.index.levels), len(counts.columns.levels)
```

```{code-cell} ipython3
:tags: [level_basic]

# what's the performance of 'london' among the people who gave a rating of 3

counts.loc[(3, 'london')] 
```

------

+++

## dataset 2

```{code-cell} ipython3
df2 = pd.DataFrame(
    {
         "A": ["foo", "far", "foo", "bar", "foo", "bar", "foo", "foo"],
         "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
         "C": np.arange(1, 9),
         "D": 10-np.arange(1, 9),
     })
df2 
```

### simple groupings

we consider two groupings

* by `A` only
* by `A` and `B`

for each of these groupings, compute 

* the mean and min for C
* the max for D

```{code-cell} ipython3
# single criteria
grouped_a = df2.groupby('A')

# dual criteria
grouped_ab = df2.groupby(['A', 'B'])
```

here again, **calling `aggregate` with a dictionary** comes in handy

```{code-cell} ipython3
:tags: [level_basic]

# remember that aggregate can be shortened into just 'agg' 

grouped_a.agg({'C': ['mean', 'min'], 'D': 'max'})
```

```{code-cell} ipython3
# same on the dual-grouping
grouped_ab.agg({'C': ['mean', 'min'], 'D': 'max'})
```

### inspecting a Groupby object

```{code-cell} ipython3
:tags: [level_basic]

# how many items in each group

grouped_a.size()
```

```{code-cell} ipython3
:tags: [level_basic]

# more details of what's in each group; only the indexes show up
grouped_a.groups
```

```{code-cell} ipython3
:tags: [level_basic]

# here the keys are 2-tuples because we have grouped on 2 criteria
grouped_ab.groups
```

```{code-cell} ipython3
:tags: [level_basic]

# one value for the key gives access to one dataframe 
grouped_a.get_group('foo')
```

```{code-cell} ipython3
:tags: [level_basic]

# same here
grouped_ab.get_group(('foo', 'two'))
```

### grouping from a `Series`

+++ {"tags": ["level_intermediate"]}

for advanced users

```{code-cell} ipython3
# we could even group based on finer-grained criteria

# here just on the first letter of the 'A' column
# so the 'foo' and 'far' values are grouped together
grouped_a1c = df2.groupby(df2['A'].str[0])
```

```{code-cell} ipython3
grouped_a1c.groups
```

```{code-cell} ipython3
# explanation: here the parameter to groupby is a Series
df2['A'].str[0]
```

### using a function to decide on the grouping

+++

this means we can group arbitrarily; for example we want to group in two categories, whether the 'B' column contains a `o` or not

```{code-cell} ipython3
df2.B.unique()
```

so this should give two groups, one the one hand the rows where B is among `one` and `two`, on the other hand the ones where `B` is three

```{code-cell} ipython3
# here too this is a finer-grained criteria
# and this time we define it from a function
# here we group together the lines where the 'B' cell has a 'o'
# which results in 2 groups, 'one' and 'two' in group1, and 'three' in group2

grouped_bo = df2.groupby(df2['B'].apply(lambda b: 'o' in b))

# the way we have written this, 'True' mean 'o' is in the 'B' column
grouped_bo.size()
```

### using 2 functions to decide on the grouping

+++

this can be extended arbitrarily; we could add a grouping in a separate dimension, whether the 'A' columns contains 'f'or not

```{code-cell} ipython3
df2.A.unique()
```

```{code-cell} ipython3
criteria = df2.apply(lambda row: ('f' in row.A, 'o' in row.B), axis=1)
```

```{code-cell} ipython3
grouped_af_bo = df2.groupby(criteria)
```

```{code-cell} ipython3
# not very legible
grouped_af_bo.size()
```

```{code-cell} ipython3
# a little nicer

grouped_af_bo = df2.groupby(
    df2.apply(
        lambda row: ('f in A' if 'f' in row.A else 'nope', 'o in B' if 'o' in row.B else 'nope'), axis=1))
```

```{code-cell} ipython3
# again
grouped_af_bo.size()
```

### groupby using buckets

```{code-cell} ipython3
# we could even group by buckets
# so here the values in C are split in 3 groups which should have the same size
# (but because we have 8 lines, not a multiple of 3, it ends up in 3 + 2 + 3
grouped_auto_buckets = df2.groupby(
    pd.qcut(x=df2['C'], q=3, labels=['low', 'mid', 'high']))
grouped_auto_buckets.size()
```

```{code-cell} ipython3
# or we could define the boundaries ourselves
grouped_buckets = df2.groupby(pd.cut(df2['C'], [0, 3.5, 6.5, 10.]))
grouped_buckets.size()
```
