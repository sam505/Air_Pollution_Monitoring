import streamlit as st


st.set_page_config(
        page_title="Air Pollution Dashboard",
        page_icon="chart_with_upwards_trend",
        layout='centered',
        initial_sidebar_state='auto'
    )


st.title("Air Quality Dashboard")

st.write("Welcome to our air quality visualization dashboard! Here, you can explore real-time air quality data from IoT devices in Kenya and Switzerland, as well as temperature and humidity readings from these regions.")

st.write("We understand the importance of clean air and the impact it has on our health and environment. That's why we've created this dashboard to provide you with a comprehensive view of the air quality in these two countries, using data collected by IoT devices.")

st.write("Our dashboard is updated every 15 minutes, providing you with the most current information on air quality levels in different cities across Kenya and Switzerland. You can use our dashboard to compare air quality levels between cities, track changes over time, and even see how air quality is affected by temperature and humidity.")

st.write("We hope that our air quality visualization dashboard will help you make informed decisions about your health and well-being, as well as contribute to a cleaner and healthier environment for everyone. Thank you for using our dashboard!")


