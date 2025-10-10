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

# using altair

CURRENT STATUS:

xxx

in order to produce such a visu from our data, we need to mess with it due to

- need to compute the duration (can that be done in altair ?)
- some apparent limitations of altair, particularly regarding the .dt accessor details

so it's kind of ruining the point that we wanted to make, namely that a standalone HTML page could be built to fetch and display the data

So, I am leaving it as-is for now...

It's probably best to build a completely new TP instead of this initial idea of enhancing one,
as the point of grouping over time has been addressed already in the first part of the leases thing

the beginning with fastapi is probably allright - except for the actual URLs and data scheme and so on

xxx

+++

# grouping through time and category - altair + fastapi version

to work on this assignment locally on your laptop, {download}`start with downloading the zip<./ARTEFACTS-leases-altair.zip>`

this is a follow-up on [the first TP on leases](#label-tp-leases)

we'll do the same kind of visualisation, but this time we'll use

- a dynamic source - as opposed to a static .csv file
  this is achieved through a fastapi web service
- altair / vega-lite as the visualisation library

one of the pros of using altair is the ability to produce an interactive visualisation as a self-contained HTML file

+++

## dependencies

you may need to

```bash
pip install "fastapi[standard]" altair
```

+++

## imports

```{code-cell} ipython3
import pandas as pd

# here is how to import altair
import altair as alt
```

## the fastapi web service

we provide you with the source code for a small web service that is able to produce random data for the leases, in a format compatible with the one in `leases.csv`  
this is the purpose of `fastapi_random_server.py`

+++

### how to start

assuming you have installed fastapi as above, you can start the web service by typing in your terminal

```bash
fastapi dev fastapi_random_server.py
```

this will behave a bit like `jupyter lab`, in that it will

- start a web server
- display the URL to use to join it
- and it will *block*, meaning the terminal is busy, and no longer responding to your commands

so first off, leave this terminal running, and create another one if needed

+++

### how to use

inside the terminal where you triggered the server, you'll see a URL  
something like <http://localhost:8000/>  
just open a web browser and cut-n-paste that URL 

```{admonition} link maybe clickable ?
:class: dropdown tip

in some terminal setups, you may be able to e.g. Command-click or Alt-click on the link in the terminal to open it in your browser (this is rather likely on linux and MacOS, not sure wbout Windows)
```

as you might have guessed now, this means

- use the http protocol
- to reach a service running on the computer named `localhost` (your own laptop, that is)
- on port 8000

```{admonition} what are ports ?
ports is a very simple mechanism to allow your computer to run many different services (in real life, you would typically have ssh on port 22, web on port 443, dns on port 53, and so on..)
```

+++

### the source code: routes

take a look at the source code for the server, and observe the occurrences of `@app.route`  
this the mechanism offered by the fastapi layer, that lets us *route* incoming requests to various features

so for example when you point your browser at <http://localhost:8000/> with no further indication, this will be routed to the `/` endpoint thanks to the
```
@app.route('/')
```

if now you do instead <http://localhost:8000/api/leases/1000/2024>, this time you will hit the code marked with
```python
@app.route('/api/leases/<how_many>/<beg>')
```

so you can see how the incoming URL gets bound to Python variables, and how the code then can perform whatever conversion needed (e.g. here we assume dates are ISO8601)

+++

### the API outcome

look more closely at the result of `http://localhost:8000/api/leases/1000/2024`  
as opposed to the home page (that outputs HTML code thanks to the `markdown-it` library), this API endpoint produces data in a JSON format, as I'm sure you've recognized  

the reason for that is the last line of the `leases()` Python function (the one bound to the api URL route), that reads
```python
return JSONResponse(content=list_of_dicts)
```

+++

### wrapping it up

so we are kind of in the same situation as with the first TP, i.e. we have a **data source** with the same data essentially, except that

- it is dynamic (re-generated every time we call the API)
- and in JSON instead of in csv

+++

## altair visualisations

altair offers a "grammar-oriented" visualisation paradigm where the visualisation is defined in a **declarative** way

+++

### a stacked bar from altair's doc

here's an example taken from the altair documentation

```{code-cell} ipython3
# stolen from https://altair-viz.github.io/gallery/stacked_bar_chart.html

import altair as alt
from vega_datasets import data

source = data.barley()

alt.Chart(source).mark_bar().encode(
    x='variety',
    y='sum(yield)',
    color='site'
)
```

### **exo**: inspect the data

take some time to get a glimpse at what the data looks like...

```{code-cell} ipython3
# your code here
# feel free to create extra cells if needed
```

```{code-cell} ipython3
# prune-cell

import itables
itables.init_notebook_mode()

source
```

+++ {"tags": ["level_basic"]}

### **exo**: write your own pivot

you should be able to see a resemblance with some sort of *pivot table* here  
would you be able to compute a pivot table that resonates with this visualisation ?

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

source.pivot_table(
    values='yield',
    aggfunc="sum",
    index="site",
    columns="variety",
)
```

### a few useful additions

here's a few additions to that sample chart, that will make our life easier:

- we set a *width* and *height*
- as well as a *title*
- and make it interactive: try to scroll up or down in the figure with 2 fingers

````{admonition} not interactive ?
:class: dropdown

Oh but no, the interactive thing is not working for us here; it is because the X axis does not have numeric values !  
but let's keep this trick in mind for later, it will come in handy at some point
````

```{code-cell} ipython3
# once and for good
alt.renderers.enable("mimetype")

# same beginning

alt.Chart(source).mark_bar().encode(
    x='variety',
    y='sum(yield)',
    color='site'
).properties(
    height=400,
    width=800,
    title=f"Barley yields",
).interactive()
```

## back to our data

we still need the country-to-region association - same as in the previous TP

```{code-cell} ipython3
countries = pd.read_csv("data/countries.csv")
countries.head(3)
```

```{code-cell} ipython3
# also to get the orders of magnitude right

# e.g. to do a grouping per week
# in altair jargon
GROUP_UNIT = "yearweek"
# just for the legends and titles
NAME = "week"

# we ask the API to create that number of leases
HOW_MANY = 1000

# we want to display the charts in this unit
GRAIN = pd.Timedelta(1, 'm')
```

```{code-cell} ipython3
# prune-begin
```

```{code-cell} ipython3
URL = f"http://localhost:8000/api/leases/{HOW_MANY}/2025"

leases = pd.read_json(URL)
leases['beg'] = pd.to_datetime(leases['beg'], format="ISO8601")
leases['end'] = pd.to_datetime(leases['end'], format="ISO8601")

# compute the duration in minutes
leases['duration'] = (leases['end'] - leases['beg']) // GRAIN

# here we use the middle of the lease as a criteria to attach a lease to a period
leases['date'] = pd.to_datetime((leases['beg'] + (leases['end']-leases['beg'])/2).dt.date)

# add the region tag to each lease
merge = leases.merge(countries, left_on="country", right_on="name")
```

```{code-cell} ipython3
merge
```

```{code-cell} ipython3
# hard-wired 'yearweek' for now, for clarity

( 
alt.Chart(merge)
  .mark_bar()
  .encode(
      x=f'yearweek(date):T',
      y='sum(duration)',
      color='region',
  )
  .properties(
       height=400,
       width=800,
       title=f"Usage by region",
 )
 .interactive()
)
```

```{code-cell} ipython3
# prune-end
```

```{code-cell} ipython3
# prune-cell

# a more realistic version
# no Python preprocessing ?

chart = (
    alt.Chart("data/leases.csv")
        .transform_calculate(
            # Duration in minutes (timestamps are in ms)
            duration="(toDate(datum.end) - toDate(datum.beg)) / (1000*60)",
            # Midpoint as a date
            mid="datetime((toDate(datum.end).getTime() + toDate(datum.beg).getTime())/2)"
        )
    .mark_bar()
    .encode(
         x=alt.X(
            f'${GROUP_UNIT}(mid):T',
            axis=alt.Axis(title=f"Period (by {name})"),
            timeUnit=f"{values['timeUnit']}",
        ),
            y=alt.Y('sum(duration):Q', title='Duration (hours)'),
            color=alt.Color(
                'family:N',
                scale=alt.Scale(domain=list(colormap.keys()),
                                range=list(colormap.values())),
                title="Family",
                legend=alt.Legend(title="by Family", symbolSize=500),
            ),
            # this actually orders the bars; it is computed in models.py
            order=alt.Order('stack-order:N', sort='ascending'),
            tooltip=['name:N', 'period:N', 'family:N', 'sum(duration):Q'],
        )
        .configure_legend(
            titleFontSize=20,
            labelFontSize=18,
            strokeColor='gray',
            fillColor='#EEEEEE',
            padding=10,
            cornerRadius=10,
            orient='top-left',
        )
        .properties(
            height='container',
            width='container',
            title=f"Usage by family ({name})",
        )
        .interactive()
```
