from datetime import timedelta
from data_analysis import read_data
import streamlit as st
import pandas as pd
import plotly.express as px


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


def sample_data(df, choice):
    if choice == "Hourly":
        raw_df = df.set_index("timestamp")
        df = raw_df.resample(rule='H').mean()
        df.reset_index(inplace=True)
        return df
    elif choice == "Daily":
        raw_df = df.set_index("timestamp")
        df = raw_df.resample(rule='D').mean()
        df.reset_index(inplace=True)
        return df
    else:
        return df


def plot(df):
    line_chart(df, "datetime", "mq7", "Parts Per Million (PPM), CO","MQ7 Sensor Data")
    line_chart(df, "datetime", "mq135", "Parts Per Million (PPM), Air Quality", "MQ135 Sensor Data")
    line_chart(df, "datetime", "humidity", "Relative Humidity (%)", "Humidity Sensor Data")
    line_chart(df, "datetime", "temperature", "Degrees Celsius (°C)", "Temperature Sensor Data")


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
        "Choose the Data to Visualize Below",
        ("Actual", "Hourly", "Daily")
    )

    df["timestamp"] = pd.to_datetime(df['timestamp'], unit='s')
    df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
    df = sample_data(df, select_data)
    df = df.rename(columns={'timestamp': 'datetime'})
    df['date'] = df['datetime'].dt.date
    dates = df.date.to_list()
    date_range = st.sidebar.slider(
        'Select a range of Dates',
        dates[0], dates[len(dates) - 1],
        (dates[0], dates[-1]),
        step=timedelta(days=1)
    )
    df = df[(df['date'] >= date_range[0]) & (df['date'] <= date_range[1])]
    plot(df)
    st.text(f"Shape of Dataset {df.shape}")
    st.dataframe(df)


if __name__ == "__main__":
    main()
