from sklearn.svm import SVC

def build_model():
    model = SVC(kernel='linear', C=1.0, random_state=42)
    return model