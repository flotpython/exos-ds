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
  pygments_lexer: ipython3
  nbconvert_exporter: python
---

(label-tp-leases)=
# grouping by period and category

```{admonition} download the zip
:class: warning

to work on this assignment locally on your laptop, {download}`start with downloading the zip<./ARTEFACTS-leases.zip>`
```

in this TP we work on

- data that represents *periods* and not just one timestamp
- checking for overlaps
- grouping by period (week, month, year..)
- then later on, grouping by period *and* category
- and some simple visualization tools

here's an example of the outputs we will obtain

(label-leases-output)=
````{grid} 3 3 3 3
```{image} media/result-color-w.png
```
```{image} media/result-color-m.png
```
```{image} media/result-color-y.png
```
````

+++

## imports

```{code-cell} ipython3

import pandas as pd
import matplotlib.pyplot as plt
```

1. make sure to use matplotlib in interactive mode - aka `ipympl`

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

# we don't actually do it as it tends to break the HTML output
# %matplotlib ipympl
```

2. optional: setup itables, so that we can have scrollable tables

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

import itables
itables.init_notebook_mode()
```

## the data

we have a table of events, each with a begin (`beg`) and `end` time; in addition each is attached to a `country`

```{code-cell} ipython3
leases = pd.read_csv("data/leases.csv")
leases.head(10)
```

### adapt the type of each columns

surely the columns dtypes need some care

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

# using this format string is a little magic

leases['beg'] = pd.to_datetime(leases['beg'], format="ISO8601")
leases['end'] = pd.to_datetime(leases['end'], format="ISO8601")
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

```{code-cell} ipython3
# prune-cell

((leases['end'] - leases['beg']) > pd.Timedelta(0)).all()
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

```{code-cell} ipython3
# prune-begin

# consider the table sorted by the begin timestamp
# then if there is no overlap, we must have end[i] <= beg[i+1]

# sort by ascending 'beg'

leases.sort_values(by='beg', ascending=True, inplace=True)
leases.head(3)
```

```{code-cell} ipython3
# the beginning of next lease
# of course this will be undefined for the last row
next_beg = leases['beg'].shift(-1)
next_beg.tail(3)
```

```{code-cell} ipython3
# step by step: this is the duration time between the beginning of next lease and the end of this one
diff = next_beg - leases['end']
diff.tail(3)
```

```{code-cell} ipython3
# except that it is also undefined for the last row
# so let's drop it
diff = (next_beg - leases['end'])[:-1]
diff.tail(3)
```

```{code-cell} ipython3
# all we need to do is to check that it is always >= 0

(diff >= pd.Timedelta(0)).all()
```

```{code-cell} ipython3
# so, all in one line - but hardly legible then ;(

(((leases['beg'].shift(-1) - leases['end'])[:-1]) >= pd.Timedelta(0)).all()
```

```{code-cell} ipython3
# prune-end
```

### timespan

What is the timespan covered by the dataset (**earliest** and **latest** events, and **duration** in-between) ?

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

desc = leases.describe()

earliest = desc.loc['min', 'beg']
latest = desc.loc['max', 'end']
duration = latest-earliest

print(f"{earliest=}")
print(f"{latest=}")
print(f"{duration=}")
```

### aggregated duration

so, given that there is no overlap, we can assume this corresponds to "reservations" attached to a unique resource (hence the term  *lease*)  
write a code that computes the **overall reservation time**, as well as the **average usage ratio** over the overall timespan

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

reserved_duration = (leases['end'] - leases['beg']).sum()
percent = (reserved_duration/duration) * 100

print(f"reserved during {reserved_duration} - i.e. a ratio of {percent:.2f}%")
```

## visualization - grouping by period

### usage by period

grouping by periods: by week, by month or by year, display the **total usage in that period**  
(when ambiguous, use the `beg` column to determine if a lease is in a period or the other)

```{admonition} *hint*
:class: dropdown tip

There are at least 2 options to do this grouping, based on `resample()` and `to_period()`  
advanced users may wish to write them both and to comment on their respective pros and cons

```

`````{admonition} for now, **just get the grouping right**
:class: dropdown

you should produce something like e.g.

````{grid} 3 3 3 3
```{image} media/result-bw-w.png
```
```{image} media/result-bw-m.png
```
```{image} media/result-bw-y.png
```
````
we'll make cosmetic improvements below, and [the final results look like this](#label-leases-output), but let's not get ahead of ourselves
`````


```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-begin
```

```{code-cell} ipython3
leases['duration'] = leases['end'] - leases['beg']
```

```{code-cell} ipython3
# solution 1: with resample:

# we need 'beg' to be in the index

# this is to make the cell idempotent
# so we can call it several times
if 'beg' in leases.columns:
    leases.set_index('beg', inplace=True)

# also, it requires to use 'ME' (month end) and 'YE'
for period in 'W', 'ME', 'YE':
    plt.figure(figsize=(8, 3))
    (leases
        .resample(period)
        ['duration']
        .sum()
        .plot.bar()
    )
    plt.show()
```

```{code-cell} ipython3
# solution 2: with to_period: a little nicer results

