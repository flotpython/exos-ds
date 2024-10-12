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

# install with
# pip install "fastapi[standard]"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse


app = FastAPI()

# CORS settings (cors = pita)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",            # to allow all
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


# globals

VARIETIES = pd.read_csv("data/varieties.csv")
SITES = pd.read_csv("data/sites.csv")

MIN_AMOUNT = 10
MAX_AMOUNT = 100

def random_data(from_year, until_year):

    return [
        {
            "variety": variety,
            "site": site,
            "yield": random.randint(MIN_AMOUNT, MAX_AMOUNT),
            "year": year,
        } 
            for variety in VARIETIES['variety']
            for site in SITES['site']
            for year in range(from_year, until_year + 1)
    ]


"""
http :8000/api/yields/1931/1940
"""

# the API endpoint
@app.get('/api/yields/{from_year}/{until_year}')
def data(from_year: int, until_year: int):
    return JSONResponse(content=random_data(from_year, until_year))
