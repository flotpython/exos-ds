---
jupytext:
  encoding: '# -*- coding: utf-8 -*-'
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
date: 2026/10/12
short_title: timeseries, irregular
---

# time series: events

```{admonition} to download
:class: warning

to work on this assignment locally, {download}`start by downloading the zip<./ARTEFACTS-timeseries-events.zip>`
```

In the previous assignment on time series, the data came **on a regular grid**: one measure each hour, one day after the other.  
Here we study a series where the timestamps are **not regular**: a catalog of **earthquakes**
in California, where each row is an *event* that happens whenever it happens.

In this assignment we practice

* recognizing that a series is **not on a fixed interval**, and measuring the gaps with `diff()`
* using `resample()` as the way to **turn events into a regular series** (counts, maxima per day, week, month)
* **zooming** on a burst of events
* **rolling** windows, that are defined by a duration rather than by a number of rows
* and, optionally, going back and forth between irregular and regular series with `reindex()`

here is the kind of picture we will end up with

<img src="media/quakes-daily.svg" width=600px>

```{code-cell} ipython3
import pandas as pd
import matplotlib.pyplot as plt

print(f"using pandas {pd.__version__}")

# time series look better in a wide figure
plt.rcParams["figure.figsize"] = (10, 4)
```

```{code-cell} ipython3
# optional
import itables
itables.init_notebook_mode()
```

## the data

+++

there is one file `data/quakes.csv`, with one row per earthquake of magnitude 2.5 or more
in California and surrounding areas, over one year (from 2025-10-01 to 2026-10-01)

| column | content |
|-|-|
| `time` | when the earthquake happened, in UTC |
| `latitude`, `longitude` | where |
| `depth` | in km |
| `mag` | the magnitude |
| `place` | a text description, like `"20 km ESE of Silver Springs, Nevada"` |
| `type` | the kind of event: nearly always `earthquake` |

+++

## 1. loading

+++

1. load the file into a dataframe `df`, and look at it; what is the type of the `time` column ?
1. turn the `time` column into timestamps, and use it as the index of `df`; make sure the index is sorted
1. the column `type` is nearly always `"earthquake"`; keep only these rows  
   (how many rows do you get rid of ? and what were they ?)

```{code-cell} ipython3
:tags: [level_basic]

# your code
```

:::{admonition} hint
:class: tip dropdown

compare with the previous assignment: here all the strings have the same ending (`Z` stands for UTC)  
so there is no need for any option and `pd.to_datetime()` just works
:::

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-begin
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 1.

df = pd.read_csv("data/quakes.csv")
df.head()
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 2.

df["time"] = pd.to_datetime(df.time)
df = df.set_index("time").sort_index()
df.index.dtype
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 3.

# what do we throw away
print(df[df.type != "earthquake"])

df = df[df.type == "earthquake"]
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

## 2. is it regular ?

+++

in the previous assignment we have used `asfreq()` or `date_range()` to check that we had one row per hour  
here we are in a different situation: the time between 2 consecutive rows is not constant

1. compute the time that separates 2 consecutive earthquakes as a `Series` named `gaps`  
   what is the type of the values in it ? (do we get durations ?)
1. express these gaps in **minutes**, as floats; what are the shortest, the longest, and the median gaps ?
1. draw a histogram of the gaps; what do you see ?

:::{admonition} hint
:class: tip dropdown

* `diff()` on a series of timestamps (a column, or `index.to_series()`) gives the difference with the previous row
* the `.dt` accessor has a method `total_seconds()` for durations
:::

