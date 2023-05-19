import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utilities import *


def main():
    df = load_counties_data()
    country_name = __file__.split(".")[0].split("_")[-1]
    df = df[df.Country == country_name]

    select_data = st.sidebar.selectbox(
            "Select Region",
            df.City.unique(),
        )
    
    plot_map(df)
    name = "data"

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