# this time, we can't seem to use this technique
# if beg is the index, because .dt won't apply on a DatetimeIndex

if 'beg' not in leases.columns:
    leases.reset_index(inplace=True)

for period in 'W', 'M', 'Y':
    leases['period'] = leases.beg.dt.to_period(period)
    (leases.
        pivot_table(
            values='duration',
            index='period',
            columns=[],
            aggfunc='sum',
        ).plot.bar()
    )
    filename = f"media/auto-result-bw-{period.lower()}"
    plt.savefig(filename)
    plt.show()
```

```{code-cell} ipython3
# prune-end
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

```{code-cell} ipython3
# prune-cell

for period in 'W', 'M', 'Y':
# for period in  'Y':
    leases['period'] = leases.beg.dt.to_period(period)
    # needed to know how many ticks to create
    draw_df = leases.pivot_table(
        values='duration',
        index='period',
        columns=[],
        aggfunc='sum',
    )
    ax = draw_df.plot.bar(
        title=f"Duration in ns per {LEGEND[period]}"
    )
    # fewer ticks
    ax.set_xticks(range(0, len(draw_df), SPACES[period]))
    # the font size
    ax.tick_params(axis='x', which='major', labelsize=5)

    plt.show()
```

### a function to convert to hours

you are to write a function that converts a `pd.Timedelta` into a number of hours  
1. read and understand the test code for the details of what is expected
2. use it to test your own implementation

```{code-cell} ipython3

# your code

def convert_timedelta_to_hours(timedelta: pd.Timedelta) -> int:
    pass
```

```{code-cell} ipython3

# prune-cell

import numpy as np

def convert_timedelta_to_hours(timedelta):
    seconds = timedelta.total_seconds()
    return int(((seconds-1) // 3600) + 1)
```

```{code-cell} ipython3
# test it

# if an hour has started even by one second, it is counted
test_cases = ( 
    # input in seconds, expected result in hours
    (0, 0), 
    (1, 1),     (3599, 1),     (3600, 1), 
    (3601, 2),  (7199, 2),     (7200, 2), 
    # 2 hours + 1s -> 3 hours
    (7201, 3),  
    # 3 hours + 2 minutes -> 4 hours
    (pd.Timedelta(3, 'h') + pd.Timedelta(2, 'm'), 4),
    # 2 days -> 48 hours
    (pd.Timedelta(2, 'D'), 48),
)

def test_convert_timedelta_to_hours():
    for seconds, exp in test_cases:
        # convert into pd.Timedelta if not already one
        if not isinstance(seconds, pd.Timedelta):
            timedelta = pd.Timedelta(seconds=seconds)
        else:
            timedelta = seconds
        # compute and compare
        got = convert_timedelta_to_hours(timedelta)
        print(f"with {timedelta=} we get {got} and expected {exp} -> {got == exp}")

test_convert_timedelta_to_hours()
```

```{code-cell} ipython3

# for debugging; this should return 48

convert_timedelta_to_hours(pd.Timedelta(2, 'D'))
```

### use it to display totals in hours

keep the same visu, but display **the Y axis in hours**  
btw, what was the unit in the graphs above ?

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

for period in 'W', 'M', 'Y':
    leases['period'] = leases.beg.dt.to_period(period)
    draw_df = leases.pivot_table(
        values='duration',
        index='period',
        columns=[],
        aggfunc="sum",
    ).map(convert_timedelta_to_hours)

    ax = draw_df.plot.bar(
        title=f"Duration in hours per {LEGEND[period]}"
    )
    ax.set_xticks(range(0, len(draw_df), SPACES[period]))
    plt.show()
```

## grouping by period and region

the following table allows you to map each country into a region

```{code-cell} ipython3
# load it

countries = pd.read_csv("data/countries.csv")
countries.head(3)
```

### a glimpse on regions

what's the most effective way to see how many regions and how many countries per region ?

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

# like always, one can access the series with
# countries['region'] or countries.loc[:, 'region']
countries.region.value_counts()
```

### attach a region to each lease

your mission is to now show the same graphs, but we want to reflect the relative usage of each region, so we want to [split each bar into several colors, one per region see expected result below](#label-leases-output)

+++

most likely your first move is to tag all leases with a `region` column

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

leases2 = leases.merge(countries, left_on='country', right_on='name')

# no need to keep this since it duplicates 'country'
leases2.drop(columns=['name'], inplace=True)

leases2
```


### visu by period by region

you can now produce [the target figures, again they look like this](#label-leases-output)

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

for period in 'W', 'M', 'Y':
    # continue
    leases2['period'] = leases.beg.dt.to_period(period)
    draw_df = (
        leases2.pivot_table(
            values='duration',
            index='period',
            columns='region',
            aggfunc="sum",
        )
        .fillna(pd.Timedelta(0))
        .map(convert_timedelta_to_hours)
    )

    ax = draw_df.plot.bar(
        title=f"Duration in hours per {LEGEND[period]}",
        stacked=True,
    )
    ax.set_xticks(range(0, len(draw_df), SPACES[period]))
    # this is just to build the assignment
    plt.savefig(f"media/auto-result-color-{period.lower()}.png")
    plt.show()
```

***
