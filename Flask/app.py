from flask import Flask, render_template, request
import pickle
import os

# Initialize the Flask application
app = Flask(__name__)

# Load the trained Linear Regression model
model_path = os.path.join(os.path.dirname(__file__), "HDI.pkl")
model = pickle.load(open(model_path, "rb"))


# Home page
@app.route('/')
def home():
    return render_template('home.html')


# Prediction input page
@app.route('/Prediction')
def prediction():
    return render_template('indexnew.html')


# Navigate back to the home page
@app.route('/Home')
def my_home():
    return render_template('home.html')


# Predict Human Development Index (HDI)
@app.route('/predict', methods=['POST'])
def predict():

    # Get user inputs from the prediction form
    country = float(request.form['Country'])
    expected_schooling = float(request.form['Expected_Years_Schooling'])
    mean_schooling = float(request.form['Mean_Years_Schooling'])
    gni = float(request.form['GNI_Per_Capita'])

    # Prepare input features for the trained model
    features = [[
        country,
        expected_schooling,
        mean_schooling,
        gni
    ]]

    # Predict the Human Development Index
    prediction = model.predict(features)

    # Round the predicted HDI value
    y_pred = round(float(prediction[0]), 3)

    # Categorize the predicted HDI
    if y_pred < 0.55:
        category = "Low HDI"
    elif y_pred < 0.70:
        category = "Medium HDI"
    elif y_pred < 0.80:
        category = "High HDI"
    else:
        category = "Very High HDI"

    # Prepare the result to display on the output page
    result = f"{category} : {y_pred}"

    # Display the prediction result
    return render_template(
        'resultnew.html',
        prediction_text=result
    )


# Run the Flask application
if __name__ == "__main__":
    app.run()