import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utilities import *


regions = {
    "data": "Kericho",
    "Home": "Nairobi"
}


def main():
    df = load_counties_data()
    country_name = __file__.split(".")[0].split("_")[-1]
    df = df[df.Country == country_name]

    st.sidebar.subheader("Select Region")
    region = [st.sidebar.button(name) for name in df.City.unique()]
        
    if region[0]:
        name = "data"
        plot_map(df[df.City == regions[name]])
        

    elif region[1]:
        name = "Home"
        plot_map(df[df.City == regions[name]])

    else:
        plot_map(df)

    if sum(region) != 0:
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


if __name__ == "__main__":
    main()