```{code-cell} ipython3
:tags: [level_basic]

# your code
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-begin
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 1.

# the index is not a Series, so we convert it first
gaps = df.index.to_series().diff()
# the values are Timedelta objects
gaps.head()
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 2.

# the first row has no previous one, so the first gap is NaT, which describe() ignores
gaps_min = gaps.dt.total_seconds() / 60
gaps_min.describe()
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 3.

# most of the gaps are short - see the median - and some are very long
# because earthquakes come in bursts; a log scale helps see the long tail
gaps_min.plot.hist(bins=50, logy=True, xlabel="minutes since the previous earthquake");
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

## 3. from events to a regular series

+++

as we have seen, `resample()` is like a `groupby` where the groups are the time intervals  
it is the tool of choice to **go from events to a regular series**

1. compute `daily`, the **number of earthquakes per day**, and plot it  
   what is the busiest day ?
1. how many days have no earthquake at all ? is this a missing data issue, like in the previous assignment ?
1. compute and plot the **maximum magnitude per day**; how many `NaN` do you get, and why ?
1. same question (number of earthquakes) per week, and per month

:::{admonition} hint
:class: tip dropdown

* to count the rows in each group, you can use `.size()`
* `"D"` is the alias for days, `"W"` for weeks and `"ME"` for months
:::

```{code-cell} ipython3
:tags: [level_basic]

# your code
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-begin
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 1.

daily = df.resample("D").size()
daily.plot()
print(daily.idxmax(), daily.max())
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 2.

# this time, no: the count of events in an empty interval is a legitimate 0
# (we know that there was no earthquake)
(daily == 0).sum()
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 3.

# on the other hand, the maximum magnitude of no earthquake is undefined
max_mag = df.mag.resample("D").max()
print(max_mag.isna().sum())
max_mag.plot(marker=".", linestyle="");
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 4.

df.resample("W").size().plot(kind="bar")
df.resample("ME").size().plot(kind="bar");
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

## 4. zooming on a burst

+++

in the daily counts, you can see a peak, that corresponds to one big earthquake followed by its aftershocks

1. what is the date of the strongest earthquake, and what is its magnitude ?
1. select the rows from 1 hour before this earthquake until 6 hours after it  
   how many are they ? and what are the magnitudes of these ?
1. compute the number of earthquakes **per hour** in that window; what do you see ?

:::{admonition} hint
:class: tip dropdown

* `idxmax()` gives the index of the maximum, so here a timestamp
* you can add or remove a duration to a timestamp, e.g. with `pd.Timedelta("1h")`
:::

```{code-cell} ipython3
:tags: [level_basic]

# your code
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-begin
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 1.

big = df.mag.idxmax()
print(big, df.mag.max())
# or
df.nlargest(3, "mag")
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 2.

burst = df.loc[big - pd.Timedelta("1h"): big + pd.Timedelta("6h")]
print(len(burst))
burst[["mag", "place"]].head(10)
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 3.

# 1 hour before the big one, we had nothing; and then there is a burst, that fades out
burst.resample("h").mag.agg(["size", "max"])
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

## 5. rolling windows

+++

the daily counts are quite noisy; let us use a **rolling window** to smooth them, as we could do on a regular series  
but here a difference is that **the rows are not evenly spaced in time**, so a window of 7 rows is not a window of 7 days

1. compute `last_7d`, a dataframe with 2 columns `count` and `max`, which give, for each earthquake, the number of earthquakes and the maximum magnitude **over the last 7 days**  
   hint: `rolling()` accepts a duration, like `"7D"`, in place of a number of rows
1. plot the `count` column; what happens to it after the big earthquake ?
1. for comparison, what would be the meaning of `df.mag.rolling(7).max()` ? how long, on average, is the period that it covers ?

```{code-cell} ipython3
:tags: [level_basic]

# your code
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-begin
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 1.

# the window is expressed as a duration; this only works because the index is a DatetimeIndex
last_7d = df.mag.rolling("7D").agg(["count", "max"])
last_7d.head()
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 2.

# a sharp jump when the burst starts, and then it stays up for 7 days, and falls down as the burst gets out of the window
last_7d["count"].plot(ylabel="earthquakes over the last 7 days");
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 3.

