import pandas as pd
import matplotlib.pyplot as plt


import pickle


def load_model(filepath):
    """
    Loads pickled model
    """
    with open(filepath, 'rb') as file:
        model = pickle.load(file)
    return model


def predict(model, start_date, end_date):
    """
    makes predictions
    """
    pred = model.get_prediction(start=pd.to_datetime(start_date).tz_localize('Africa/Nairobi'),
                                end=pd.to_datetime(end_date).tz_localize('Africa/Nairobi'),
                                dynamic=False)
    pred_ci = pred.conf_int()
    return pred_ci


def make_prediction(start="2022-01-01", end="2022-01-05"):
    """
    main function
    """
    model1_path = "models/model1.pkl"
    model2_path = "models/model2.pkl"
    model1 = load_model(model1_path)
    model2 = load_model(model2_path)
    result1 = predict(model1, start, end)
    result2 = predict(model2, start, end)
    return result1, result2


if __name__ == "__main__":
    make_prediction()
