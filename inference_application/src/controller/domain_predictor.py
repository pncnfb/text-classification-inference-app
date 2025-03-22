import joblib

class DomainPredictor:
    def __init__(self, model_path: str, vectorizer_path: str):
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)

    def predict(self, text: str) -> str:
        text_transformed = self.vectorizer.transform([text])
        prediction = self.model.predict(text_transformed)
        return prediction[0]