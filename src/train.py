import joblib

def train_model(model, X_train, y_train, scaler):
    model.fit(X_train, y_train)
    joblib.dump(model, "diabetes_model.pkl")
    joblib.dump(scaler, "scaler.pkl")
    print("Model saved as diabetes_model.pkl")
