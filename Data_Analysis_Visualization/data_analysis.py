import pandas as pd
import firebase_admin
from firebase_admin import db
import os
import pickle
import json


filename = "Data_Analysis_Visualization/certificate.json"
pickle_path = "Data_Analysis_Visualization/certificate.pickle"


def pickle_to_json():
    """
    """
    with open(pickle_path, "rb") as data:
        data = pickle.load(data)
    with open(filename, 'w') as fp:
        json.dump(data, fp)


pickle_to_json()

cred_obj = firebase_admin.credentials.Certificate(filename)
default_app = firebase_admin.initialize_app(cred_obj,
                                            {
                                                'databaseURL': "https://air-pollution-monitoring-a88eb-default-rtdb"
                                                               ".firebaseio.com/"})
ref = db.reference("/")
os.remove(filename)


def main():
    read_data()


def read_data(name):
    data = ref.get()
    datetime = []
    mq7 = []
    mq8 = []
    mq135 = []
    temp = []
    humidity = []
    data = data[name]
    variables = data.keys()
    for variable in variables:
        raw_values = data[variable]
        try:
            assert raw_values[0] == "#"
            assert raw_values[1] != "#"
            if name == "data":
                values = raw_values.split("#")[1:5]
            elif name == "Swiss":
                values = raw_values.split("#")[1:9]

            for i in range(4):
                float(values[i])
                assert values[i] != ""
        except AssertionError:
            values = raw_values.split("##")[1]
            values = values.split("#")
        except ValueError:
            try:
                values = raw_values.split("##")[1]
                values = values.split("#")
            except IndexError:
                pass
        else:
            if name == "data":
                datetime.append(variable)
                mq7.append(float(values[0]))
                mq135.append(float(values[1]))
                temp.append(float(values[2]))
                humidity.append(float(values[3]))
            
            elif name == "Swiss":
                datetime.append(variable)
                mq7.append(float(values[0]))
                mq8.append(float(values[1]))
                mq135.append(float(values[2]))
                temp.append(float(values[-2]))
                humidity.append(float(values[-1]))
    
    if name == "data":
        values_dict = {
            "timestamp": datetime,
            "mq7": mq7,
            "mq135": mq135,
            "temperature": temp,
            "humidity": humidity
        }
    elif name == "Swiss":
        values_dict = {
            "timestamp": datetime,
            "mq7": mq7,
            "mq8": mq8,
            "mq135": mq135,
            "temperature": temp,
            "humidity": humidity
        }
    df = pd.DataFrame(values_dict)
    file_name = f"{name}.csv"
    df.set_index("timestamp", inplace=True)
    df.to_csv(file_name)
    return file_name


if __name__ == "__main__":
    main()
