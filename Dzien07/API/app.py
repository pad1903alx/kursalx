
# Przykład usługi API we Flasku
from flask import Flask, request
import joblib
import numpy as np
import sklearn

# inicjalizacja Flaska
app = Flask("KNN")

# wczytywanie modelu z pliku
model = joblib.load("knn.model")

# http://127.0.0.1:1234/predict?sl=5.6&sw=3.2&pl=5.2&pw=1.45
@app.route("/predict")
def predict():
    try:
        sl = float(request.args.get("sl"))
        sw = float(request.args.get("sw"))
        pl = float(request.args.get("pl"))
        pw = float(request.args.get("pw"))
        if sl<=0 or sw<=0 or pl<=0 or pw<=0:
            raise Exception("Gdzieś kolego jest <= 0")
        result = model.predict( [ np.array([sl, sw, pl, pw]) ] )[0]
        iris = ["setosa", "versicolor", "virginica"]
        return iris[result]
    except Exception as exc:
        return str(exc)


@app.route("/")
def hello():
    return "<h1>Hello world!</h1>"

app.run(debug=True, port=1234)



