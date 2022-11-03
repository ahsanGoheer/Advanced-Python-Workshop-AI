# Import modules required for the streamlit app.
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import base64

# Define the name of the application.
st.title("S&P Dashboard App")

# Add some information about your application in markdown format.
markdown_data = """*This application has been designed to demonstrate the capabilities of Streamlit. The module allows Data Scientists to 
                   create and deploy quick dashboards and applications for their clients. Streamlit provides a wide variety of tools for developing
                   different kinds of solutions. This module can be especially helpful while desigining Proof-of-Concept solutions for the client
                   during pre-sales.*    
                   The current application is a dashboard for visualizing the closing prices of S&P 500 company stocks.
                   The data sources are as follows:  
                   1) [Wikipedia: list of S&P 500 companies](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)  
                   2) The Yfinance module in python. (To get the stock closing prices.)
                """
st.markdown(markdown_data)


# Set up a configurations side bar.
st.sidebar.header("Configurations")


# Write a function to fetch the S&P 500 companies data.
@st.cache
def load_comp_data(mode="offline"):

    path = "./S&P_company_data.csv"
    link = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    company_data = None
    if mode == "offline":
        company_data = pd.read_csv(path)
    elif mode == "online":
        company_data = pd.read_html(link)
        company_data = company_data[0]

    return company_data


# Load the company data.
company_data_df = load_comp_data(mode="offline")

# Get all the sectors present in the data.
sectors = list(company_data_df["GICS Sector"].unique())


# Get selected companies and sectors from the multi-select menu.
selected_sectors = st.sidebar.multiselect("Sector", sectors, sectors)

# Filter data based on selected companies and sectors.
if selected_sectors:
    company_data_df = company_data_df[
        (company_data_df["GICS Sector"].isin(selected_sectors))
    ]

# Get all the companies present in the data.
companies = list(company_data_df.Security.unique())


selected_companies = st.sidebar.multiselect("Company", companies, companies)

if selected_companies:
    company_data_df = company_data_df[
        (company_data_df["Security"].isin(selected_companies))
    ]

# Write a header for the new section of the application
st.header("Vizualize S&P 500 Company Data")
st.write(
    f"Selected data has the following dimensions : {company_data_df.shape[0]} rows \
    and {company_data_df.shape[1]} columns."
)

# Add dataframe to streamlit.
st.dataframe(company_data_df)

# Provide user the option to download data.
st.write(
    """You can also give the users the option to download the filtered data. \
       The documentation for how to do so can be found at:
       [Streamlit-Download File](https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806) 
    """
)

# Function that allows users to download the file from your application.
def download_file(dataframe):
    csv_format = dataframe.to_csv(index=False)
    csv_to_byte = base64.b64encode(csv_format.encode()).decode()
    hyperlink = f'<a href="data:file/csv;base64,{csv_to_byte}" download="SP500.csv">Download CSV File</a>'
    return hyperlink


st.markdown(download_file(company_data_df), unsafe_allow_html=True)


# Add a header for plotting section.
st.header("Visualize Closing Price")


# Loading stocks data.
stocks_data = pd.read_csv("./S&P_stock_data.csv")

# A function that takes the symbol i.e. company ticker and generates the stocks data plot for it.
def generate_price_plot(symbol):

    column_to_access = f"{symbol}|Close"
    plotting_data = pd.DataFrame(
        stocks_data[[column_to_access, "Date"]].values, columns=["Close", "Date"]
    )
    x = plotting_data.Date
    y = plotting_data.Close

    figure = go.Figure()
    figure.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name=symbol))
    figure.update_layout({"title": f"Closing Prices: {symbol}"})

    return figure


# Press button to generate plots functionality.
if st.button("Show Plots"):

    symbols = company_data_df.Symbol.unique()
    for symbol in symbols:
        st.write(generate_price_plot(symbol))
