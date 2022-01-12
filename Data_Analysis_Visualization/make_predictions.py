import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator


def main():
    """
    Main function
    """
    df = pd.read_csv("Data_Analysis_Visualization/data.csv")
    print(df)
    model1 = tf.keras.models.load_model('mq7_model.model')
    model2 = tf.keras.models.load_model('mq135_model.model')

    df["timestamp"] = pd.to_datetime(df['timestamp'], unit='s')
    df["timestamp"] = df["timestamp"].dt.tz_localize('Africa/Nairobi')
    raw_df = df.set_index("timestamp")
    df = raw_df.resample(rule='H').mean()

    scaler = MinMaxScaler()
    df.reset_index(inplace=True)
    scaled_data = scaler.fit_transform(df.drop("timestamp", axis=1))

    x = scaled_data
    y = scaled_data[:, 0]
    y1 = scaled_data[:, 1]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=456, shuffle=False)
    x_train1, x_test1, y_train1, y_test1 = train_test_split(x, y1, test_size=0.2, random_state=456, shuffle=False)

    window_length = 6
    batch_size = 16
    test_generator = TimeseriesGenerator(x_test, y_test, length=window_length, sampling_rate=1,
                                         batch_size=batch_size)

    test_generator1 = TimeseriesGenerator(x_test1, y_test1, length=window_length, sampling_rate=1,
                                          batch_size=batch_size)

    # mq7_preds = model1.predict_generator(test_generator)
    # mq7_preds = mq7_preds.reshape(mq7_preds.shape[0], window_length)
    #
    # mq135_preds = model2.predict(test_generator1)
    # mq135_preds = mq135_preds.reshape(mq135_preds.shape[0], window_length)
    #
    # print(mq7_preds)


if __name__ == "__main__":
    main()
