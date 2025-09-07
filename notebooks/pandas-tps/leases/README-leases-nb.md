---
jupytext:
  custom_cell_magics: kql
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
---

# grouping through time and category

to work on this assignment locally on your laptop, {download}`start with downloading the zip<./ARTEFACTS-leases.zip>`

in this TP we work on 

- data that represents *periods* and not just one timestamp
- checking for overlaps
- grouping by time
  - later grouping by time and category
- and some simple visualization tools

here's an example of the outputs we will obtain

```{image} media/result-m.png
:width: 300px
:align: center
```

+++

## imports

```{code-cell} ipython3
:lines_to_next_cell: 2

import pandas as pd
import matplotlib.pyplot as plt
```

1. make sure to use matplotlib in interactive mode - aka `ipympl`

```{code-cell} ipython3
# your code
```

## the data

we have a table of events, each with a begin and end time; in addition each is attached to a country

```{code-cell} ipython3
leases = pd.read_csv("data/leases.csv")
leases.head(10)
```

### adapt the type of each columns

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# check it

leases.dtypes
```

### raincheck

check that the data is well-formed, i.e. **the `end`** timestamp **happens after `beg`**

```{code-cell} ipython3
# your code
```

### are there any overlapping events ?

+++

   it turns out there are **no event overlap**, but write a code that checks that this is true

   ```{admonition} note
   :class: tip

   nothing in the rest depends on this question, so if you find this too hard, you can skip to the next question
   ```

```{code-cell} ipython3
# your code
```

### timespan

What is the timespan coverred by the dataset (**earliest** and **latest** events, and **duration** in-between) ?

```{code-cell} ipython3
# your code
```

### aggregated duration

so, given that there is no overlap, we can assume this corresponds to "reservations" attached to a unique resource (hence the term  *lease*)

write a code that computes the **overall reservation time**, as well as the **average usage ratio** over the active period

```{code-cell} ipython3
# your code
```

## visualization - grouping by time only

### usage by period

grouping by periods: by week, by month or by year, display the **total usage in that period**  
(when ambiguous, use the `beg` column to determine if a lease is in a period or the other)

for now, just get the grouping right, we'll improve miscellaneous details below

also you can [refer to this section below](#label-sample-results) to get a glimpse of the expected output, even though for now we have no grouping, so a single color for all bars.

```{code-cell} ipython3
# your code
```

### improve the title and bottom ticks

add a title to your visualisations

also, and particularly relevant in the case of the per-week visu, we don't get to read **the labels on the horizontal axis**, because there are **too many of them**  
to improve this, you can use matplotlib's `set_xticks()` function; you can either figure out by yourself, or read the few tips below

````{admonition} a few tips
:class: dropdown tip

- the object that receives the `set_xticks()` method is an instance of `Axes` (one X&Y axes system),  
  which is not the figure itself (a figure may contain several Axes)  
  ask google or chatgpt to find the way you can spot the `Axes` instance in your figure
- it is not that clear in the docs, but all you need to do is to pass `set_xticks` a list of *indices* (integers)  
  i.e. if you have, say, a hundred bars, you could pass `[0, 10, 20, ..., 100]` and you will end up with one tick every 10 bars.
- there are also means to use smaller fonts, which may help see more relevant info
````

```{code-cell} ipython3
# let's say as arule of thumb
LEGEND = {
    'W': "week",
    'M': "month",
    'Y': "year",
}

SPACES = {
    'W': 12,   # in the per-week visu, show one tick every 12 - so about one every 3 months
    'M': 3,    # one every 3 months
    'Y': 1,    # on all years
}
```

```{code-cell} ipython3
# your code
```

### a function to convert to hours

write a function that converts a timedelta into a number of hours - see the test code for the details of what is expected

```{code-cell} ipython3
:lines_to_next_cell: 1

# your code

def convert_timedelta_to_hours(timedelta):
    pass
```

```{code-cell} ipython3
# test it

# if an hour has started even by one second, it is counted
# seconds, hours
test_cases = ( 
    (0, 0), 
    (1, 1), (3600, 1), 
    (3601, 2), (7199, 2), (7200, 2), 
    (7201, 3), (pd.Timedelta(3, 'h') + pd.Timedelta(2, 'm'), 4),
    (pd.Timedelta(2, 'D'), 48),
)

def test_convert_timedelta_to_hours():
    for seconds, exp in test_cases:
        if not isinstance(seconds, pd.Timedelta):
            timedelta = pd.Timedelta(seconds=seconds)
        else:
            timedelta = seconds
        got = convert_timedelta_to_hours(timedelta)
        print(f"with {timedelta=} we get {got} and expected {exp} -> {got == exp}")

test_convert_timedelta_to_hours()
```

```{code-cell} ipython3
:lines_to_next_cell: 2

convert_timedelta_to_hours(pd.Timedelta(2, 'D'))
```

### use it to display totals in hours

keep the same visu, but display **the Y axis in hours**

btw, what was the unit in the graphs above ?

```{code-cell} ipython3
# your code
```

## grouping by time and by region

the following table allows you to map each country into a region

```{code-cell} ipython3
# load it

countries = pd.read_csv("data/countries.csv")
countries.head(3)
```

```{code-cell} ipython3
# how many countries ?

countries.region.value_counts()
```

that is to say, 5 groups (at most)

+++

your mission is to now show the same graphs, but with each bar split into up to 5, to reflect the relative usage of each region

+++

### attach a region to each lease

most likely your first move is to tag all leases with a `region` column

```{code-cell} ipython3
# your code
```

(label-sample-results)=

### visu by time and by region

you can now produce the target figures; the expected final results looks like this

```{image} media/result-w.png
```
```{image} media/result-m.png
```
```{image} media/result-y.png
```

```{code-cell} ipython3
# your code
```
