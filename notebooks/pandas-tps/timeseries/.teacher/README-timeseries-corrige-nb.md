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
short_title: timeseries, regular
---

# time series, the basics

```{admonition} to download
:class: warning

to work on this assignment locally, {download}`start by downloading the zip<./ARTEFACTS-timeseries.zip>`
```

In this assignment we study **cycling in Paris**, using the hourly counts of one of the
bike counters that the city has installed in its streets.

This is a *first contact* with time series in pandas; we will practice

* **parsing** strings into timestamps, and dealing with time zones
* the **`.dt` accessor**, to extract the hour, the day of the week, etc.
* **slicing** a dataframe on its time index
* **`resample()`**, to aggregate by day, week, month
* and finally **joining** with another time series, daily weather data

the companion assignment *time series: events* deals with series that are **not** on a regular grid

here is the kind of pictures we will end up with

<img src="media/hourly-profile.svg" width=500px>

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

## 0. the data

+++

there are two files in the `data/` folder

| file | one row per | columns |
|-|-|-|
| `bike-counter.csv` | hour | `timestamp`, `count` (number of bikes that went through the counter) |
| `weather.csv` | day | `jour`, `temperature` (°C, daily mean), `rain_mm` (daily total) |

the counter is on the *voie Georges Pompidou*, along the Seine; it counts the bikes going in one direction only  
we start with the first one

+++

## 1. parsing the timestamps

+++

### loading

+++

1. load `data/bike-counter.csv` into a dataframe named `df`
1. look at the first rows and at the types of the columns - what is the type of the `timestamp` column ?
1. the name `count` is unfortunate, because `df.count` is a method of the dataframe;  
   rename that column into `n_bikes`

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

df = pd.read_csv("data/bike-counter.csv")
df.head()
```

```{code-cell} ipython3
:tags: [level_intermediate]

# the timestamps are just strings, i.e. dtype `str`

df.dtypes
```

```{code-cell} ipython3
:tags: [level_intermediate]

df = df.rename(columns={"count": "n_bikes"})
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

### converting

+++

we want to turn the `timestamp` column into actual timestamps

1. use `pd.to_datetime()` for that; what do you get ? read the message carefully
1. look at the strings in the data: apart from the date and the hour, what else is there ?  
   how many different values are there for that part ? can you guess why ?

```{code-cell} ipython3
:tags: [level_basic]

# your code
```

:::{admonition} hint
:class: tip dropdown

the last 6 characters of a string can be obtained with `df.timestamp.str[-6:]`  
and then you can use `value_counts()`
:::

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-begin
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 1.

# this fails: the strings do not all have the same time zone offset,
# and pandas refuses to guess what we want (we will fix this in a bit)
# NOTE: with pandas 2 this would only issue a warning and return an object column,
# and pandas 3 makes it an error
try:
    pd.to_datetime(df.timestamp)
except ValueError as exc:
    print("OOPS", type(exc), exc)
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 2.

# the offset is +01:00 in winter and +02:00 in summer, because of the daylight saving time
df.timestamp.str[-6:].value_counts()
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

### converting, again

+++

pandas has a hard time with a column that mixes several time zone offsets  
the way out is to ask for everything to be expressed in UTC, using the `utc=True` option

1. redo the conversion with that option, and store the result back into the `timestamp` column;  
   what is the dtype now ?
1. we are interested in the **local time** in Paris, since this is when people go to work  
   convert that column to the timezone `"Europe/Paris"`  
   you will need to find the right method in the `.dt` accessor (or do a search on `tz_convert`)

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

df["timestamp"] = pd.to_datetime(df.timestamp, utc=True)
df.dtypes
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 2.

df["timestamp"] = df.timestamp.dt.tz_convert("Europe/Paris")
df.head()
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

+++

## 2. the `.dt` accessor

+++

now that `timestamp` has a proper type, the `.dt` accessor gives us access to all the details  
add these columns to `df`

