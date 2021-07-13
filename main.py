# Import libraries
import numpy as np
import pandas as pd
import plotly as py
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)


def dataSet():
    # Reads DataSet
    global df
    df = pd.read_csv("covid_19_data.csv")

    # format numbers
    pd.options.display.float_format = '{:,.2f}'.format

    # Rename columns
    df = df.rename(columns={'Country/Region': 'Country'})
    df = df.rename(columns={'ObservationDate': 'Date'})


def manipulates():

    # Manipulate Dataframe
    global df_countries
    df_countries = df.groupby(['Country', 'Date']).sum(
    ).reset_index().sort_values('Date', ascending=False)

    df_countries

    # Removes entires that has the same country name
    df_countries = df_countries.drop_duplicates(subset=['Country'])
    df_countries = df_countries[df_countries['Confirmed'] > 0]


def createsChoropleth():
    # Create the Choropleth
    global fig
    fig = go.Figure(data=go.Choropleth(
        # Displays the name of the country when you hover over it
        locations=df_countries['Country'],
        locationmode='country names',
        z=df_countries['Confirmed'],
        colorbar=dict(  # adds info to color bar
            title="Confirmed Cases",
            x=1.05,
            thickness=175
        ),
        # Colorset what will be used for Map
        colorscale='ylgn',
        marker_line_color='black',  # Outline of Countries
        marker_line_width=.75,  # width of line that divides country

    ))

    fig.update_layout(
        title='Confirmed Cases of Coronavirus as of March 2021',  # Gives title to map
        title_x=.5,  # referes to variable title and adds margin
        legend_bgcolor="#444",
        legend_borderwidth=200,  # sets width in pixels
        showlegend=True,
        geo=dict(
            showframe=True,
            showcoastlines=True,
            projection_type='equirectangular'  # The container in which map is displayed
        ),
        font=dict(
            family="Arial",
            size=20,
            color="#7f7f7f",
        ),

    )


def display():
    # Displays choropleth and writes to html file
    fig.show()
    fig.write_html("map.html")


def main():
    # retrieves info
    dataSet()

    # Manipulates dataset
    manipulates()

    # Creates Choropleth
    createsChoropleth()

    # Displays choropleth
    display()


main()
