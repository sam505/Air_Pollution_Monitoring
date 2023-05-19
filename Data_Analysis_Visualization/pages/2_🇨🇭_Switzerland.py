import pandas as pd
import streamlit as st
from utilities import *
import plotly.express as px
from datetime import timedelta
import plotly.graph_objects as go
from data_analysis import read_data



def line_chart(df, x, y, units, title):
    fig = px.line(df, x=x, y=y)
    fig.update_xaxes(title_text='Date/Time')
    fig.update_yaxes(title_text=units)
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        })
    st.plotly_chart(fig, use_container_width=True)


def main():
    df = load_counties_data()
    country_name = __file__.split(".")[0].split("_")[-1]
    df = df[df.Country == country_name]

    # select_data = st.sidebar.selectbox(
    #         "Select Region",
    #         df.City.unique(),
    #     )
    
    plot_map(df)

    name = "Swiss"
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


