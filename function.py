import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from bs4 import BeautifulSoup as soup
import datetime
base_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
confirmed_df = pd.read_csv(base_url + "time_series_covid19_confirmed_global.csv")
deaths_df = pd.read_csv(base_url + "time_series_covid19_deaths_global.csv")
recovered_df = pd.read_csv(base_url + "time_series_covid19_recovered_global.csv")

confirmed_df.drop(["Province/State", "Lat", "Long"], axis=1, inplace=True)
deaths_df.drop(["Province/State", "Lat", "Long"], axis=1, inplace=True)
recovered_df.drop(["Province/State", "Lat", "Long"], axis=1, inplace=True)

confirmed_df = confirmed_df.groupby("Country/Region").aggregate(np.sum).T
confirmed_df.index.name = "Date"
confirmed_df = confirmed_df.reset_index()

deaths_df = deaths_df.groupby("Country/Region").aggregate(np.sum).T
deaths_df.index.name = "Date"
deaths_df = deaths_df.reset_index()

recovered_df = recovered_df.groupby("Country/Region").aggregate(np.sum).T
recovered_df.index.name = "Date"
recovered_df = recovered_df.reset_index()

confirmed_df_melt = confirmed_df.melt(id_vars="Date")
deaths_df_melt = deaths_df.melt(id_vars="Date")
recovered_df_melt = recovered_df.melt(id_vars="Date")

confirmed_df_melt.rename(columns={"value": "Confirmed"}, inplace=True)
deaths_df_melt.rename(columns={"value": "Deaths"}, inplace=True)
recovered_df_melt.rename(columns={"value": "Recovered"}, inplace=True)

confirmed_df_melt['Date'] = pd.to_datetime(confirmed_df_melt['Date'])
deaths_df_melt['Date'] = pd.to_datetime(deaths_df_melt['Date'])
recovered_df_melt['Date'] = pd.to_datetime(recovered_df_melt['Date'])

confirmed_df_melt['Date'] = confirmed_df_melt['Date'].dt.strftime("%Y/%m/%d")
deaths_df_melt['Date'] = deaths_df_melt['Date'].dt.strftime("%Y/%m/%d")
recovered_df_melt['Date'] = recovered_df_melt['Date'].dt.strftime("%Y/%m/%d")

def select_date(date):
    date = date.strftime("%Y/%m/%d")

    total_confirmed_df = confirmed_df_melt[confirmed_df_melt['Date'] == date]
    total_deaths_df = deaths_df_melt[confirmed_df_melt['Date'] == date]
    total_recovered_df = recovered_df_melt[confirmed_df_melt['Date'] == date]

    return total_confirmed_df, total_deaths_df, total_recovered_df

def cases(total_confirmed_df, total_deaths_df, total_recovered_df):

    total_confirmed = total_confirmed_df['Confirmed'].sum()
    total_deaths = total_deaths_df['Deaths'].sum()
    total_recovered = total_recovered_df['Recovered'].sum()
    total_active = total_confirmed - total_deaths - total_recovered

    return total_confirmed, total_deaths, total_recovered, total_active

def cases_for_a_specific_date(total_confirmed, total_deaths, total_recovered, total_active):
    fig = go.Figure()
    fig.add_trace(go.Indicator(mode="number", value=int(total_confirmed),
                               number={'valueformat': 'f'},
                               title={'text': 'Total Confirmed Cases'},
                               domain={'row': 0, 'column': 0}))

    fig.add_trace(go.Indicator(mode='number', value=int(total_deaths),
                               number={'valueformat': 'f'},
                               title={'text': 'Total Death Cases'},
                               domain={'row': 0, 'column': 1}))

    fig.add_trace(go.Indicator(mode='number', value=int(total_recovered),
                               number={'valueformat': 'f'},
                               title={'text': 'Total Recovered Cases'},
                               domain={'row': 1, 'column': 0}))

    fig.add_trace(go.Indicator(mode='number', value=int(total_active),
                               number={'valueformat': 'f'},
                               title={'text': 'Total Active Cases'},
                               domain={'row': 1, 'column': 1}))

    fig.update_layout(grid={'rows': 2, 'columns': 2, 'pattern': 'independent'})

    return fig

def chloropleth_graph(total_confirmed_df):
    pd.set_option('mode.chained_assignment', None)
    fig = px.choropleth(total_confirmed_df,
                        locations='Country/Region', locationmode='country names',
                        color_continuous_scale=px.colors.sequential.Plasma,
                        color=np.log10(total_confirmed_df['Confirmed']),
                        range_color=(0, 10))

    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
    )

    return fig

