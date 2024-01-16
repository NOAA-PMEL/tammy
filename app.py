import json

import dash
import dash_ag_grid
import numpy as np
import pandas as pd
import plotly.express as px
from app_studio import Rv
from dash import Input, Output, State, callback, dcc, html
from dash_enterprise import EnterpriseDash, ddk

app = EnterpriseDash(__name__, suppress_callback_exceptions=True)
app.configure(
    logo="https://dash.plotly.com/assets/images/plotly_logo_dark.png", title="")


u1040 = 'https://data.pmel.noaa.gov/generic/erddap/tabledap/sd1040_hurricane_2023.csv?time,latitude,longitude,BARO_PRES_MEAN,WIND_SPEED_MEAN,TEMP_SBE37_MEAN,WAVE_SIGNIFICANT_HEIGHT&time>=2023-10-21&time<=2023-10-25'
u1041 = 'https://data.pmel.noaa.gov/generic/erddap/tabledap/sd1041_hurricane_2023.csv?time,latitude,longitude,BARO_PRES_MEAN,WIND_SPEED_MEAN,TEMP_SBE37_MEAN,WAVE_SIGNIFICANT_HEIGHT&time>=2023-10-21&time<=2023-10-25'
u1068 = 'https://data.pmel.noaa.gov/generic/erddap/tabledap/sd1068_hurricane_2023.csv?time,latitude,longitude,BARO_PRES_MEAN,WIND_SPEED_MEAN,TEMP_SBE37_MEAN,WAVE_SIGNIFICANT_HEIGHT&time>=2023-10-21&time<=2023-10-25'
d1040 = pd.read_csv(u1040, skiprows=[1])
d1040['drone'] = 'sd1040'
d1041 = pd.read_csv(u1041, skiprows=[1])
d1041['drone'] = 'sd1041'
d1068 = pd.read_csv(u1068, skiprows=[1])
d1068['drone'] = 'sd1068'
df = pd.concat([d1040, d1041, d1068])
variable_dropdown = dcc.Dropdown(
    options=df.columns, value='BARO_PRES_MEAN', multi=False, id='variable_dropdown-component')
plot_value = Rv(variable_dropdown, 'value')
map = px.scatter_geo(df, lat='latitude', lon='longitude', color=plot_value,
                     fitbounds='locations', height=750, color_continuous_scale=px.colors.sequential.Inferno)
figure = px.line(df, x='time', y=plot_value, color='drone')
figure.update_yaxes(title=dict(text=plot_value))
figure.update_layout(title=plot_value)


