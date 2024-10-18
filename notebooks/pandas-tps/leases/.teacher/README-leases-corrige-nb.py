# ---
# jupyter:
#   jupytext:
#     custom_cell_magics: kql
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
# ---

# %% [markdown]
# # grouping through time and category
#
# to work on this assignment locally on your laptop, {download}`start with downloading the zip<./ARTEFACTS-leases.zip>`
#
# in this TP we work on 
#
# - data that represents *periods* and not just one timestamp
# - checking for overlaps
# - grouping by time
#   - later grouping by time and category
# - and some simple visualization tools
#
# here's an example of the outputs we will obtain
#
# ```{image} media/result-m.png
# :width: 300px
# :align: center
# ```

# %% [markdown]
# ## imports

# %%
import pandas as pd
import matplotlib.pyplot as plt


# %% [markdown]
# 1. make sure to use matplotlib in interactive mode - aka `ipympl`

# %%
# your code

# %%
# prune-cell

# %matplotlib ipympl

# %% [markdown]
# ## the data
#
# we have a table of events, each with a begin and end time; in addition each is attached to a country

# %%
leases = pd.read_csv("data/leases.csv")
leases.head(10)

# %% [markdown]
# ### adapt the type of each columns

# %%
# your code

# %%
# prune-cell

# using this format string is a little magic

leases['beg'] = pd.to_datetime(leases['beg'], format="ISO8601")
leases['end'] = pd.to_datetime(leases['end'], format="ISO8601")

# %%
# check it

leases.dtypes

# %% [markdown]
# ### raincheck
#
# check that the data is well-formed, i.e. **the `end`** timestamp **happens after `beg`**

# %%
# your code

# %%
# prune-cell

((leases['end'] - leases['beg']) > pd.Timedelta(0)).all()

# %% [markdown]
# ### are there any overlapping events ?

# %% [markdown]
#    it turns out there are **no event overlap**, but write a code that checks that this is true
#
#    ```{admonition} note
#    :class: tip
#
#    nothing in the rest depends on this question, so if you find this too hard, you can skip to the next question
#    ```

# %%
# your code

# %%
# prune-begin

# consider the table sorted by the begin timestamp
# then if there is no overlap, we must have end[i] <= beg[i+1]

# sort by ascending 'beg'

leases.sort_values(by='beg', ascending=True, inplace=True)
leases.head(3)

# %%
# the beginning of next lease
# of course this will be undefined for the last row
next_beg = leases['beg'].shift(-1)
next_beg.tail(3)

# %%
# step by step: this is time between the beginning of next lease and the end of this one
diff = next_beg - leases['end']
diff.tail(3)

# %%

# except that it is also undefined for the last row
# so let's drop it
diff = (next_beg - leases['end'])[:-1]
diff.tail(3)

# %%
# to check that it is always >= 0

(diff >= pd.Timedelta(0)).all()

# %%
# so, all in one line - but hardly legible then ;(

(((leases['beg'].shift(-1) - leases['end'])[:-1]) >= pd.Timedelta(0)).all()

# %%
# prune-end

# %% [markdown]
# ### timespan
#
# What is the timespan coverred by the dataset (**earliest** and **latest** events, and **duration** in-between) ?

# %%
# your code

# %%
# prune-cell

desc = leases.describe()

earliest = desc.loc['min', 'beg']
latest = desc.loc['max', 'end']
duration = latest-earliest

print(f"{earliest=}")
print(f"{latest=}")
print(f"{duration=}")

# %% [markdown]
# ### aggregated duration
#
# so, given that there is no overlap, we can assume this corresponds to "reservations" attached to a unique resource (hence the term  *lease*)
#
# write a code that computes the **overall reservation time**, as well as the **average usage ratio** over the active period  

# %%
# your code

# %%
# prune-cell

reserved_duration = (leases['end'] - leases['beg']).sum()
percent = (reserved_duration/duration) * 100

print(f"reserved during {reserved_duration} - i.e. a ratio of {percent:.2f}%")

# %% [markdown]
# ## visualization - grouping by time only
#
# ### usage by period
#
# grouping by periods: by week, by month or by year, display the **total usage in that period**  
# (when ambiguous, use the `beg` column to determine if a lease is in a period or the other)
#
# for now, just get the grouping right, we'll improve miscellaneous details below
#
# also you can [refer to this section below](#label-sample-results) to get a glimpse of the expected output, even though for now we have no grouping, so a single color for all bars.

