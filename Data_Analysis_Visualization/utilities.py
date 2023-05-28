import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import timedelta
import plotly.graph_objects as go
from data_analysis import read_data
from make_predictions import make_prediction


def load_data(name):
    filename = read_data(name)
    df = pd.read_csv(filename)
    df = df.dropna()
    df["timestamp"] = pd.to_datetime(df['timestamp'], unit='s')
    if name == "Swiss":
        df["timestamp"] = df["timestamp"].dt.tz_localize("UTC", ambiguous='infer')
    else:
         df["timestamp"] = df["timestamp"].dt.tz_localize("Africa/Nairobi")
    
    if name != "data":
        raw_df = df.set_index("timestamp")
        df = raw_df.resample(rule='5T').mean()
        df.reset_index(inplace=True)

    return df


@st.cache_data()
def load_counties_data():
	countries_df = pd.read_csv("Data_Analysis_Visualization/countries_data.csv", index_col=None)

	return countries_df


@st.cache_data(show_spinner=False)
def plot_map(df):
	st.map(df)


@st.cache_data(show_spinner=False)
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
def plot(df, name):
    line_chart(df, "datetime", "mq7", "Parts Per Million (PPM), CO", "MQ7 Sensor Data")
    if name != "data":
         line_chart(df, "datetime", "mq8", "Parts Per Million (PPM), Hydrogen Gas", "MQ8 Sensor Data")
    line_chart(df, "datetime", "mq135", "Parts Per Million (PPM), Air Quality", "MQ135 Sensor Data")
    line_chart(df, "datetime", "humidity", "Relative Humidity (%)", "Humidity Sensor Data")
    line_chart(df, "datetime", "temperature", "Degrees Celsius (°C)", "Temperature Sensor Data")
    

@st.cache_data(experimental_allow_widgets=True, show_spinner=False)
def show_actual(df, select_data, name):
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
    plot(df, name)


@st.cache_data(show_spinner=False)
def show_predictions(df, name):
    if name == "data":
        results = make_prediction()
        mq7_pred = results[0]
        mq135_pred = results[1]

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=df.timestamp, y=df.mq7,
                                    mode='lines',
                                    name='Actual'))
        fig1.add_trace(go.Scatter(x=mq7_pred.index, y=mq7_pred.mean(axis=1),
                                    mode='lines',
                                    name='Predicted'))
        fig1.update_xaxes(title_text='Date/Time')
        fig1.update_yaxes(title_text="Parts Per Million")
        fig1.update_layout(
            title={
                'text': "MQ7 Sensor Data vs Forecasted Values against Time",
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            })
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df.timestamp, y=df.mq135,
                                    mode='lines',
                                    name='Actual'))
        fig2.add_trace(go.Scatter(x=mq135_pred.index, y=mq135_pred.mean(axis=1),
                                    mode='lines',
                                    name='Predicted'))
        fig2.update_xaxes(title_text='Date/Time')
        fig2.update_yaxes(title_text="Parts Per Million")
        fig2.update_layout(
            title={
                'text': "MQ135 Sensor Data vs Forecasted Values against Time",
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            })
        st.plotly_chart(fig2, use_container_width=True)
    else:
         st.warning("Models in training. Predictions will be available soon...")
    