def SortByConfirmedAndDeathrate(total_confirmed_df, total_deaths_df):
    A = total_confirmed_df.copy()
    A['Deaths'] = total_deaths_df['Deaths']
    A['DeathRate'] = (A['Deaths'] / A['Confirmed'] * 100).round(2)
    fig1 = px.scatter(A.sort_values('Confirmed', ascending=False).head(20),
                     x='Confirmed', y='Deaths', size='DeathRate', color='Country/Region')

    B = A.copy()
    B = B.sort_values('Deaths', ascending=False).head(20)

    fig2 = make_subplots(specs=[[{'secondary_y': True}]])
    fig2.add_trace(go.Bar(x=B['Country/Region'], y=B['Deaths'],
                         text=B['Deaths'], name='Deaths',
                         textposition='auto'), secondary_y=False)

    fig2.add_trace(go.Scatter(x=B['Country/Region'], y=B['DeathRate'],
                             text=B['DeathRate'], name='DeathRate (%)',
                             mode='markers+lines'), secondary_y=True)

    return fig1, fig2


def DailyConfirmedCases():
    C1 = confirmed_df_melt.groupby('Date').aggregate(np.sum)
    C1.index.name = 'Date'
    C1['DailyConfirmed'] = C1['Confirmed'].diff()
    C1 = C1.reset_index()

    fig = px.area(C1, x='Date', y='DailyConfirmed')

    return fig
def DailyRecoveredCases():
    C2 = recovered_df_melt.groupby('Date').aggregate(np.sum)
    C2.index.name = 'Date'
    C2['DailyRecovered'] = C2['Recovered'].diff()
    C2 = C2.reset_index()

    fig = px.bar(C2, x='Date', y='DailyRecovered')

    return fig

def DailyDeathCases():
    C3 = deaths_df_melt.groupby('Date').aggregate(np.sum)
    C3.index.name = 'Date'
    C3['DailyDeath'] = C3['Deaths'].diff()
    C3 = C3.reset_index()

    fig = px.area(C3, x='Date', y='DailyDeath')

    return fig

def DailyConfirmedCasesPer100k():
    # Retrieving the population data for all countries
    url = "https://www.worldometers.info/world-population/population-by-country/"
    r = requests.get(url)
    bs = soup(r.content, 'html')
    table = bs.find_all('table')[0]
    population_df = pd.read_html(str(table))[0]

    # Some basic preprocessing
    population_df.rename(columns={'Country (or dependency)': "Country/Region", "Population (2020)": "Population"},inplace=True)
    population_df.drop(population_df.columns.difference(['Country/Region', 'Population']), axis=1, inplace=True)
    population_df.replace("United States", "US", inplace=True)

    # Daily confirmed cases per 100k across all countries for previous 2 weeks
    today = datetime.datetime.now()
    minus14 = today - datetime.timedelta(weeks=2)
    minus14 = minus14.strftime("%Y/%m/%d")
    D = confirmed_df_melt.copy()
    D = D[D['Date'] >= minus14]

    # Making the daily cases column
    D['Daily'] = D.groupby('Country/Region')['Confirmed'].diff()
    D.drop(['Date', 'Confirmed'], axis=1, inplace=True)
    D = D.groupby('Country/Region').sum()
    D = D.sort_values('Daily', ascending=False)

    # Making the per100k column after merging the population dataframe with the Dataframe D
    E = pd.merge(left=D, right=population_df, left_on='Country/Region', right_on='Country/Region')
    E['per100k'] = (E['Daily'] * 100000) / E['Population']
    fig = px.bar(E.sort_values('per100k', ascending=False).head(30).round(2),
                 x="Country/Region", y="per100k", text="per100k")

    return fig


def select_date_country(date,country):
    date = date.strftime("%Y/%m/%d")

    total_confirmed_df = confirmed_df_melt[(confirmed_df_melt['Date'] == date)&( confirmed_df_melt['Country/Region'] == country) ]
    total_deaths_df = deaths_df_melt[(confirmed_df_melt['Date'] == date)&( confirmed_df_melt['Country/Region'] == country)]
    total_recovered_df = recovered_df_melt[(confirmed_df_melt['Date'] == date)&( confirmed_df_melt['Country/Region'] == country)]

    return total_confirmed_df, total_deaths_df, total_recovered_df

def DailyConfirmedCases_country():
    C4 = confirmed_df_melt.groupby(['Date','Country/Region']).aggregate(np.sum)
    C4.index.name = 'Country/Region'
    C4['DailyConfirmed'] = C4['Confirmed'].diff()
    C4 = C4.reset_index()

    fig = px.area(C4, x='Date', y='DailyConfirmed')

    return fig
def DailyRecoveredCases_country():
    C5 = recovered_df_melt.groupby(['Date','Country/Region']).aggregate(np.sum)
    C5.index.name = 'Country/Region'
    C5['DailyRecovered'] = C5['Recovered'].diff()
    C5 = C5.reset_index()

    fig = px.bar(C5, x='Date', y='DailyRecovered')

    return fig

def DailyDeathCases_country():
    C6 = deaths_df_melt.groupby(['Date','Country/Region']).aggregate(np.sum)
    C6.index.name = 'Country/Region'
    C6['DailyDeath'] = C6['Deaths'].diff()
    C6 = C6.reset_index()

    fig = px.area(C6, x='Date', y='DailyDeath')

    return fig