| column | content |
|-|-|
| `hour` | the hour of the day, 0 to 23 |
| `weekday` | the day of the week, as a string like `"Monday"` |
| `is_weekend` | a boolean, `True` on Saturday and Sunday |
| `month` | the month, as a number 1 to 12 |

```{code-cell} ipython3
:tags: [level_basic]

# your code
```

:::{admonition} hint
:class: tip dropdown

* `.dt.hour`, `.dt.month` are attributes
* `.dt.day_name()` is a method, and there is also an attribute `.dt.dayofweek` that returns a number with 0 for Monday
:::

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-begin
```

```{code-cell} ipython3
:tags: [level_intermediate]

df["hour"] = df.timestamp.dt.hour
df["weekday"] = df.timestamp.dt.day_name()
df["is_weekend"] = df.timestamp.dt.dayofweek >= 5
df["month"] = df.timestamp.dt.month
df.head()
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

### the hourly profile

+++

1. what is the average number of bikes **per hour of the day** ? use a `groupby` and plot the result with `.plot()`  
   what are the busiest hours ? does that match your expectations ?
1. now do the same but separately for week days and for week ends, so that both curves show on the same plot  
   we expect something like the picture in the introduction

:::{admonition} hint
:class: tip dropdown

for the second question, group by 2 criteria, and think about `unstack()` to get 2 columns  
this is the same trick as what we have seen with `pivot_table`
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
# two peaks, around 8-9 and 18-19, the commute

df.groupby("hour").n_bikes.mean().plot(kind="bar");
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 2.

profile = df.groupby(["is_weekend", "hour"]).n_bikes.mean().unstack(0)

# or, equivalently, with a pivot_table
profile2 = df.pivot_table(
    index="hour", columns="is_weekend", values="n_bikes", aggfunc="mean")
print(profile.equals(profile2))

profile.columns = ["week days", "week ends"]
profile.plot(grid=True, ylabel="average number of bikes");
```

```{code-cell} ipython3
:tags: [level_intermediate]

# generate the picture for the instructions, under a name with -auto
# (the name that is used in the instructions is a manual copy)

plt.rcParams["svg.hashsalt"] = "timeseries"
ax = profile.plot(
   grid=True,
   ylabel="average number of bikes",
   xlabel="hour of the day",
   xticks=range(0, 24, 3),
   figsize=(6, 3.5))
ax.figure.savefig("media/hourly-profile-auto.svg", metadata={"Date": None}, bbox_inches="tight")
plt.close(ax.figure)
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

## 3. using the time as the index

+++

it is very common to use the timestamps as the index of a time series; this makes slicing very convenient

1. make `timestamp` the index of `df`
1. make sure the index is sorted in chronological order (check that with `index.is_monotonic_increasing`)
1. what are the first and the last timestamps ? so, how long is the period covered ?

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

df = df.set_index("timestamp")
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 2.

print(df.index.is_monotonic_increasing)
# in the general case you would need to do
df = df.sort_index()
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 3.

print(df.index.min(), df.index.max())
print(df.index.max() - df.index.min())
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

### missing data

+++

this is a counter that sits in the street, so there can be some missing data  
we expect one row per hour

1. how many rows would you expect between the first and the last timestamp ? how many do we have ?
1. how many rows contain `NaN` in the `n_bikes` column ?
1. which days are entirely missing ?

:::{admonition} hint
:class: tip dropdown

* `pd.date_range()` can create the index with all the hours; use the option `freq="h"`
* or use `df.asfreq("h")`, that creates the missing rows with `NaN` in it
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

expected = pd.date_range(df.index.min(), df.index.max(), freq="h")
print(f"expected {len(expected)}, got {len(df)}, diff={len(expected)-len(df)}")
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 2.
# so we have 2 kinds of missing data:
# missing rows, and rows with no data in them

print(df.n_bikes.isna().sum())
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 3.
# we make the missing rows appear

hourly = df.asfreq("h")
missing = hourly[hourly.n_bikes.isna()]
print(len(missing))

