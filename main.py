from data.data_loader import load_data
from data.preprocess import preprocess
from model.RandomForest.model import build_model
from model.LogisticRegression.model import build_model as build_logistic_model
from model.SVM.model import build_model as build_svm_model
from src.train import train_model
from src.evaluate import evaluate
from src.predict import predict_new

def main():
    df = load_data("data/diabetes.csv")
    
    X_train, X_test, y_train, y_test, scaler = preprocess(df)
   
    model = build_model()

    model1 = build_logistic_model()              
    train_model(model, X_train, y_train,scaler)        
     
    evaluate(model, X_test, y_test)             
    print("\nEvaluating Logistic Regression Model:\n")
    train_model(model1, X_train, y_train,scaler)
    evaluate(model1, X_test, y_test)
    # Example prediction
    print("\nEvaluating Support Vector Machine Model:")
    model2=build_svm_model()
    train_model(model2, X_train, y_train,scaler)
    evaluate(model2, X_test, y_test)
    sample = scaler.transform([[5,116,74,0,0,25.6,0.201,30]])
    result = predict_new(sample[0])
    print("\nSample Input Prediction:", "Diabetic" if result == 1 else "Healthy")

if __name__ == "__main__":
    main()
