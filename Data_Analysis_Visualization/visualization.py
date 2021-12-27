from datetime import timedelta

from data_analysis import read_data
import streamlit as st
import pandas as pd


def main():
    st.set_page_config(page_title="Air Pollution Dashboard", page_icon=None, layout='wide',
                       initial_sidebar_state='auto')
    st.title("Air Pollution Dashboard")
    filename = read_data()
    df = pd.read_csv(filename)
    df = df.dropna()
    add_select_box = st.sidebar.selectbox(
        "Which data would you like to visualize?",
        ("Actual", "Predicted")
    )
    df["timestamp"] = pd.to_datetime(df['timestamp'], unit='s')
    df["timestamp"] = df["timestamp"].dt.tz_localize('UTC')
    df = df.rename(columns={'timestamp': 'index'})
    df['date'] = df['index'].dt.date
    dates = df.date
    date_range = st.sidebar.slider(
        'Select a range of values',
        dates[0], dates[len(dates) - 1],
        (dates[int(0.1 * len(dates))], dates[int(0.25 * len(dates))]),
        step=timedelta(days=1)
    )
    df = df[df.date.isin([date_range[0], date_range[1]])]
    print(df)
    st.text(date_range)
    df_mq7 = df[["index", "mq7"]].set_index('index')
    df_mq135 = df[["index", "mq135"]].set_index('index')
    df_temp = df[["index", "temperature"]].set_index('index')
    df_humidity = df[["index", "humidity"]].set_index('index')
    # st.text(df_mq7)
    st.subheader("MQ7 Sensor Data")
    st.line_chart(df_mq7)
    # st.text(df_mq135)
    st.subheader("MQ135 Sensor Data")
    st.line_chart(df_mq135)
    # st.text(df_temp)
    st.subheader("Temperature Data")
    st.line_chart(df_temp)
    # st.text(df_humidity)
    st.subheader("Humidity Data")
    st.line_chart(df_humidity)
    # st.text(df)


if __name__ == "__main__":
    main()
