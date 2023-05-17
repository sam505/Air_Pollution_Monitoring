from datetime import timedelta
from data_analysis import read_data
from make_predictions import make_prediction
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



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


@st.cache_data
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


@st.cache_data
def plot(df):
    line_chart(df, "datetime", "mq7", "Parts Per Million (PPM), CO", "MQ7 Sensor Data")
    line_chart(df, "datetime", "mq8", "Parts Per Million (PPM), Hydrogen Gas", "MQ8 Sensor Data")
    line_chart(df, "datetime", "mq135", "Parts Per Million (PPM), Air Quality", "MQ135 Sensor Data")
    line_chart(df, "datetime", "humidity", "Relative Humidity (%)", "Humidity Sensor Data")
    line_chart(df, "datetime", "temperature", "Degrees Celsius (°C)", "Temperature Sensor Data")


@st.cache_resource
@st.cache_data
def load_data():
    filename = read_data("Swiss")
    df = pd.read_csv(filename)
    df = df.dropna()
    df["timestamp"] = pd.to_datetime(df['timestamp'], unit='s')
    df["timestamp"] = df["timestamp"].dt.tz_localize("UTC", ambiguous='infer')
    raw_df = df.set_index("timestamp")
    df = raw_df.resample(rule='5T').mean()
    df.reset_index(inplace=True)

    return df


@st.cache_data(experimental_allow_widgets=True)
def show_actual(df, select_data):
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
    # st.text(f"Shape of Dataset {df.shape}")
    # st.dataframe(df)


@st.cache_data
def show_predictions():
    st.warning("Models in training. Predictions will be available soon...")



def main():
    df = pd.DataFrame(
        [[46.9480, 7.4474]], 
        columns=["lat", "lon"])

    st.map(df)

    df = load_data()
    data_type = st.sidebar.radio(
        "Choose the Data to Visualize",
        ('Actual', 'Predicted'))
    if data_type == "Actual":
        select_data = st.sidebar.selectbox(
            "Sample Data By:",
            ("Actual", "Hourly", "Daily")
        )
        show_actual(df, select_data)
    else:
        show_predictions()


if __name__ == "__main__":
    main()