# a day is completely missing if we have 24 of these
# note that the index is a DatetimeIndex, so we have .date and similar attributes right on it
per_day = missing.groupby(missing.index.date).size()
per_day[per_day == 24]
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

## 4. slicing

+++

now that we have a time index, we can slice with `.loc[]` using strings that look like dates  
let us practice, using `df.loc[...]` to answer these questions

1. what are the total number of bikes counted in December 2025 ?
1. how many rows do we have between January 1st and January 7th 2026 (both included) ?  
   is the end of the slice included or not ?
1. how many bikes in total in the morning rush, i.e. between 7:00 and 10:00 (all days included) ?
1. how many rows do we have on 2026-03-29 ? and on 2025-10-26 ? why is that ?

:::{admonition} hint
:class: tip dropdown

for question 3, you can build a mask from the hour of the day, which is available
as an attribute of the index (`df.index.hour`) or from the column we have created earlier  
and if you like, there is also a method `between_time()` that does it directly
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
# a partial date designates the whole month

df.loc["2025-12", "n_bikes"].sum()
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 2.
# with strings, the end of the slice is inclusive, and the whole day is included
# so we have 7 * 24 rows (if no hour is missing)

len(df.loc["2026-01-01":"2026-01-07"])
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 3.
# note that 7:00 and 10:00 are both included
# so, as we have one row per hour, that means the hours 7, 8, 9 and 10

# with a mask on the hour; here we use the attribute of the index
mask = (df.index.hour >= 7) & (df.index.hour <= 10)
print(df.loc[mask, "n_bikes"].sum())

# or the same with the column
print(df.loc[df.hour.between(7, 10), "n_bikes"].sum())

# or, using a dedicated method, that is specific to time series
print(df.between_time("07:00", "10:00").n_bikes.sum())
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 4.
# the day we move to summer time (+1h), there are only 23 hours between midnight and midnight
# and the one when we go back to winter time has 25 - but our data has a hole on that day

print(len(df.loc["2026-03-29"]))
print(len(df.loc["2025-10-26"]))
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

### is the practice growing ? (optional)

+++

our data covers the period from September 12th to October 11th **twice**: in 2025 and in 2026  
compare the total number of bikes in each of these 2 periods

```{code-cell} ipython3
:tags: [level_basic]

# your code
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-cell

before = df.loc["2025-09-12":"2025-10-11", "n_bikes"].sum()
after = df.loc["2026-09-12":"2026-10-11", "n_bikes"].sum()
# beware that there are missing days, so this is not rigorous
print(before, after, f"{after / before - 1:.1%}")
```

## 5. resampling

+++

`resample()` is like a `groupby`, where the groups are time intervals; it is the tool of choice to change the granularity of a time series  
so, to move from one point per hour to one point per day

1. compute `daily`, the total number of bikes per day (a `Series`), and plot it
1. what is the busiest day ? and the least busy one ?  
   hint: `idxmax()` and `idxmin()`

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

daily = df.n_bikes.resample("D").sum()
daily.plot();
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 2.

print("busiest:", daily.idxmax(), daily.max())
print("least busy:", daily.idxmin(), daily.min())
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

### beware of the missing data

+++

some days have **no bike at all**, which is suspicious - recall that some days were missing entirely  
on the plot above they show as a few sharp drops down to 0, in the late summer and in the fall

1. which are these days ? what happened ? what does `sum()` return on a group with no data at all ?
1. fix `daily` so that these days show up as `NaN` rather than 0  
   hint: look at the options of `sum()`
1. plot again, but only the last 2 months, and with `marker="."` to see the individual points;  
   what does `plot()` do with a `NaN` ?

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
# the sum of nothing is 0; so a day with no data at all is accounted for as having no bike
# which is not true, we do not know

daily[daily == 0]
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 2.

daily = df.n_bikes.resample("D").sum(min_count=1)
print(daily.isna().sum())
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 3.

