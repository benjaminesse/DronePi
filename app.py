"""Script to handle the PiSpec dashboard."""
import os
import pandas as pd
import plotly.express as px
from flask import Flask
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

# List the plot parameters
plot_items = ["Lat", "Lon", "Alt", "SO2_SCD_mol", "SO2_err_mol",
              "SO2_SCD_ppmm", "SO2_err_ppmm", "IntegrationTime", "Intensity"]

# Get the available colorscales
colorscales = px.colors.named_colorscales()

# Setup the Dash app
server = Flask(__name__)
app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.DARKLY])
app.title = "PiSpec Dashboard"

# =============================================================================
# App Controls
# =============================================================================

controls = dbc.Card(
    [
        # Select parameter to plot ============================================
        html.Div(
            [
                dbc.Label("Plot Parameter"),
                dcc.Dropdown(
                    id="param-filter",
                    options=[{"label": plot_param, "value": plot_param}
                             for plot_param in plot_items],
                    value="SO2_SCD_ppmm",
                    clearable=False,
                    searchable=False,
                    style=dict(color="black")
                )
            ]
        ),

        # Select Colormap =====================================================
        html.Div(
            [
                dbc.Label("Colormap"),
                dcc.Dropdown(
                    id="cmap-filter",
                    options=[{"label": cmap, "value": cmap}
                             for cmap in colorscales],
                    value="viridis",
                    clearable=False,
                    style=dict(color="black")
                )
            ]
        ),

        html.Hr(),

        # Select upper and lower limits =======================================
        html.Div(
            [
                dbc.Label("Upper Limit"),
                dbc.Input(id='clim-hi', type='number', placeholder="-")
            ]
        ),

        html.Div(
            [
                dbc.Label("Lower Limit"),
                dbc.Input(id='clim-lo', type='number', placeholder="-")
            ]
        ),

        html.Hr(),

        # Add refresh button ==================================================
        html.Div(
            [
                dbc.Button("Refresh", id="refresh", color="primary",
                           style={"margin-left": "15px"})
            ]
        )
    ],
    body=True
)

# =============================================================================
# App Plots
# =============================================================================

plots = dbc.Card(
    [
        html.Div(
            dcc.Slider(0, 20, 1, value=11, id="zoom-slider")
        ),
        html.Div(
            dcc.Graph(id="map-chart")
        ),
        html.Hr(),
        html.Div(
            dcc.Graph(id="time-chart")
        )
    ],
    body=True
)

# =============================================================================
# App Layout
# =============================================================================

app.layout = dbc.Container(
    [
        html.H1("PiSpec Dashboard"),
        html.Div([dbc.Label("Status")], id="status-text"),
        html.Hr(),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(controls, md=4),
                        dbc.Col(plots, md=8),
                    ]
                ),
                dcc.Interval(
                    id='interval-component',
                    interval=5000, # in milliseconds
                    n_intervals=0
                )
            ]
        )
    ],
    fluid=True
)


# =============================================================================
# Callbacks
# =============================================================================

@app.callback(
    [
        Output("map-chart", "figure"),
        Output("time-chart", "figure")
    ],
    [
        Input("param-filter", "value"),
        Input("cmap-filter", "value"),
        Input("clim-hi", "value"),
        Input("clim-lo", "value"),
        Input("zoom-slider", "value"),
        Input("refresh", "n_clicks"),
        Input("interval-component", "n_intervals")
    ]
)
def refresh(plot_param, cmap, clim_hi, clim_lo, zoom, n, n_interval):
    """Refresh app plots."""
    # Get the results folder
    res_folders = os.listdir("Results")
    res_folders.sort()
    fpath = res_folders[-1]

    # Read in the results
    try:
        df = pd.read_csv(f"Results/{fpath}/so2_output.csv", parse_dates=True)
    except FileNotFoundError:
        # If the file is not found, return an empty DataFrame
        cols = ["Time"] + plot_items
        df = pd.DataFrame(columns=cols)
        clim_lo = None
        clim_hi = None

    # Set the limits
    if clim_lo is None:
        clim_lo = df[plot_param].min()
    if clim_hi is None:
        clim_hi = df[plot_param].max()
    limits = [clim_lo, clim_hi]

    # Generate the map figure
    map_fig = px.scatter_mapbox(
        df, lat="Lat", lon="Lon", color=plot_param, range_color=limits,
        mapbox_style="stamen-terrain", color_continuous_scale=cmap,
        zoom=zoom
    )

    # Generate the time series figure
    time_fig = px.line(df, x="Time", y=plot_param)
    time_fig.update_yaxes(range=limits)

    return [map_fig, time_fig]


if __name__ == "__main__":
    app.run_server(debug=True)
