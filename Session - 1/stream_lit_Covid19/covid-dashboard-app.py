# Import modules required by the application.

import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import numpy as np


# Define the title of the application.
st.title("Covid - 19 Dashboard")


# Write information about the application.
application_details = """ This application is a demo of how streamlit can be used to create 
interactive dashboards.  
The data used in the creation of this application  has been taken from [WHO](https://covid19.who.int/data)
"""

st.markdown(application_details)


# Adding header image to the application
st.image("./assets/COVID19_share.jpg")


# Add a header for the dashboard section.
st.header("Covid 19 Visualizations")

# Load covid-19 cases data.
@st.cache
def load_data():
    covid_data_path = "./covid_datasets/WHO-COVID-19-global-data.csv"
    covid_cases_data = pd.read_csv(covid_data_path)
    return covid_cases_data


# Get covid data that needs to be visualized.
covid_data_df = load_data()


# Generate bar chart for all the cases reported.
min_date = covid_data_df["Date_reported"].min()
max_date = covid_data_df["Date_reported"].max()

# Add information about the vizualization that is being generated.
st.markdown(f"Cases reported from {min_date} till {max_date}")

# Write a function that can create the data needed for the bar chart.
@st.cache
def get_barchart_data(covid_df):

    bar_chart_df = covid_df.groupby(["Country"]).agg({"New_cases": "sum"}).reset_index()
    return bar_chart_df


# Fetch the barchart data.
barchart_df = get_barchart_data(covid_data_df)

# Add a header to the side bar for barchart configurations.
st.sidebar.header("Global Barchart Controls")

# Add a multiselect for countries to filter countries for the barchart.
selected_countries = st.sidebar.multiselect(
    "Countries", barchart_df["Country"].unique(), barchart_df["Country"].unique()[:5]
)
barchart_df = barchart_df[barchart_df["Country"].isin(selected_countries)]

# If there are countries in the multi select add a slider to control the number of countries.
if selected_countries:
    Num_countries_to_show = st.sidebar.slider(
        "Num Countries",
        0,
        len(barchart_df["Country"].unique()),
        len(barchart_df["Country"].unique()),
    )
    countries = barchart_df.Country.unique()
    countries = countries[:Num_countries_to_show]
    barchart_df = barchart_df[barchart_df["Country"].isin(countries)]

# Create a function that generates a barchart from the given data.
def plot_barchart(barchart_df):

    barchart_fig = go.Figure()
    countries = barchart_df.Country.unique()
    for country in countries:
        x = barchart_df[barchart_df["Country"] == country].Country
        y = barchart_df[barchart_df["Country"] == country].New_cases
        barchart_fig.add_trace(go.Bar(x=x, y=y, name=country))
    return barchart_fig


# Add bar chart to the application.
st.plotly_chart(plot_barchart(barchart_df), use_container_width=True)


# Add side bar for filters and configurations.
st.sidebar.header("Country Specific Plot Controls")


# Add countries to the filters.
countries = list(covid_data_df.Country.unique())


# Add Dropdown menu for countries to the sidebar.
selected_country = st.sidebar.selectbox("Country", countries)


# Filter the dataframe based on the selected country.
if selected_country:
    country_df = covid_data_df[covid_data_df["Country"] == selected_country]

# Display covid data for the country selected.
st.markdown(f"<h2>Covid Stats for {selected_country}</h2>", unsafe_allow_html=True)
st.dataframe(country_df, use_container_width=True)

# Create a plot for the cases reported in the selected couuntry.
st.markdown(f"<h3> Covid Cases Reported Daily Since 2020</h3>", unsafe_allow_html=True)

# Create a function to generate a plot for covid cases.
def plot_covid_cases(country_df):

    covid_cases_fig = go.Figure()
    country = country_df.Country.unique()
    x = country_df.Date_reported
    y = country_df.New_cases

    covid_cases_fig.add_trace(go.Bar(x=x, y=y, name="Daily Cases"))
    covid_cases_fig.add_trace(go.Scatter(x=x, y=y, name="Daily Cases", mode="lines"))
    covid_cases_fig.update_layout(
        title=f"Daily Covid Cases - {country[0]}",
        xaxis_title="Dates",
        yaxis_title="Covid Cases",
    )
    return covid_cases_fig


# Create a function to generate plots for the cumulative covid cases.
def plot_cumulative_covid_cases(country_df):

    covid_cases_fig = go.Figure()
    country = country_df.Country.unique()
    x = country_df.Date_reported
    y = country_df.Cumulative_cases

    covid_cases_fig.add_trace(
        go.Scatter(x=x, y=y, name="Cummulative Cases", mode="lines")
    )
    covid_cases_fig.update_layout(
        title=f"Covid Cases - {country[0]}",
        xaxis_title="Dates",
        yaxis_title="Cummulative Covid Cases",
    )

    return covid_cases_fig


# Add covid cases plot to the application.
st.plotly_chart(plot_covid_cases(country_df), use_container_width=True)

# Add cumulative covid cases plot to the application.
st.plotly_chart(plot_cumulative_covid_cases(country_df), use_container_width=True)

# Add a heading for the vaccination data.
st.markdown(
    f"<h3> Vaccinations Data for {selected_country} </h3>", unsafe_allow_html=True
)

# Create a function to load the vaccination data.
@st.cache
def load_vaccinations_data():
    vacc_data_path = "./covid_datasets/vaccination-data.csv"
    vacc_data_df = pd.read_csv(vacc_data_path)
    return vacc_data_df


# Get vaccination data.
vacc_data_df = load_vaccinations_data()

# Filter the vaccination data according to user input.
vacc_data_df = vacc_data_df[vacc_data_df["COUNTRY"] == selected_country]
dates = sorted(list(vacc_data_df.DATE_UPDATED))
st.sidebar.header("Vaccination Data Filter")
selected_date = st.sidebar.selectbox("Dates", dates)
vacc_data_df = vacc_data_df[vacc_data_df["DATE_UPDATED"] == selected_date]

# Create a function to generate a pie chart for vaccination.
def get_vacc_piechart(vacc_data_df):

    labels = ["First Dose", "Fully Vaccinated", "Booster Dose"]

    y = (
        vacc_data_df[
            [
                "PERSONS_VACCINATED_1PLUS_DOSE",
                "PERSONS_FULLY_VACCINATED",
                "PERSONS_BOOSTER_ADD_DOSE",
            ]
        ]
        .fillna(0)
        .astype(int)
        .values.tolist()
    )
    if y:
        pie_chart_fig = go.Figure(
            data=[go.Pie(labels=labels, values=y[0], name="Vaccination Chart")]
        )

        pie_chart_fig.update_traces(hoverinfo="label+percent", textinfo="value")

    return pie_chart_fig


# Add the pie chart to the application.
st.plotly_chart(get_vacc_piechart(vacc_data_df), use_container_width=True)

