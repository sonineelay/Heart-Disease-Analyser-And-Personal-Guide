from flask import Flask,render_template,jsonify,request
from dotenv import load_dotenv
import google.generativeai as genai
import numpy as np
import pickle
import os
import time


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html",activeNav="index")

@app.route("/heart-disease")
def heartDisease():
    return render_template("heart-diseases.html",activeNav="index",activeSide="heart-disease")

@app.route("/heart-disease/predict" ,methods=['POST'])
def heartDiseasePrediction():
    
    # Start the timer
    start_time = time.time()
    data = request.get_json()
    
    model_files = ['dt_model.pkl', 'rf_model.pkl', 'knn_model.pkl', 'svm_model.pkl']
    trained_model = pickle.load(open(model_files[data['algo_type']], 'rb'))
    
    # Extract features from JSON input
    features = [
    data['age'], data['sex'],
    data['cp'],
    data['trestbps'], data['chol'],
    data['fbs'], data['restecg'],
    data['thalach'], data['exang'], data['oldpeak'],
    data['slope'], data['ca'], data['thal']
    ]

    query = np.array(features, dtype=object).reshape(1, 13)

    # # Perform prediction
    checker = trained_model.predict(query)
    probability = trained_model.predict_proba(query)
    
    giveRecommendationsString = ''
    for feature in features:
        giveRecommendationsString += str(feature) + ","

    giveRecommendationsString += '1,' if checker else '0,'
    # Append remaining data using string formatting
    giveRecommendationsString += f"{data['smking']},{data['roh']},{data['dbts']},{data['family']}"

    # print(giveRecommendationsString)
    recommendationsList = giveRecommendations(giveRecommendationsString)
 
    end_time = time.time()

    elapsed_time = end_time - start_time
    
    # print(checker,probability[0][0] * 100,probability[0][1] * 100)
    
    result = {
        'hasDisease': bool(checker),
        'prediction': probability[0][int(bool(checker))] * 100,
        'timeTook': elapsed_time,
        'recommendations':recommendationsList
    }
    return jsonify(result)

def giveRecommendations(objList : str):

    load_dotenv()

    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

    prompt = "Act are a Personal guide and based on the provided data Age: {age} The patient's age in years.Sex: {sex} The patient's gender ({sex_description})Chest Pain (cp): {cp} Type of chest pain experienced (0: Typical angina, 1: Atypical angina, 2: Non-anginal pain, 3: Asymptomatic).Resting Blood Pressure (trestbps): {trestbps} Resting blood pressure in mm Hg.Cholesterol Levels (chol): {chol} Serum cholesterol in mg/dl.Fasting Blood Sugar (fbs): {fbs} Fasting blood sugar level (1 = above 120 mg/dl, 0 = otherwise).Resting ECG (restecg): {restecg} Resting electrocardiographic results (0: Normal, 1: ST-T wave abnormality, 2: Probable or definite left ventricular hypertrophy).Max Heart Rate (thalach): {thalach} Maximum heart rate achieved during a stress test.Exercise-Induced Angina (exang): {exang} Presence of exercise-induced angina (1 = yes, 0 = no).ST Depression (oldpeak): {oldpeak} ST depression induced by exercise relative to rest.Slope of Peak Exercise ST Segment (slope): {slope} Slope of the peak exercise ST segment (0: Upsloping, 1: Flat, 2: Downsloping).Major Vessels (ca): {ca} Number of major vessels (0-4) colored by fluoroscopy.Thelisemia (thal): {thal} Thelisemia (0: Normal, 1: Fixed defect, 2: Reversible defect, 3: Not described).Heart Disease Status (target): {target} Presence of heart disease (0 = no disease, 1 = presence of disease).Smoking (smking): {smking} Is Patient Smoking or not (0 = not smoking, 1 = smoking).Alcohol Consumption (roh): {roh} Is Consuming Alcohol (0 = not consuming alcohol, 1 = consuming alcohol).Diabetes (dbts): {dbts} Having Diabetes or Not (0 = not having, 1 = having).Family History of Heart Disease (family): {family} Having In Family Or Not (0 = not having, 1 = Having), this patient is a with several risk factors for heart disease.Here are five personalized recommendations for a healthier heart without any title or additional advice and just : **1. Title:**Content\n **2. Title:**Content\n **3. Title:**Content\n **4. Title:**Content **5. Title:**Content\n" + objList
    
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content(prompt)

    recommendation = response.text.split('\n\n')
    print(recommendation)
    return recommendation

def string_to_recommendations(input_string):
    # Split the input string by '\n\n' to separate each section
    sections = input_string.strip().split('\n\n')

    # Initialize an empty list to store recommendations
    recommendations = []

    # Loop through each section
    for section in sections:
        # Split each section by '\n' to get individual recommendations
        section_recommendations = section.split('\n    * ')

        # Remove the section heading
        section_recommendations[0] = section_recommendations[0].replace("**", "").strip()

        # Add each recommendation to the list
        recommendations.extend(section_recommendations)

    return recommendations

@app.route("/help")
def helpPage():
    return render_template("help-page.html",activeNav="index",activeSide="help")


if __name__ == "__main__":

    app.run(host="127.0.0.1",debug=True)