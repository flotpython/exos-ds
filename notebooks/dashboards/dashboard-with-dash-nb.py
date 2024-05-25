# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control,-trusted,-editable
#     notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version,
#       -jupytext.text_representation.format_version,-language_info.version, -language_info.codemirror_mode.version,
#       -language_info.codemirror_mode,-language_info.file_extension, -language_info.mimetype,
#       -toc, -rise, -version
#     text_representation:
#       extension: .py
#       format_name: light
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
#   language_info:
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
# ---

# # a sample dash dashboard 

# ````{admonition} attention
# :class: warning
#
# this code won't work from a notebook, you need to kick it off using (download as .py if needed)
#
# ```bash
# python dashboard-with-dash-nb.py
# ```
#
# which starts a http server; you then need to open a web browser on the displayed URL (something like `http://127.0.0.1:8050`)
# ````

import plotly.express as px

from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output

# +
# Load Data

df = px.data.tips()

# +
# Build App
# __name__ is a global auto-defined by Python
# from the current filename

app = Dash(__name__)
# -

# create html content
app.layout = html.Div([
    html.H1("Dash Demo: a minimal dashboard"),
    # the graph
    dcc.Graph(id='graph'),
    # the colorscale picker (dropdown)
    html.Label([
        "colorscale",
        dcc.Dropdown(
            id='colorscale-dropdown', 
            clearable=False,
            value='plasma', 
            options=[
                {'label': c, 'value': c}
                for c in px.colors.named_colorscales()
            ],
        )
    ]),
])

# flask-friendly
# Define callback to update graph
@callback(
    Output('graph', 'figure'),
    Input("colorscale-dropdown", "value"),
)


def update_figure(colorscale):
    print(f"{colorscale=}")
    return px.scatter(
        df, x="total_bill", y="tip", 
        color="size",
        color_continuous_scale=colorscale,
        render_mode="webgl", 
        title="Tips"
    )



# Run app: this kicks off a http server
#
# from your web browser, open a new tab or window
# and point at the displayed URL, it will display the dashboard

app.run_server()

# ```{seealso}
# there are ways to run this inside a jupyter notebook  
# it's a bit of a moving target though, so please refer to this page for details  
# <https://dash.plotly.com/dash-in-jupyter>
# ```

# ***
