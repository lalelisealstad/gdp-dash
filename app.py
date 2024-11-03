from flask import Flask
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from src.func import get_country_gdp, get_dict_countries, make_gdp_fig, get_last_gdp, publish_country_selection

# Initialize Flask
server = Flask(__name__)

# Initialize Dash
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.FLATLY])

app.layout = html.Div(
    [
        dbc.Row(
            [
                # Sidebar
                dbc.Col(
                    [
                        html.H1('Find country GDP'),
                        html.P('Search for a country in the dropdown menu below and see how GDP has grown over time.'),
                        dcc.Dropdown(
                            id='searchable-dropdown',
                            options=get_dict_countries(),
                            value='US',
                            placeholder='Select country',
                            searchable=True,
                            ),
                    ],
                    xs=10, sm=10, md=10, lg=3, xl=3,
                    className='sidebar',
                    
                ),
                # Main content
                dbc.Col(
                    [
                        # Second row with figure
                        dbc.Row([
                            html.Div(id='country-gdp-text', className='sometext'), 
                            dbc.Col(dcc.Graph(id='timeline-graph')),]
                        ),
                    ],
                    xs=10, sm=10, md=10, lg=8, xl=8,
                    className='content'
                ),
            ],
        ),
    ],
)


@app.callback([Output('timeline-graph', component_property='figure'), 
               Output('country-gdp-text', component_property='children'), ],
              Input('searchable-dropdown', component_property='value')
              )

def update_components(country_code): 
    
    dict_countries = get_dict_countries() 
    
    data = get_country_gdp(country_code)
    
    country_name = dict_countries[country_code]
    
    # publish to pubsub for monitoring
    publish_country_selection(country_name)
    
    fig = make_gdp_fig(data, country_name)
    
    latest_date, gdp_in_billions = get_last_gdp(country_name, data)
    
    country_gdp_text = f"{country_name} GDP in {latest_date} was {gdp_in_billions} billion (current US dollars $)"
    
    
    return fig, country_gdp_text



# Run Flask server
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8080, debug=False)
