import streamlit as st
from function import *
from datetime import date

fig = go.Figure()
st.write("""
# Covid19 Dashboard
[JHU CSSE COVID-19 DATASET]("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/") is used to get the data in this app.
""")

st.sidebar.write(
    'Coronavirus is officially a pandemic. Since the first case in decemberof 2019 the disease has spread fast reaching almost every corner of the world.' +
    'They said it\'s not a severe disease but the number of people that needs hospital care is growing as fast as the new cases.' +
    'Governments are taking measures to prevent a sanitary collapse to be able to take care of all these people.' +
    'Now Omicron which defined as new variant of corona virus spread all over the world hugely'+
    'So, I request all of you who see my project now please wear mask, use hand sanitizer , stay safe'+
    "I wish everyone's recovery as soon as possible"+
    'I\'m tackling this challenge here. Let\'s see how some countries/regions are doing!')

selected_date = st.sidebar.date_input(label="Select Date")
country=list(confirmed_df_melt['Country/Region'].unique())
country.insert(0,'Whole World')
selected_country = st.sidebar.selectbox('Select Country', options=country)
is_clicked = st.sidebar.button("Apply")
st.sidebar.header('Daily Cases Graph')
daily= st.sidebar.radio(" Choose one ",('Daily Confirmed Cases per 100k','Daily Confirmed Cases','Daily Recovered Cases','Daily Death Cases'))

if is_clicked:
    if selected_country=='Whole World':
        total_confirmed_df, total_deaths_df, total_recovered_df = select_date(selected_date)
        total_confirmed, total_deaths, total_recovered, total_active = cases(total_confirmed_df,
                                                                         total_deaths_df, total_recovered_df)

        figure1 = cases_for_a_specific_date(total_confirmed, total_deaths, total_recovered, total_active)

        figure2 = chloropleth_graph(total_confirmed_df)

        figure3, figure4 = SortByConfirmedAndDeathrate(total_confirmed_df, total_deaths_df)

    else:
        st.write(selected_country)
        total_confirmed_df, total_deaths_df, total_recovered_df = select_date_country(selected_date,selected_country)
        total_confirmed, total_deaths, total_recovered, total_active = cases(total_confirmed_df,
                                                                             total_deaths_df, total_recovered_df)

        figure1 = cases_for_a_specific_date(total_confirmed, total_deaths, total_recovered, total_active)

        figure2 = chloropleth_graph(total_confirmed_df)

        figure3, figure4 = SortByConfirmedAndDeathrate(total_confirmed_df, total_deaths_df)


    st.write("This Chart gives us a little summary on **Total Confirmed Cases**, **Total Death Cases**,"
             " **Total Recovery Cases** "
             "and **Total Active Cases** till now.")
    st.plotly_chart(figure1, use_container_width=True)

    st.write("This plot shows the **Chloropleth graph** of those countries in the dataset. Here the more dark colour "
             "denotes the low confirmed cases of that country and the less dark colour denotes the high confirmed "
             "cases of that country.")
    st.plotly_chart(figure2, use_container_width=True)

    st.write("This is the **Confirmed vs Deaths** Scatter plot in which the size of the circle is determined "
             "by the percentage of the death i.e. **Death Rate**.")
    st.plotly_chart(figure3, use_container_width=True)

    st.write("In this stacked graph I am drawing inference on **Top 20 countries which are highest in Deaths**. "
             "the bars denotes the **Death Count** and the line denotes the **Death Rate**")
    st.plotly_chart(figure4, use_container_width=True)





else:
    if selected_country=='Whole World':
        total_confirmed_df, total_deaths_df, total_recovered_df = select_date(date.today()-datetime.timedelta(1))
        total_confirmed, total_deaths, total_recovered, total_active = cases(total_confirmed_df,
                                                                         total_deaths_df, total_recovered_df)

        figure1 = cases_for_a_specific_date(total_confirmed, total_deaths, total_recovered, total_active)

        figure2 = chloropleth_graph(total_confirmed_df)

        figure3, figure4 = SortByConfirmedAndDeathrate(total_confirmed_df, total_deaths_df)

    else:
        st.write(selected_country)
        total_confirmed_df, total_deaths_df, total_recovered_df = select_date_country(selected_date,selected_country)
        total_confirmed, total_deaths, total_recovered, total_active = cases(total_confirmed_df,
                                                                             total_deaths_df, total_recovered_df)

        figure1 = cases_for_a_specific_date(total_confirmed, total_deaths, total_recovered, total_active)

        figure2 = chloropleth_graph(total_confirmed_df)

        figure3, figure4 = SortByConfirmedAndDeathrate(total_confirmed_df, total_deaths_df)


    st.write("This Chart gives us a little summary on **Total Confirmed Cases**, **Total Death Cases**,"
             " **Total Recovery Cases** "
             "and **Total Active Cases** till now.")
    st.plotly_chart(figure1, use_container_width=True)

    st.write("This plot shows the **Chloropleth graph** of those countries in the dataset. Here the more dark colour "
             "denotes the low confirmed cases of that country and the less dark colour denotes the high confirmed "
             "cases of that country.")
    st.plotly_chart(figure2, use_container_width=True)

    st.write("This is the **Confirmed vs Deaths** Scatter plot in which the size of the circle is determined "
             "by the percentage of the death i.e. **Death Rate**.")
    st.plotly_chart(figure3, use_container_width=True)

    st.write("In this stacked graph I am drawing inference on **Top 20 countries which are highest in Deaths**. "
             "the bars denotes the **Death Count** and the line denotes the **Death Rate**")
    st.plotly_chart(figure4, use_container_width=True)

if daily == 'Daily Confirmed Cases':
    figure5 = DailyConfirmedCases()
    st.write("In this graph, I am drawing inference on **Daily Confirmed Cases** across all the countries.")
    st.plotly_chart(figure5, use_container_width=True)
if daily == 'Daily Recovered Cases':
    figure6 = DailyRecoveredCases()
    st.write("In this graph, I am drawing inference on **Daily Recovered Cases** across all the countries.")
    st.plotly_chart(figure6, use_container_width=True)
if daily == 'Daily Death Cases':
    figure7 = DailyDeathCases()
    st.write("In this graph, I am drawing inference on **Daily Death Cases** across all the countries.")
    st.plotly_chart(figure7, use_container_width=True)
if daily == 'Daily Confirmed Cases per 100k':
    figure8 = DailyConfirmedCasesPer100k()
    st.write("In this graph, I am drawing inference on **Daily Confirmed Cases per 100k** across all the countries.")
    st.plotly_chart(figure8, use_container_width=True)




