import firebase_admin
from firebase_admin import db
import json
import streamlit as st

if len(firebase_admin._apps) == 0:
	cred_obj = firebase_admin.credentials.Certificate("certificate.json")
	default_app = firebase_admin.initialize_app(cred_obj,
												{'databaseURL': "https://air-pollution-monitoring-a88eb-default-"
																"rtdb.firebaseio.com/"})
ref = db.reference("/")


def main():
	st.set_page_config(page_title="Air Pollution Dashboard", page_icon=None, layout='wide',
					   initial_sidebar_state='auto')
	st.title("Air Pollution Dashboard")
	data = ref.get()
	variables = data["data"].keys()
	for variable in variables:
		values = process_data(data["data"][variable])
		st.title("{} data".format(variable))
		st.line_chart(values)
		st.write("{} Data Points".format(len(values)))

def process_data(raw_data):
	processed_data = list(raw_data.values())
	return processed_data


if __name__ == "__main__":
	main()
