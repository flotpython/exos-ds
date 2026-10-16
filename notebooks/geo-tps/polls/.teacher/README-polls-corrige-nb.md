---
jupytext:
  custom_cell_magics: kql
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.3
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

+++ {"editable": true, "slideshow": {"slide_type": ""}}

# US polls with altair

+++

```{admonition} download the zip
:class: warning

to run this code on your own laptop,
{download}`start with downloading the zip file<./ARTEFACTS-polls.zip>`
```

```{code-cell} ipython3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import geopandas as gpd

# activate this if running under jlab
# %matplotlib ipympl
```

## 1. loading presidential averages

538.com - actually <http://fivethirtyeight.com> - was a site that published data about the US presidential election  
the site is no longer online, so we use a copy of its **presidential averages** that is stored in `data/DATA.csv`

load this file into a dataframe `df`; make sure to
- be careful about the types of the columns, in particular `date`, that must be a proper timestamp
- notice that the first column is a leftover index, and so ensure it does not end up as a column in `df`

```{code-cell} ipython3
:tags: [level_basic]

# your code
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-cell

# in a single shot

df = pd.read_csv("data/DATA.csv", index_col=0, parse_dates=["date"])

df.head(2)
```

## 2. plotting

And what we want to do is to plot the average of the polls for each candidate.  
In other words, you should obtain something like this - we will arbitrarily focus on the 2024 year only

```{image} media/polls-over-time-2024.png
:width: 800px
:align: center
```

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

# extract 2024
# note that the sorting is probably optional

df = df[df.date.dt.year >= 2024].sort_values("date")
df.head(2)
```

```{code-cell} ipython3
:tags: [level_intermediate]

# pivot and plot
#
# note that this averages all the rows we have for a given day and candidate
# which includes the national polls, but also all the states

(df
    .pivot_table(
        values='pct_estimate',
        aggfunc='mean',
        index='date',
        columns='candidate'
    )
).plot(figsize=(10, 4))

# this saved version is the one shown above (after a manual copy)
plt.savefig('media/polls-over-time-2024-auto.png')
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

## 3. use interactivity

using the interactive view (if under Jupyter Lab) make sure to use `%matplotlib ipympl`, and zoom into the figure and retrieve
- the date for the last data about Joe Biden
- the date for the first data about Kamala Harris

```{code-cell} ipython3
:tags: [level_basic]

# your answer in english - as a comment
# ...
```

also write a line of code to compute this second date

```{code-cell} ipython3
:tags: [level_basic]

# your code

first_harris_date = ...
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-begin
```

```{code-cell} ipython3
:tags: [level_intermediate]

df.candidate.value_counts()
```

```{code-cell} ipython3
:tags: [level_intermediate]

first_harris_date = df[df.candidate == "Harris"].date.min()
first_harris_date
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

## 4. race end

from this part we will focus on the period after `first_harris_date`
1. how many candidates are still in the data ?
1. make sure to keep only the 2 most famous ones
1. how many data points do we have now for each of them ?

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

df = df[df.date >= first_harris_date]
df.value_counts("candidate")
```

```{code-cell} ipython3
:tags: [level_intermediate]

# a more robust way than removing Kennedy by name
df = df[df.candidate.isin(["Harris", "Trump"])]
df.value_counts("candidate")
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

## 5: loading shapefiles with geopandas

```{code-cell} ipython3
# here's the typical nickname for geopandas

import geopandas as gpd
```

we want to plot this data on a geographic map; first we need a definition of the various US states; this comes from the US Census Bureau (file `us-states.zip`), and we have a copy of it under `data/`

we load this shapefile into a geopandas object

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
---
gdf = gpd.read_file("data/us-states.zip")
```

1. how many entries ?

```{code-cell} ipython3
:tags: [level_basic]

# your code
```

```{code-cell} ipython3
---
tags: [level_intermediate]
editable: true
slideshow:
  slide_type: ''
---
# prune-cell

gdf.head(2)
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-cell 1.

len(gdf)
```

2. what are the various column types

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-cell 2.

