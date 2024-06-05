import plotly.express as px

from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output

# Load Data

df = px.data.tips()

# Build App
# __name__ is a global auto-defined by Python
# from the current filename

app = Dash(__name__)


# create html content
app.layout = html.Div([
    html.H1("Dash Demo: an interactive visualization of tips data"),
    html.P("This is a demo of Dash - you can use the dropdown below to use a different colormap"),

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



# run the app
app.run_server()