# %%
# your code

# %%
# prune-begin

# %%
leases['duration'] = leases['end'] - leases['beg']

# %%
# with resample:

# we need 'beg' to be in the index

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

# %%
# with to_period: a little nicer results

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
    plt.show()

# %%
# prune-end

# %% [markdown]
# ### improve the title and bottom ticks
#
# add a title to your visualisations
#
# also, and particularly relevant in the case of the per-week visu, we don't get to read **the labels on the horizontal axis**, because there are **too many of them**  
# to improve this, you can use matplotlib's `set_xticks()` function; you can either figure out by yourself, or read the few tips below
#
# ````{admonition} a few tips
# :class: dropdown tip
#
# - the object that receives the `set_xticks()` method is an instance of `Axes` (one X&Y axes system),  
#   which is not the figure itself (a figure may contain several Axes)  
#   ask google or chatgpt to find the way you can spot the `Axes` instance in your figure
# - it is not that clear in the docs, but all you need to do is to pass `set_xticks` a list of *indices* (integers)  
#   i.e. if you have, say, a hundred bars, you could pass `[0, 10, 20, ..., 100]` and you will end up with one tick every 10 bars.
# - there are also means to use smaller fonts, which may help see more relevant info
# ````

# %%
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

# %%
# your code

# %%
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


# %% [markdown]
# ### a function to convert to hours
#
# write a function that converts a timedelta into a number of hours - see the test code for the details of what is expected

# %%
# your code

def convert_timedelta_to_hours(timedelta):
    pass

# %%
# prune-cell

import numpy as np

def convert_timedelta_to_hours(timedelta):
    seconds = timedelta.total_seconds()
    return int(((seconds-1) // 3600) + 1)

# %%
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

# %%
convert_timedelta_to_hours(pd.Timedelta(2, 'D'))


# %% [markdown]
# ### use it to display totals in hours
#
# keep the same visu, but display **the Y axis in hours**
#
# btw, what was the unit in the graphs above ?

# %%
# your code

# %%
# prune-cell

for period in 'W', 'M', 'Y':
    leases['period'] = leases.beg.dt.to_period(period)
    draw_df = leases.pivot_table(
        values='duration',
        index='period',
        columns=[],
        aggfunc=sum,
    ).map(convert_timedelta_to_hours)

    ax = draw_df.plot.bar(
        title=f"Duration in hours per {LEGEND[period]}"
    )
    ax.set_xticks(range(0, len(draw_df), SPACES[period]))
    plt.show()

# %% [markdown]
# ## grouping by time and by region
#
# the following table allows you to map each country into a region

# %%
# load it

countries = pd.read_csv("data/countries.csv")
countries.head(3)

# %%
# how many countries ?

countries.region.value_counts()

# %% [markdown]
# that is to say, 5 groups (at most)

# %% [markdown]
# your mission is to now show the same graphs, but with each bar split into up to 5, to reflect the relative usage of each region

# %% [markdown]
# ### attach a region to each lease
#
# most likely your first move is to tag all leases with a `region` column

# %%
# your code

# %%
# prune-cell

leases2 = leases.merge(countries, left_on='country', right_on='name')
leases2.drop(columns=['name'], inplace=True)
leases2

# %% [markdown]
# (label-sample-results)=
#
# ### visu by time and by region
#
# you can now produce the target figures; the expected final results looks like this
#
# ```{image} media/result-w.png
# ```
# ```{image} media/result-m.png
# ```
# ```{image} media/result-y.png
# ```

# %%
# your code

# %%
# prune-cell

for period in 'W', 'M', 'Y':
    # continue
    leases2['period'] = leases.beg.dt.to_period(period)
    draw_df = (
        leases2.pivot_table(
            values='duration',
            index='period',
            columns='region',
            aggfunc=sum,
        )
        .fillna(pd.Timedelta(0))
        .map(convert_timedelta_to_hours)
    )

    ax = draw_df.plot.bar(
        title=f"Duration in hours per {LEGEND[period]}",
        stacked=True,
    )
    ax.set_xticks(range(0, len(draw_df), SPACES[period]))
    plt.savefig(f"media/result-{period.lower()}.png")
    plt.show()