gdf.dtypes
```

as you can see, this is almost like a regular dataframe, except for the `geometry` column; which is a geographic entity, hence the term `geo-dataframe`

+++

## digression: using altair to produce a geographic viz

```{admonition} this may require an installation
:class: dropdown tip
of course you might have to install `altair`...  how do you go about doing that again ?
```

````{admonition} see also on altair and its use on geographic data
:class: dropdown warning

more details on this topic can be found here: 

- <https://altair-viz.github.io/user_guide/marks/geoshape.html>
- <https://idl.uw.edu/visualization-curriculum/altair_cartographic.html>
- <https://altair-viz.github.io/altair-tutorial/notebooks/09-Geographic-plots.html>
````

```{code-cell} ipython3
import altair as alt

# this is for rendering altair charts within the notebook
alt.renderers.enable("html")
```

Here are a few examples of what we can do with this library

+++

### the simplest chart

```{code-cell} ipython3
# to show a geographic map from that geo-df
# (suboptimal, we'll improve that...)

# we could just write this and it would render
# alt.Chart(gdf).mark_geoshape()

# but we can also this more usual form

chart = (
    alt.Chart(gdf)
    .mark_geoshape()
)

chart.display()
```

### improving that view

+++

now in terms of presentation, it is a little suboptimal, let's improve this a bit

```{code-cell} ipython3
# we can improve by:
# (1) setting a width
# (2) using the albersUsa projection, which puts Alaska and Hawai under mainland
#     this way we use space more effectively
# NOTE that in the process Alaska is artificially shrunk down
#      it's actually the largest US state
(
    alt.Chart(gdf)
    .mark_geoshape()
    .properties(width=600)
    .project('albersUsa')
)
```

### using colors

+++

now, the initial geo-dataframe has some numeric values, that we can use to color the map !  
for example, there are `AWATER` and `ALAND`  
which we can interpret as meaning *area of water* (as in lakes) and *area of land* respectively

```{code-cell} ipython3
gdf.head(2)
```

and we can use one of these to color the different states  
for that we would use `encode()` like so

```{code-cell} ipython3
(
    alt.Chart(gdf)
    .mark_geoshape()
    .encode(
        color="ALAND:Q",          # Q stands for quantitative
    )
    .properties(width=600)
    .project('albersUsa')
)
```

### better with a legend

```{code-cell} ipython3
# or if we prefer, same result essentially
# but this way we can be more descriptive

(
    alt.Chart(gdf)
    .mark_geoshape()
    # legend
    .encode(
        color=alt.Color(field="ALAND", type="quantitative", title="land area")
    )
    # a bit narrower so the legend shows up
    .properties(width=600)
    .project('albersUsa')
)
```

### even better with tooltips

```{code-cell} ipython3
# also useful with altair, we can give a `tooltip` parameter to encode
# and this shows when your mouse hovers on a state

# NOTE: altair can only see the columns, not the index
# so as we want to show the name of the state, we need it in a regular column
# so you had made the choice to use the state as the index
# you may need to reset_index()

(
    alt.Chart(gdf)
    .mark_geoshape()
    .encode(
        color=alt.Color(field="AWATER", type="quantitative", title="water area"),
        # and we can show there anything from the table
        tooltip=["NAME", "ALAND"],
    )
    .properties(width=600)
    .project('albersUsa')
)
```

## our goal: geographic rendering

in this following we will produce a summary map, which looks like this:
- for all the states where we have data
- the color depicts the ratio between, Harris's and Trump's average scores over time
- also the tooltips allow to expose more details on the individual results

```{image} media/states-with-data.png
:width: 800px
:align: center
```

+++

## 6. first map

+++

1. for how many states do we have polls data ? which are they ?

```{code-cell} ipython3
:tags: [level_basic]

# your code
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-cell

df.state.nunique()
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-cell

df.state.unique()
```

2. for this data, compute a table with the state as index, and the two contestants polls (averaged)

```{code-cell} ipython3
:tags: [level_basic]

# your code
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-cell

# compute a dataframe, indexed by the state name
# state-name -> average-harris average-trump

pivot = df.pivot_table(
    values="pct_estimate",
    index="state",
    columns=["candidate"],
)
pivot.head()
```

3. using what you've seen in the digression, and what you will gather if needed on the Internet,  produce the above map

```{code-cell} ipython3
:tags: [level_basic]

