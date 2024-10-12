"""
this Python code uses FastAPI to implement a http server that
serves random data suitable to be fed in the first part of the assignment

in part 1 we build a notebook that reads file `data/leases.csv`

here we write an http endpoint that can generate random leases
in a specified time interval

remember to install with
```bash
pip install fastapi[standrd]
```
"""

import json
import random

import pandas as pd
import numpy as np

# pip install markdown-it-py
from markdown_it import MarkdownIt

# pip install "fastapi[standard]"
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse


app = FastAPI()


# the welcome page - in markdown

WELCOME = """
# random generator

## the API endpoint

use the API endpoint ```text /api/leases/how-many/beg ``` to receive a JSON
stream of leases that have essentially the same format as `leases.csv`, i.e.
with columns

| beg | end | country |
|-----|-----|---------|
| iso8601 | iso8601 | string |

## beg format

dates (`beg`) should be in a format that `pd.Timestamp` understands  

## the end

you don't get to specify the end, as the leases are generated randomly but in
successive order using some hard-wired constants (see the code)

## examples

- [/api/leases/1000/2024](/api/leases/1000/2024)  
   yields 1000 samples starting on 1st jan 24 (at 00:00, that is, in this case)
- [/api/leases/100/2024-06-30T12:30](/api/leases/100/2024-06-30T12:30)  
   yields 100 samples starting on 30th june 24 at 12:30
"""

@app.route('/')
def hello(request) -> HTMLResponse:
    renderer = MarkdownIt("gfm-like")
    return HTMLResponse(renderer.render(WELCOME))

# globals

COUNTRIES = pd.read_csv("data/countries.csv")

GRAIN = pd.Timedelta('10m')
MIN_LEASE = pd.Timedelta('1h')
MAX_LEASE = pd.Timedelta('2h')

MIN_PAUSE = pd.Timedelta('10m')
MAX_PAUSE = pd.Timedelta('8h')

def random_leases(how_many, beg):
    lease_extent = (MAX_LEASE - MIN_LEASE) // GRAIN
    pause_extent = (MAX_PAUSE - MIN_PAUSE) // GRAIN

    lease_durations = np.random.randint(0, lease_extent, how_many) * GRAIN
    pause_durations = np.random.randint(0, pause_extent, how_many) * GRAIN

    begs = np.empty((how_many,), dtype='datetime64[ns]')
    ends = np.empty((how_many,), dtype='datetime64[ns]')

    # not seeing a way to vectorize this at first
    current = beg
    for index in range(how_many):
        # breakpoint()
        begs[index] = current + pause_durations[index]
        current = ends[index] = begs[index] + lease_durations[index]

    return begs, ends


# the API endpoint
@app.get('/api/leases/{how_many}/{beg}')
def leases(how_many: int, beg: str):
    try:
        beg = pd.Timestamp(beg)
    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid timestamp format: {beg}. Error: {str(e)}"
        )

    begs, ends = random_leases(how_many, beg)

    # pick the countries
    countries = random.choices(COUNTRIES.name, k=how_many)

    list_of_dicts = [
        dict(beg=str(beg), end=str(end), country=country)
        for beg, end, country in zip(begs, ends, countries)
    ]
    # return json.dumps(list_of_dicts)
    return JSONResponse(content=list_of_dicts)