# a NaN is not drawn: the line is interrupted, and so we see a gap
# there is no line to or from the missing point, and it is not interpolated either
# with a single missing day, the 2 segments around it are lost, so the gap is 2 days wide
# on the full plot this is hardly visible, which is why we zoom in
daily.loc["2026-08-10":].plot(marker=".");
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

### weekly and monthly

+++

1. compute and plot the number of bikes per week, and per month  
   in the resulting series, what is the first date for a month ? and for a week ?
1. the first and last months are not complete; in addition, the months have different lengths  
   so a monthly total is not the best way to compare them; compute the **average per day** instead  
   hint: you can use `daily`
1. make a dataframe with 3 columns `total`, `mean` and `max` giving, for each month, the corresponding aggregates of the daily numbers  
   hint: `agg()`

```{code-cell} ipython3
:tags: [level_basic]

# your code
```

:::{admonition} hint
:class: tip dropdown

the aliases for the frequency are `"W"` for weeks, and `"ME"` for the end of the months  
(`"MS"` for the start of the months); in older versions of pandas it was `"M"`
:::

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-begin
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 1.

weekly = df.n_bikes.resample("W").sum(min_count=1)
monthly = df.n_bikes.resample("ME").sum(min_count=1)
weekly.plot(kind="bar")
monthly.plot(kind="bar");
# the label is the END of the interval: weeks end on a Sunday, and months on the last day
# the first/last intervals are partial
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 2.

daily.resample("ME").mean().plot(kind="bar");
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 3.

daily.resample("ME").agg(["sum", "mean", "max"])
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

## 6. adding the weather

+++

does the weather make a difference ? let us find out with the second file

1. load `data/weather.csv` into a dataframe `weather`, and make sure the column `jour` becomes a proper timestamp  
   careful with the format: `12/09/2025` is meant to be September 12th; what would happen if pandas chose to read it as December 9th ?  
   use the `format=` option of `pd.to_datetime` to say what you mean
1. make that column the index of `weather`
1. combine `daily` and `weather` into one dataframe `both`, with the 3 columns `n_bikes`, `temperature` and `rain_mm`  
   at that point you may run into an issue with the indexes - that is because one has a time zone, and the other one has not  
   we recommend to remove the time zone from `daily`, you can use `tz_localize(None)` on its index

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

weather = pd.read_csv("data/weather.csv")
weather["jour"] = pd.to_datetime(weather.jour, format="%d/%m/%Y")
weather.head(3)
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 2.

weather = weather.set_index("jour")
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 3.
# the index of daily has a timezone, but not the one of weather
# so they are not comparable, and the join would not match any row
# the timezone has no use for days, so we can remove it

daily_naive = daily.copy()
daily_naive.index = daily_naive.index.tz_localize(None)

both = pd.concat([daily_naive, weather], axis=1)
# or equivalently
# both = weather.join(daily_naive)
both.head(3)
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

### a look at the result

+++

1. are there less bikes on rainy days ?  
   let us say a day is rainy if there is more than 1mm of rain  
   compare the average number of bikes on rainy days and on other days
1. draw a scatter plot of the number of bikes against the temperature, using `df.plot.scatter()` or similar
1. what is the correlation between the 3 columns ?  
   hint: `corr()`

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

both.groupby(both.rain_mm > 1).n_bikes.mean()
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 2.

both.plot.scatter(x="temperature", y="n_bikes", alpha=0.5);
```

```{code-cell} ipython3
:tags: [level_intermediate]

# 3.
# a weak but visible effect: warmer is better, rain is worse

both.corr()
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

## appendix: where the data comes from

+++

* the bike counts come from the open data portal of the city of Paris, dataset *comptage vélo - données compteurs*  
  <https://opendata.paris.fr>
* the weather comes from the *Open-Meteo* archive API, for Paris  
  <https://open-meteo.com>
* the script `fetch-data.py`, that comes with this assignment, was used to acquire this data
  - it picks one counter, and exports the hours in local time **with the UTC offset**, as the original does
  - and it writes the days of the weather in the French format on purpose
* the data is frozen, no need to refresh it