# your code
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-cell

# both dataframes are indexed by the state name, so we can join on the index
# the (inner) join keeps only the rows with a match, so 'National' and the like are dropped

# note that we do not do how="right" since fake entries like "National" 
# would show up in that case

gdf_scores = gdf.merge(pivot, left_on="NAME", right_index=True, how="inner")
gdf_scores['ratio'] = gdf_scores['Harris'] / gdf_scores['Trump']
gdf_scores.head(2)
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-cell

# just apply the recipe

chart = (
    alt.Chart(gdf_scores)
    .mark_geoshape(stroke='blue')
    .encode(
        color=alt.Color(field="ratio", type="quantitative", title="Harris / Trump"),
        tooltip=["Harris", "Trump", "NAME"],
    )
    .properties(width=600)
    .project('albersUsa')
)

# just to produce the figure
chart.save("media/states-with-data-auto.png")

chart
```

## 7. outlining swing states

+++

from the graph above, we want to outline the swing states  
for example, we could come up with something like

```{image} media/swing-states-outlined.png
:width: 800px
:align: center
```

````{admonition} *hints*
:class: dropdown

- the method `pd.Series.isin()` might come in handy for this step
- also you will probably need to search a bit by yourself, outside of what we've covered in the digression
````

```{code-cell} ipython3
SWING_STATES = [
    'Nevada',
    'Arizona',
    'Wisconsin',
    'Michigan',
    'Pennsylvania',
    'Georgia',
    'North Carolina',
]
```

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

# store 'is a swing state' in a new bool column

gdf_scores['swing'] = gdf_scores.NAME.isin(SWING_STATES)
```

```{code-cell} ipython3
:tags: [level_intermediate]

chart = (
    alt.Chart(gdf_scores)
    .mark_geoshape(stroke='blue')
    .encode(
        color=alt.Color(field="ratio", type="quantitative", title="Harris / Trump"),
        tooltip=["Harris", "Trump", "NAME"],
        stroke=alt.condition("datum.swing", alt.value("black"), alt.value("white")),
        strokeWidth=alt.condition("datum.swing", alt.value(2), alt.value(0.3)),
    )
    .properties(width=600)
    .project('albersUsa')
)

# just to produce the figure
chart.save("media/swing-states-outlined-auto.png")

chart
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-end
```

## 8. filling gaps (optional)

this is not very readable; instead we want to still get the missing states show up in gray,  
and to keep the outlining of the swing states, i.e.

```{image} media/all-states.png
:width: 800px
:align: center
```

```{admonition} tip
:class: dropdown tip
this one is less obvious, and you are allowed to use an IA to find the solution !
```

```{code-cell} ipython3
:tags: [level_basic]

# your code
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-cell

# use how=left on purpose so we get 52 rows in the result

gdf_scores = gdf.merge(pivot, left_on="NAME", right_index=True, how="left")
gdf_scores['ratio'] = gdf_scores['Harris'] / gdf_scores['Trump']
gdf_scores['swing'] = gdf_scores.NAME.isin(SWING_STATES)
```

```{code-cell} ipython3
:tags: [level_intermediate]

# prune-cell

# we can use a layered approach, i.e. build 2 charts
# and display the sum (superposition) of them

# layer 1: the missing states
base = (
    alt.Chart(gdf)
    .mark_geoshape(fill="lightgray", stroke="white")
)

# layer 2: the states with data, with the swing states outlined as before
colored = (
    alt.Chart(gdf_scores)
    .mark_geoshape(stroke="blue")
    .encode(
        color=alt.Color(field="ratio", type="quantitative", title="Harris / Trump"),
        tooltip=["Harris", "Trump", "NAME"],
        stroke=alt.condition("datum.swing", alt.value("black"), alt.value("white")),
        strokeWidth=alt.condition("datum.swing", alt.value(2), alt.value(0.3)),
    )
)

# this '+'   ↓↓↓  is what creates the layered graph
chart = (base + colored).properties(width=600).project("albersUsa")

# just to produce the figure
chart.save("media/all-states-auto.png")

chart
```
