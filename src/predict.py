import joblib

def predict_new(input_data):
    model = joblib.load("diabetes_model.pkl")
    prediction = model.predict([input_data])
    return prediction[0]
