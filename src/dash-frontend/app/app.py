import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash import no_update
import sys
import mongo_db_helper
from pprint import pprint

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# db = Database()

total_cases = mongo_db_helper.get_by_model("total_cases")
deaths = mongo_db_helper.get_by_model("deaths")
hospitalized = mongo_db_helper.get_by_model("hospitalized")
intensive_care = mongo_db_helper.get_by_model("intensive_care")
deaths = mongo_db_helper.get_by_model("deaths")
domestic_isolation = mongo_db_helper.get_by_model("domestic_isolation")
region = mongo_db_helper.get_by_region(1)
pprint(deaths)

region_metric = region[0]


app.layout = dbc.Container(
    dbc.Row(
        dbc.Col(
            [
                dbc.Card(
                    [
                        html.H2('Covid Dashboard Italy', className='card-title'),
                        
                        html.Br(),

                        dcc.Graph(
                            id='graph_total_cases',
                            figure={
                                'data': [
                                    {'x': [x for x in range(14)], 'y': [((y + region_metric['day']) * region_metric['coefficients'][0]) + region_metric['intercept'] for y in range(14)], 'type': 'line', 'name': region_metric['region_id']} 
                                    for region_metric in total_cases
                                ],
                                'layout': {
                                    'title': 'Total Cases by Region',
                                }
                            }
                        ),

                        dcc.Graph(
                            id='graph_domestic_isolation',
                            figure={
                                'data': [
                                    {'x': [x for x in range(14)], 'y': [((y + region_metric['day']) * region_metric['coefficients'][0]) + region_metric['intercept'] for y in range(14)], 'type': 'line', 'name': region_metric['region_id']} 
                                    for region_metric in domestic_isolation
                                ],
                                'layout': {
                                    'title': 'Domestic Isolation by Region',
                                }
                            }
                        ),

                        dcc.Graph(
                            id='graph_hospitalized',
                            figure={
                                'data': [
                                    {'x': [x for x in range(14)], 'y': [((y + region_metric['day']) * region_metric['coefficients'][0]) + region_metric['intercept'] for y in range(14)], 'type': 'line', 'name': region_metric['region_id']} 
                                    for region_metric in hospitalized
                                ],
                                'layout': {
                                    'title': 'Hospitalizations by Region',
                                }
                            }
                        ),

                        dcc.Graph(
                            id='graph_intensive_care',
                            figure={
                                'data': [
                                    {'x': [x for x in range(14)], 'y': [((y + region_metric['day']) * region_metric['coefficients'][0]) + region_metric['intercept'] for y in range(14)], 'type': 'line', 'name': region_metric['region_id']} 
                                    for region_metric in intensive_care
                                ],
                                'layout': {
                                    'title': 'Intensive Care by Region',
                                }
                            }
                        ),

                        dcc.Graph(
                            id='graph_deaths',
                            figure={
                                'data': [
                                    {'x': [x for x in range(14)], 'y': [((y + region_metric['day']) * region_metric['coefficients'][0]) + region_metric['intercept'] for y in range(14)], 'type': 'line', 'name': region_metric['region_id']} 
                                    for region_metric in deaths
                                ],
                                'layout': {
                                    'title': 'Deaths by Region',
                                }
                            }
                        ),
                        

                    ], # end card children
                    body=True
                ) # end card
            ], # end col children
        ), # end col
        justify='center'
    ) # end row
) # end container

def output(value):
    return value


if __name__ == "__main__":
    app.run_server(
        debug=True,
        port=8050,
        host='0.0.0.0' if len(sys.argv) > 1 and sys.argv[1] == "docker" else "127.0.0.1"
    )