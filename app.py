#%%
import pandas as pd
import numpy as np
import plotly.express as px

import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dash_table, dcc, callback, Output, Input, State

import dash_bootstrap_components as dbc

# %%
# DATA LOADING
df = pd.read_csv('power_machines.csv', sep=';')

df = df.rename(columns={'type_of_equipment': 'Тип турбины',
                        'type_of_station': 'Тип станции',
                        'power': 'Мощность',
                        'number_of_turbines': 'Количество',
                        'station': 'Станция',
                        'country': 'Страна',
                        'year_of_manufacture': 'Год выпуска',
                        'sum_power': 'Суммарная мощность'})


country_ = df['Страна'].unique()
equipment_ = df['Тип турбины'].unique()


# GLOBAL DESIGN SETTINGS
CHARTS_TEMPLATE = go.layout.Template(
    layout=dict(
        font=dict(family='Century Gothic',
                  size=14,
                  color='black'),
        legend=dict(orientation='h',
                    title_text='',
                    x=0,
                    y=1.2)
    )
)


# %%
# INITIALIZE THE APP

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])



# APP LAYOUT

sidebar = html.Div(
    [
        dbc.Row(
            [
                html.P('Турбины Силовых машин',
                       style={'margin-top': '6px',
                              'margin-left': '8px',
                              'font-size': '20px',
                              'font-family': 'Century Gothic'}),
            ],
            style={"height": "5vh"},
            className='bg-dark-subtle text-black font-italic'
        ),
        dbc.Row(
            [
                html.P('Выбор страны и типа турбины (паровая/гидро)'),
                dcc.Dropdown(id='select_contry', multi=False, value='Россия',
                             options=[{'label': x, 'value': x} for x in country_],
                             style={'margin-top': '2px',
                                    'width': '100%'}),
                dcc.Dropdown(id='select_equipment', multi=False, value='Паровые турбины',
                             options=[{'label': x, 'value': x} for x in equipment_],
                             style={'margin-top': '6px',
                                    'width': '100%'})
            ],
            style={"height": "23vh"}
        ),
        dbc.Row(
            [
                html.Div([
                    dcc.Markdown('Общее число выпущенных турбин (шт):'),
                    html.H2(id='total-turbine', style={'margin-top': '6px',
                                                       'color': 'black'})
                ]),
                html.Div([
                    dcc.Markdown('Общая мощность выпущенных турбин (МВт):'),
                    html.H2(id='total-power', style={'color': 'black'})
                ])
            ],
            style={"height": "45vh"}
        )
    ]
)

# GRAPHICS AND TABLE FOR CONTENT

graph_card1 = dbc.Card(
    [
        dbc.CardBody(
            dcc.Graph(id="capacity-distribution", responsive=True)
        ),
    ],
    style={"width": "100%", "margin": "20px"}
)

graph_card2 = dbc.Card(
    [
        dbc.CardBody(
            dcc.Graph(id="power-by-years", responsive=True)
        ),
    ],
    style={"width": "100%", "margin": "20px"}
)

table_card = dbc.Card(
    [
        dbc.CardBody(
            html.Div(id='data-table')
        ),
    ],
    style={"width": "100%", "margin": "20px"}
)

content = html.Div([
                dbc.Row([
                    dbc.Col(graph_card1, width=6),
                    dbc.Col(graph_card2, width=6)
                ],
                style={"width": "100%", "margin": "auto"}),
                
                dbc.Row([
                    dbc.Col(table_card, width=12)
                ],
                style={"width": "100%", "margin": "auto"})
])

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=2, className='bg-body-secondary'),
                dbc.Col(content, width=10, className='bg-light-subtle')
                ],
            style={"height": "100%"}
            ),
        ],
    fluid=True
    )


# ADD CONTROLS TO BUILD THE INTERATION
@callback(
    [Output('total-turbine', 'children'),
    Output('total-power', 'children'),
    Output('capacity-distribution', 'figure'),
    Output('power-by-years', 'figure'),
    Output('data-table', 'children')],
    [Input('select_contry', 'value'),
     Input('select_equipment', 'value')]
)

def update_total_count(selected_country, selected_equipment):
    filtered_data = df[(df['Страна'] == selected_country) & 
                       (df['Тип турбины'] == selected_equipment)]
    
    
    # create plots
    hist = px.histogram(filtered_data, 
                        x="Мощность", 
                        color="Тип турбины",
                        hover_data=filtered_data.columns, 
                        nbins=60)
    hist.update_layout(template=CHARTS_TEMPLATE,
                       font_color='black',
                       legend=dict(font_color='black'))
    hist.update_xaxes(title='Мощность, МВт')
    hist.update_yaxes(title='Количество, шт')
    
    scatter = px.scatter(filtered_data, 
                         x="Год выпуска", 
                         y="Суммарная мощность", 
                         color="Тип станции")
    scatter.update_layout(template=CHARTS_TEMPLATE,
                          font_color='black',
                          legend=dict(font_color='black'))
    scatter.update_xaxes(title='Год')
    scatter.update_yaxes(title='Суммарная мощность, МВт')

    # create indicators
    indicator_turbine = filtered_data['Тип турбины'].count()
    indicator_power = round(filtered_data['Суммарная мощность'].sum(), 1)
    
    # create data table
    raw_data = filtered_data.drop(['Unnamed: 0', 'Тип турбины', 'Тип станции', 'Страна'], axis=1)
    
    tb = dash_table.DataTable(data=raw_data.to_dict('records'),
                              columns=[{'name': i, 'id': i}
                                       for i in raw_data.columns],
                              style_cell={'fontSize':14, 
                                          'font-family':'Century Gothic'},
                              style_data={'width': '100px',
                                          'maxWidth': '100px',
                                          'minWidth': '100px',
                                          'backgroundColor': 'rgb(255, 255, 255)'}, 
                              style_header={'textAlign': 'center',
                                            'backgroundColor': 'rgb(200, 200, 200)'},
                              page_size=15)
    
    return indicator_turbine, indicator_power, hist, scatter, tb

# RUN THE APP
if __name__ == '__main__':
    app.run(debug=True)
# %%
