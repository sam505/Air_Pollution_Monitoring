import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utilities import *


regions = {
    "data": "Kericho",
    "Home": "Nairobi"
}
region = None
data_type = None
select_data = None


@st.cache_data(experimental_allow_widgets=True)
def initialize_sidebar(name):
    df = load_data(name)

    data_type = st.sidebar.radio(
        "Choose the Data to Visualize",
        ('Actual', 'Predicted'))
    if data_type == "Actual":
        select_data = st.sidebar.selectbox(
            "Sample Data By:",
            ("Actual", "Hourly", "Daily")
        )
        show_actual(df, select_data, name)
    else:
        show_predictions(df, name)




def main():
    df = load_counties_data()
    country_name = __file__.split(".")[0].split("_")[-1]
    df = df[df.Country == country_name]

    st.sidebar.subheader("Select Region")
    region = [st.sidebar.button(name) for name in df.City.unique()]
        
    if region[0]:
        name = list(regions.keys())[0]
        plot_map(df[df.City == regions[name]])
        initialize_sidebar(name)
        

    elif region[1]:
        name = list(regions.keys())[1]
        plot_map(df[df.City == regions[name]])
        initialize_sidebar(name)

    else:
        plot_map(df)

        

if __name__ == "__main__":
    main()
