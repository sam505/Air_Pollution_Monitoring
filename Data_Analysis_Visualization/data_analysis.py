import pandas as pd
import firebase_admin
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate("Data_Analysis_Visualization/certificate.json")
default_app = firebase_admin.initialize_app(cred_obj,
                                            {
                                                'databaseURL': "https://air-pollution-monitoring-a88eb-default-rtdb"
                                                               ".firebaseio.com/"})
ref = db.reference("/")


def main():
    read_data()


def read_data():
    datetime = []
    mq7 = []
    mq135 = []
    temp = []
    humidity = []
    data = ref.get()
    variables = data["data"].keys()
    for variable in variables:
        values = data["data"][variable]
        values = values.split("#")
        values = values[:4]
        try:
            datetime.append(variable)
            mq7.append(float(values[0]))
            mq135.append(float(values[1]))
            temp.append(float(values[2]))
            humidity.append(float(values[3]))
        except ValueError:
            print(values)
            pass
    print(len(datetime), len(mq7), len(mq135), len(temp), len(humidity))
    values_dict = {
        "timestamp": datetime,
        "mq7": mq7,
        "mq135": mq135,
        "temperature": temp,
        "humidity": humidity
    }
    df = pd.DataFrame(values_dict)
    filename = "data.csv"
    df.set_index("timestamp", inplace=True)
    df.to_csv(filename)
    return filename


if __name__ == "__main__":
    main()
