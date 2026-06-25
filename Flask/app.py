from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)

model_path = os.path.join(os.path.dirname(__file__), "HDI.pkl")
model = pickle.load(open(model_path, "rb"))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Prediction')
def prediction():
    return render_template('indexnew.html')

@app.route('/Home')
def my_home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():

    country = float(request.form['Country'])
    expected_schooling = float(request.form['Expected_Years_Schooling'])
    mean_schooling = float(request.form['Mean_Years_Schooling'])
    gni = float(request.form['GNI_Per_Capita'])

    features = [[
        country,
        expected_schooling,
        mean_schooling,
        gni
    ]]

    prediction = model.predict(features)

    y_pred = round(float(prediction[0]), 3)

    if y_pred < 0.55:
        category = "Low HDI"
    elif y_pred < 0.70:
        category = "Medium HDI"
    elif y_pred < 0.80:
        category = "High HDI"
    else:
        category = "Very High HDI"

    result = f"{category} : {y_pred}"

    return render_template(
        'resultnew.html',
        prediction_text=result
    )

if __name__ == "__main__":
    app.run()