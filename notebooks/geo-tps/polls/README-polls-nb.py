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
# # data from 538.com with altair

# %% [markdown]
# to run this code on your own laptop,
# {download}`start with downloading the zip file<./ARTEFACTS-polls.zip>`

# %%
import pandas as pd
import matplotlib.pyplot as plt

# activate this if running under jlab
# # %matplotlib ipympl

# %% [markdown]
# ## presidential averages
#
# 538.com - actually it is <http://fivethirtyeight.com> - is a site hosted by ABC news, that exposes data about the US presidential election
#
# we're gonna use the data in this URL:

# %%
URL = "https://projects.fivethirtyeight.com/polls/data/presidential_general_averages.csv"

# %% [markdown]
# ```{admonition} update 2025
#
# initially we would have written a function that loads this URL; it would
#
# - cache it on your hard drive so you can reload it faster
# - do any type conversion that you see fit
#
# as of 2025 **this URL is no longer online** so we'll just 
#
# - load the data from `data/DATA.csv`
# - still be careful about the columns types
# ```

# %% tags=["level_basic"]
# your code

CACHE = "data/DATA.csv"

# %% [markdown]
# And what we want to do is to plot the average of the polls for each candidate.  
# In other words, you should obtain something like this - we will arbitrarily focus on the 2024 year only
#
# ```{image} media/polls-over-time-2024.png
# :width: 800px
# :align: center
# ```

# %% tags=["level_basic"]
# your code

# %% [markdown]
# using the interactive view (after all we are using `%matplotlib ipympl`), zoom into the figure and retrieve
# - the date for the last data about Joe Biden
# - the date for the first data about Kamala Harris
#
# also write a line of code to compute this second date

# %% tags=["level_basic"]
# your code

first_harris_date = ...

# %% [markdown]
# ## race end
#
# from this part we will focus on the period after `first_harris_date` 

# %% tags=["level_basic"]
# your code

# %% [markdown]
# how many candidates are still in the data ?  
# make sure to keep only the 2 most famous ones

# %% tags=["level_basic"]
# your code

# %% [markdown]
# ## geographic rendering
#
# in this section we will produce a summary map, which looks like this  
# the color depicts the ratio between, otoh Harris's average score over time, and otoh Trump's  
# also the tooltips allow to expose more details on the individual results
#
# ```{image} media/polls-over-space-2024.png

# %% [markdown]
# ### digression 1: loading shapefiles with geopandas

# %%
# here's the typical nickname for geopandas

import geopandas as gpd

# %% [markdown]
# first we need a definition of the various US states; there is one here

# %% [markdown]
# ```{admonition} update 2025
#
# here again, there's been a change since 2024: this URL no longer comes with a valid SSL certificate  
# so we'll use the version stored under `data/` again
#
# ```

# %%
# no longer easily readable by geopandas because of an SSL certificate issue
US_STATES_SHAPEFILE_URL = "https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_state_20m.zip"

US_STATES_SHAPEFILE_CACHE = "data/us-states.zip"

# %% [markdown]
# and we can load it like so:

# %%
# so instead of doing this
# gdf = gpd.read_file(US_STATES_SHAPEFILE_URL)

# we'll do this
gdf = gpd.read_file(US_STATES_SHAPEFILE_CACHE)

# and we get this
gdf.head()

# %% [markdown]
# so as you can see this is almost like a regular dataframe, except for the `geometry` column; which is a geographic entity, hence the term `geo-dataframe`

# %% [markdown]
# ### digression 2: using altair to produce a geographic visualization
#
# of course you might have to install `altair`...  how do you go about doing that again ?
#
# ````{admonition} see also
# :class: dropdown
#
# more details on this topic can be found here: 
#
# - <https://altair-viz.github.io/user_guide/marks/geoshape.html>
# - <https://idl.uw.edu/visualization-curriculum/altair_cartographic.html>
# - <https://altair-viz.github.io/altair-tutorial/notebooks/09-Geographic-plots.html>
# ````

# %%
import altair as alt

# this is for rendering altair charts within the notebook
alt.renderers.enable("html")

# %%
# to show a geographic map from that geo-df

alt.Chart(gdf).mark_geoshape()

# %%
# or we can also use it like this if we prefer

chart = (
    alt.Chart(gdf)
    .mark_geoshape()
)

chart.display()

# %% [markdown]
# now in terms of presentation, it is a little suboptimal, let's improve this a bit

# %%
(
    alt.Chart(gdf)
    .mark_geoshape()
    .properties(width=800)
    .project('albersUsa')
)

# %% [markdown]
# now, the initial geo-dataframe has some numeric values, that we can use to color the map !
#
# for example, there are `AWATER` and `ALAND` - that I take it mean *area of water* and *area of land* respectively  
# and we can use one of these to color the different states
#
# for that we just do, like for simpler altair plots we call `encode()` like so

# %%
(
    alt.Chart(gdf)
    .mark_geoshape()
    .encode(
        color="ALAND:Q",          # Q stands for quantitative
    )
    .properties(width=800)
    .project('albersUsa')
)

# %%
# or if we prefer, same result essentially
# but this way we can be more descriptive

(
    alt.Chart(gdf)
    .mark_geoshape()
    .encode(
        color=alt.Color(field="ALAND", type="quantitative", title="land area")
    )
    .properties(width=800)
    .project('albersUsa')
)

# %%
# also useful with altair, we can give a `tooltip` parameter to encode
# and this shows when your mouse hovers on a state

(
    alt.Chart(gdf)
    .mark_geoshape()
    .encode(
        color=alt.Color(field="AWATER", type="quantitative", title="water area"),
        # and we can show there anything from the table
        tooltip=["NAME", "ALAND"],
    )
    .properties(width=800)
    .project('albersUsa')
)

# %% [markdown]
# ### back to our data

# %% [markdown]
# given this knowledge, you should be able to produce our target graph, namely again
#
# ```{image} media/polls-over-space-2024.png
# :width: 800px
# :align: center
# ```

# %% tags=["level_basic"]
# your code

# %% [markdown]
# ## focusing on swing states

# %% [markdown]
# from the graph above, keep only the following states
#
# ````{admonition} *hint*
# :class: dropdown
#
# the method `pd.Series.isin()` might come in handy for this step
# ````

# %%
SWING_STATES = [
    'Nevada',
    'Arizona',
    'Wisconsin',
    'Michigan',
    'Pennsylvania',
    'Georgia',    
    'North Carolina',
]

# %% tags=["level_basic"]
# your code
