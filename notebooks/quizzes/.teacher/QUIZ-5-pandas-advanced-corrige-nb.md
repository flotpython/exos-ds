---
jupytext:
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
nbhosting:
  title: advanced pandas
---

# merge (join)

```{code-cell} ipython3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
```

## the data

+++

Here is a simple dataset of three tables.

```{code-cell} ipython3
import pandas as pd

wifi_table = pd.DataFrame(
    {
        "SSID_ID": [1, 2, 2, 5, 3, 1],
        "BSSID_ID": [1, 2, 2, 5, 3, 1],
        "DBM": [-34, -36, -80, -60, -55, -48],
    },
    index=pd.date_range("3 june 2021", periods=6),
)

ssid_table = pd.DataFrame(
    {
        "ID": [1, 2, 3, 4, 5, 6],
        "SSID": ["box bill", "sam", "orange1884", "FreeWifi", "sfr43", "Eduroam"],
    }
)
bssid_table = pd.DataFrame(
    {
        "ID": [1, 2, 3, 4, 5, 6],
        "BSSID": [
            "10:10:10:10:20",
            "30:30:20:11:15",
            "18:34:26:45:12",
            "11:54:65:55:23",
            "45:43:22:43:54",
            "44:35:33:22:11",
        ],
    }
)
print(f"**wifi_table**\n{wifi_table}\n**ssid_table**\n{ssid_table}\n**bssid_table**\n{bssid_table}")
```

### merge

Let's start with a simple merge of `wifi_table` with `ssid_table` (on `SSID_ID` and `ID`), and with `bssid_table` (on `BSSID_ID` and `ID`). You must keep the index of `wifi_table`.

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

(
    wifi_table.reset_index()
    .merge(ssid_table, left_on="SSID_ID", right_on="ID", how="left")
    .drop(columns=["SSID_ID", "ID"])
    .merge(bssid_table, left_on="BSSID_ID", right_on="ID", how="left")
    .drop(columns=["BSSID_ID", "ID"])
    .set_index("index")
    .sort_index()
)
```

## another dataset

+++

Here is a new dataset

```{code-cell} ipython3
df1 = pd.DataFrame({'name': ['Bob', 'Lisa', 'Sue'],
                    'pulse': [70, 63, 81]}, 
                   index=[123, 354, 165])
df2 = pd.DataFrame({'name': ['Eric', 'Bob', 'Marc'],
                    'weight': [60, 100, 70]},
                  index=[654, 123, 664])
```

### merge

Let's outer merge the tables df1 and df2 on name and preserving both indexes. Name the index of df1 `ID_old` and the index of df2 `ID_new`.

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell 

df1 = df1.reset_index().rename(columns={"index": "ID_old"})
df2 = df2.reset_index().rename(columns={"index": "ID_new"})
x = pd.merge(df1, df2, how='outer')
print(x)
```

**Now, consider that `ID_new` is the new person ID that must be kept, but that for some person, the new ID is missing. In that case, this missing ID must be replaced with the old person ID `ID_old`. Finally, set the new person ID as the index.**

*Hint*: consider `combine_first`

```{code-cell} ipython3
# your code
```

```{code-cell} ipython3
# prune-cell

x.loc[:,'ID_new'] = x.loc[:,'ID_new'].combine_first(x.loc[:,'ID_old'])
x = x.drop(columns='ID_old').set_index('ID_new').sort_index()
print(x)
```

***