app.layout = html.Div([
    ddk.Hero(
        description="Three drones interact with Hurricane Tammy during the 2023 hurricane saildrone mission.\n\nThis app allows you to explore barometric pressure, wind speed, sea surface temperature and significant wave height from the 3 drones. ",
        primary_controls=[
            html.Div(
                title="Variable dropdown",
                children=html.Div(
                    children=variable_dropdown,
                    id="variable_dropdown-component-parent"
                )
            )
        ],
        sticky_controls=True,
        tags=[
            ddk.Tag(
                icon="user",
                text="**Created By:** Roland Schweitzer"
            ),
            ddk.Tag(
                icon="envelope",
                text="**Contact:** roland.schweitzer@noaa.gov"
            ),
            ddk.Tag(
                icon="clock",
                text="**Last Updated:** January 16, 2024"
            )
        ],
        title="Hurricane Tammy August 21, 2023 to August 15, 2033"
    ),
    html.Div(
        className="appcontent",
        children=[
            html.Section(
                className="section",
                children=[
                    html.Div(
                        className="section--info",
                        children=[
                            html.Div(
                                children="Location and Timeseries",
                                className="section--title"
                            ),
                            html.Div(
                                children="The location of drones and timeseries plots of the data from the 3 drones.",
                                className="section--description"
                            )
                        ]
                    ),
                    html.Div(
                        className="section--layout",
                        children=[
                            html.Div(
                                className="section-layout s1",
                                children=[
                                    ddk.Card(
                                        description="Colored by the selected variable",
                                        title="Drone Locations",
                                        children=ddk.Graph(
                                            figure=map,
                                            id="map-component"
                                        )
                                    )
                                ]
                            ),
                            html.Div(
                                className="section-layout s1",
                                children=[
                                    ddk.Card(
                                        description="Colored by the observing drone.",
                                        title="Timeseries",
                                        children=ddk.Graph(
                                            figure=figure,
                                            id="figure-component"
                                        )
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            html.Section(
                className="section",
                children=[
                    html.Div(
                        className="section--info",
                        children=[
                            html.Div(
                                children="Data Table",
                                className="section--title"
                            ),
                            html.Div(
                                children="The data used in the plots.",
                                className="section--description"
                            )
                        ]
                    ),
                    html.Div(
                        className="section--layout",
                        children=html.Div(
                            className="section-layout s1",
                            children=[
                                ddk.Card(
                                    description="",
                                    title="Df",
                                    children=dash_ag_grid.AgGrid(
                                        columnDefs=[{'field': i} for i in df.columns],
                                        dashGridOptions={
                                            "pagination": True,
                                            "paginationAutoPageSize": True,
                                            "defaultColDef": {
                                                "resizable": True,
                                                "sortable": True,
                                                "filter": True
                                            }
                                        },
                                        id="df-component",
                                        rowData=df.to_dict('records')[:1000]
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        ]
    ),
    ddk.Footer(
        tags=[
            ddk.Tag(
                icon="user",
                text="**Created By:** Roland Schweitzer"
            ),
            ddk.Tag(
                icon="envelope",
                text="**Contact:** roland.schweitzer@noaa.gov"
            )
        ],
        title="Hurricane Tammy August 21, 2023 to August 15, 2033"
    )
])

@callback(Output("map-component", "figure"), Input("variable_dropdown-component", "value"), prevent_initial_call=True)
def update(plot_value):
    u1040 = 'https://data.pmel.noaa.gov/generic/erddap/tabledap/sd1040_hurricane_2023.csv?time,latitude,longitude,BARO_PRES_MEAN,WIND_SPEED_MEAN,TEMP_SBE37_MEAN,WAVE_SIGNIFICANT_HEIGHT&time>=2023-10-21&time<=2023-10-25'
    u1041 = 'https://data.pmel.noaa.gov/generic/erddap/tabledap/sd1041_hurricane_2023.csv?time,latitude,longitude,BARO_PRES_MEAN,WIND_SPEED_MEAN,TEMP_SBE37_MEAN,WAVE_SIGNIFICANT_HEIGHT&time>=2023-10-21&time<=2023-10-25'
    u1068 = 'https://data.pmel.noaa.gov/generic/erddap/tabledap/sd1068_hurricane_2023.csv?time,latitude,longitude,BARO_PRES_MEAN,WIND_SPEED_MEAN,TEMP_SBE37_MEAN,WAVE_SIGNIFICANT_HEIGHT&time>=2023-10-21&time<=2023-10-25'
    d1040 = pd.read_csv(u1040, skiprows=[1])
    d1040['drone'] = 'sd1040'
    d1041 = pd.read_csv(u1041, skiprows=[1])
    d1041['drone'] = 'sd1041'
    d1068 = pd.read_csv(u1068, skiprows=[1])
    d1068['drone'] = 'sd1068'
    df = pd.concat([d1040, d1041, d1068])
    map = px.scatter_geo(df, lat='latitude', lon='longitude', color=plot_value,
                         fitbounds='locations', height=750, color_continuous_scale=px.colors.sequential.Inferno)
    return map


@callback(Output("figure-component", "figure"), Input("variable_dropdown-component", "value"), prevent_initial_call=True)
def update(plot_value):
    u1040 = 'https://data.pmel.noaa.gov/generic/erddap/tabledap/sd1040_hurricane_2023.csv?time,latitude,longitude,BARO_PRES_MEAN,WIND_SPEED_MEAN,TEMP_SBE37_MEAN,WAVE_SIGNIFICANT_HEIGHT&time>=2023-10-21&time<=2023-10-25'
    u1041 = 'https://data.pmel.noaa.gov/generic/erddap/tabledap/sd1041_hurricane_2023.csv?time,latitude,longitude,BARO_PRES_MEAN,WIND_SPEED_MEAN,TEMP_SBE37_MEAN,WAVE_SIGNIFICANT_HEIGHT&time>=2023-10-21&time<=2023-10-25'
    u1068 = 'https://data.pmel.noaa.gov/generic/erddap/tabledap/sd1068_hurricane_2023.csv?time,latitude,longitude,BARO_PRES_MEAN,WIND_SPEED_MEAN,TEMP_SBE37_MEAN,WAVE_SIGNIFICANT_HEIGHT&time>=2023-10-21&time<=2023-10-25'
    d1040 = pd.read_csv(u1040, skiprows=[1])
    d1040['drone'] = 'sd1040'
    d1041 = pd.read_csv(u1041, skiprows=[1])
    d1041['drone'] = 'sd1041'
    d1068 = pd.read_csv(u1068, skiprows=[1])
    d1068['drone'] = 'sd1068'
    df = pd.concat([d1040, d1041, d1068])
    figure = px.line(df, x='time', y=plot_value, color='drone')
    figure.update_yaxes(title=dict(text=plot_value))
    figure.update_layout(title=plot_value)
    return figure


server = app.server
if __name__ == '__main__':
    app.run(debug=True)
