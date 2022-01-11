from datetime import timedelta
from data_analysis import read_data
import streamlit as st
import pandas as pd
import plotly.express as px


def line_chart(df, x, y, title):
    fig = px.line(df, x=x, y=y)
    fig.update_xaxes(title_text='Date/Time')
    fig.update_yaxes(title_text='Parts Per Million (PPM)')
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        })
    st.plotly_chart(fig, use_container_width=True)


def plot(df):
    line_chart(df, "datetime", "mq7", "MQ7 Sensor Data")
    line_chart(df, "datetime", "mq135", "MQ135 Sensor Data")
    line_chart(df, "datetime", "humidity", "Humidity Sensor Data")
    line_chart(df, "datetime", "temperature", "Temperature Sensor Data")


def main():
    st.set_page_config(
        page_title="Air Pollution Dashboard",
        page_icon="chart_with_upwards_trend",
        layout='wide',
        initial_sidebar_state='auto'
    )
    st.title("Air Pollution Dashboard")
    filename = read_data()
    df = pd.read_csv(filename)
    df = df.dropna()
    select_data = st.sidebar.selectbox(
        "Which data would you like to visualize?",
        ("Actual", "Predicted", "Both")
    )
    st.text(select_data)
    df["timestamp"] = pd.to_datetime(df['timestamp'], unit='s')
    df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
    df = df.rename(columns={'timestamp': 'datetime'})
    df['date'] = df['datetime'].dt.date
    dates = df.date
    date_range = st.sidebar.slider(
        'Select a range of Dates',
        dates[0], dates[len(dates) - 1],
        (dates[int(0.1 * len(dates))], dates[int(0.25 * len(dates))]),
        step=timedelta(days=1)
    )
    df = df[(df['date'] >= date_range[0]) & (df['date'] <= date_range[1])]
    plot(df)
    st.text(f"Shape of Dataset {df.shape}")
    st.dataframe(df)


if __name__ == "__main__":
    main()
