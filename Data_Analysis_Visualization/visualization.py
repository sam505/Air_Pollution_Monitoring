from data_analysis import read_data
import streamlit as st
import pandas as pd


def main():
    st.set_page_config(page_title="Air Pollution Dashboard", page_icon=None, layout='centered',
                       initial_sidebar_state='auto')
    st.title("Air Pollution Dashboard")
    filename = read_data()
    df = pd.read_csv(filename)
    df.dropna()
    df["timestamp"] = pd.to_datetime(df['timestamp'], unit='s')
    df["timestamp"] = df["timestamp"].dt.tz_localize('UTC')
    df.timestamp = df.timestamp.dt.tz_convert('Africa/Nairobi')
    df = df.rename(columns={'timestamp': 'index'})
    df_mq7 = df[["index", "mq7"]].set_index('index')
    df_mq135 = df[["index", "mq135"]].set_index('index')
    df_temp = df[["index", "temperature"]].set_index('index')
    df_humidity = df[["index", "humidity"]].set_index('index')
    # st.text(df_mq7)
    st.line_chart(df_mq7)
    # st.text(df_mq135)
    st.line_chart(df_mq135)
    # st.text(df_temp)
    st.line_chart(df_temp)
    # st.text(df_humidity)
    st.line_chart(df_humidity)
    # st.text(df)


if __name__ == "__main__":
    main()
