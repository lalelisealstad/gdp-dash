
import wbdata
import pandas as pd

def get_dict_countries(): 
    countries = wbdata.get_countries()
    countries_df = pd.DataFrame(countries)
    countries_df = countries_df[['name', 'iso2Code']]
    dict_c = dict(zip(countries_df['iso2Code'], countries_df['name']))
    return dict_c



import wbdata
import pandas as pd
from datetime import datetime

def get_country_gdp(country_code): 
    indicator = 'NY.GDP.MKTP.CD'   
    
    data = wbdata.get_dataframe({indicator: 'GDP'}, country=country_code)
    
    data = (
        data.reset_index()
        .sort_values(by='date')
        .dropna()
    )
    
    return data



import plotly.graph_objects as go

def make_gdp_fig(data, country_name): 
    

    fig = go.Figure()

    # Add the GDP line with the corrected color
    fig.add_trace(go.Scatter(
        x=data['date'],  # x-axis is the date
        y=data['GDP'],   # y-axis is the GDP value
        mode='lines',
        line=dict(width=2, color='#66FCF1'),
    ))
    #45A29E
    # Update the layout to remove grids and show x-axis ticks every 10 years
    fig.update_layout(
        title=f"GDP for {country_name}",
        xaxis_title="Year",
        yaxis_title="GDP (current US$)",
        template="plotly_white",
        font=dict(family="Helvetica, Arial", size=12),
        hovermode="x unified",
        margin=dict(l=40, r=40, t=80, b=40),
        title_font=dict(size=24, color='#66FCF1'),
        plot_bgcolor='#0B0C10',
        paper_bgcolor='#0B0C10',
        xaxis=dict(
            tickmode='array',
            tickvals=[year for year in range(int(min(data['date'])), int(max(data['date'])) + 1, 10)],  # Every 10 years
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            showgrid=False  
        ),
        yaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            showgrid=False  
        )
    )

    return fig

import numpy as np
def get_last_gdp(country_name, data):
    
    max_row = data.sort_values(by='date', ascending=False).iloc[0]
    max_row.date
    gdp_in_billions = np.round((int(max_row.GDP)/ 1_000_000_000),3)
    text = f"{country_name} GDP in {max_row.date} was {gdp_in_billions} billion (current US dollars $)"
    
    return text