# rolling(7) is the maximum over the last 7 EARTHQUAKES, which can be a couple of hours or some weeks
# depending on the period, so these values are not comparable with each other
# the average duration is about 7 times the mean gap
print(f"{7 * gaps_min.mean() / 60:.1f} hours on average")
```

```{code-cell} ipython3
:tags: [level_intermediate]

# generate the picture for the instructions, under a name with -auto
# (the name that is used in the instructions is a manual copy)
plt.rcParams["svg.hashsalt"] = "timeseries-events"
ax = daily.plot(alpha=0.4, label="earthquakes per day", figsize=(7, 3))
daily.rolling("7D").mean().plot(ax=ax, label="average over the last 7 days", legend=True)
ax.set_ylabel("number of earthquakes")
ax.figure.savefig("media/quakes-daily-auto.svg", metadata={"Date": None}, bbox_inches="tight")
plt.close(ax.figure)
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

## 6. back to a grid, with `reindex()` (optional)

+++

sometimes, we need to know **the state at some given times** - for example, what was the magnitude of the latest earthquake at midnight each day ?  
for this we need to build a regular index, and to "look up" in an irregular series

1. build `midnights`, the `DatetimeIndex` with one timestamp per day at midnight (UTC), from the first to the last day of the series  
   hint: `pd.date_range()`
1. what do you get with `df.mag.asfreq("D")`, or with `df.mag.reindex(midnights)` ? how many values are defined ? why ?
1. use `reindex()` with the option `method="ffill"` to get, for each midnight, the magnitude of the latest earthquake before that time

```{code-cell} ipython3
:tags: [level_basic]

# your code
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-begin
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 1.

first = df.index.min().normalize()
last = df.index.max().normalize()
midnights = pd.date_range(first, last, freq="D")
midnights[:3]
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 2.

# a reindex only looks for EXACT matches
# and no earthquake happens precisely at midnight
exact = df.mag.reindex(midnights)
print(exact.notna().sum())
# asfreq() is very similar, but starts at the first earthquake rather than at midnight
# so the first value is defined, and that is all
print(df.mag.asfreq("D").notna().sum())
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 3.

latest = df.mag.reindex(midnights, method="ffill")
print(latest.notna().sum())
latest.head()
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

## 7. the week at a glance (optional)

+++

do earthquakes occur more often at some hours, or some days ?  
since we are in California, let us look at the **local time** rather than UTC

1. convert the index to the time zone `"America/Los_Angeles"`, and add columns `hour` and `dayofweek` to `df`
1. build a dataframe with the 24 hours as rows and the 7 days of the week as columns, with the **number of earthquakes** in each cell  
   once with `pivot_table`, and once with `groupby` + `unstack`; check that you get the same
1. display that as a heatmap, using `sns.heatmap()` or `plt.imshow()`; what do you conclude ?

```{code-cell} ipython3
:tags: [level_basic]

# your code
```

:::{admonition} hint
:class: tip dropdown

to count with `pivot_table`, you can pass `aggfunc="count"`  
with `groupby`, you will use `size()`
:::

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-begin
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 1.

df.index = df.index.tz_convert("America/Los_Angeles")
df["hour"] = df.index.hour
df["dayofweek"] = df.index.dayofweek
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 2.

week = df.pivot_table(index="hour", columns="dayofweek", values="mag", aggfunc="count")
week2 = df.groupby(["hour", "dayofweek"]).size().unstack()
print(week.equals(week2))
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 3.

# no pattern, which is what we expect: earthquakes do not follow our working hours
# compare with the bikes of the previous assignment
import seaborn as sns

week.columns = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
sns.heatmap(week, cmap="viridis");
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

+++

## appendix: where the data comes from

+++

* the earthquakes come from the catalog of the *USGS* (US Geological Survey), that can be queried at  
  <https://earthquake.usgs.gov/fdsnws/event/1/>
* the script `fetch-data.py`, that comes with this assignment, was used to acquire this data
  - it selects a rectangle around California (so that you see some events in Nevada and Mexico too)
  - and only the events with a magnitude of 2.5 or more
* the data is frozen, no need to refresh it
