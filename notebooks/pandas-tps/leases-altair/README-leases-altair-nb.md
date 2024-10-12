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

# CURRENT STATUS:

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
python fastapi_random_server.py
```

this will behave a bit like `jupyter lab`, in that it will

- start a web server
- display the URL to use to join it
- and it will *block*, meaning the terminal is busy, and no longer responding to your commands

so first off, leave this terminal running, and create another one if needed

+++

### how to use

just open a web browser and cut-n-paste the URL displayed in the terminal; something like  
`http://localhost:4999/`

as you might have got now, this means

- use the http protocol
- to reach a service running on the computer named `localhost` (your own laptop, that is)
- on port 4999

ports is a very simple mechanism to allow your computer to run many different services (in real life, you would typically have ssh on port 22, web on port 443, dns on port 53, and so on..)

+++

### the source code: routes

take a look at the source code for the server, and observe the occurrences of `@app.route`  
this the mechanism offered by the fastapi layer, that lets us *route* incoming requests to various features

so for example when you point your browser at `http://localhost:4999/` with no further indication, this will be routed to the `/` endpoint thanks to the
```
@app.route('/')
```
but when doing `http://localhost:4999/api/leases/1000/2024`, this time you will hit the code marked with
```python
@app.route('/api/leases/<how_many>/<beg>')
```

so you can see how the incoming URL gets bound to Python variables, and how the code then can perform whatever conversion needed (e.g. here we assume dates are ISO8601)

+++

### the API outcome

look more closely at the result of `http://localhost:4999/api/leases/1000/2024`  
as opposed to the home page (that outputs HTML code thanks to the `markdown-it` library), this API endpoint produces data in a JSON format, as I'm sure you've recognized  

the reason for that is the last line of the `leases()` Python function (the one bound to the api URL route), that reads
```python
    return json.dumps(list_of_dicts)
```

+++

### wrapping it up

so we are kind of in the same situation os with the first TP, i.e. we have a data source with the same data essentially, except that

- it is dynamic (re-generated every time we call the API)
- and in JSON instead of in csv

+++

## altair visualisations

altair offers a "grammar-oriented" visualisation paradigm where the visualisation is defined in a **declarative** way

+++

### a stacked bar example

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

```{code-cell} ipython3
# take some time to get a glimpse at what the data looks like
```

```{code-cell} ipython3

```

+++ {"tags": ["level_basic"]}

### exo

you should be able to see a resemblance with some sort of pivot table here  
would you be able to compute a pivot table that resonates with this visualisation ?

```{code-cell} ipython3
# your code
```

### a few useful additions

here's a few additions to that sample chart, that will make our life easier:

- we set a width and height
- as well as a title
- and make it interactive: try to scroll up or down in the figure with 2 fingers

````{admonition} not interactive ?

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

### back to our data

```{code-cell} ipython3



chart = (
    alt.Chart("data/leases.csv")
    .mark_bar()
    .encode(
         x=alt.X(
            f'period-middle:T',
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
