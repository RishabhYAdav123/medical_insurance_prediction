# importing the necessary dependencies
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin 
import pickle
import numpy as np

app = Flask(__name__)  # initializing the Flask app

@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])  # route to show the predictions in a web UI
def predict():
    if request.method == 'POST':
        try:
            # Reading the inputs given by the user
            age = float(request.form['age'])
            sex = request.form['sex'].lower()  # Convert to lowercase for uniformity
            bmi = float(request.form['bmi'])
            smoker = request.form['smoker'].lower()  # Convert to lowercase
            children = int(request.form['children'])
            region = request.form['region'].lower()  # Convert to lowercase

            # Convert categorical variables to numeric values
            if sex == 'male':
                sex = 1
            else:
                sex = 0
            
            if smoker == 'yes':
                smoker = 1
            else:
                smoker = 0

            # Region encoding (map to numeric values based on your dataset)
            region_mapping = {
                'southwest': 0,
                'southeast': 1,
                'northwest': 2,
                'northeast': 3
            }
            region = region_mapping.get(region, -1)  # Default to -1 if region is invalid

            # Load the model and make predictions
            filename = 'model.pkl'  # path to your saved model
            loaded_model = pickle.load(open(filename, 'rb'))  # loading the model from storage
            
            # Preparing the input features in the same order as the training data
            input_features = np.array([[age, sex, bmi, children, smoker, region]])
            
            # Make the prediction
            prediction = loaded_model.predict(input_features)
            
            # Showing the prediction results in a UI
            return render_template('index.html', result=f"${round(prediction[0], 2)}")

        except Exception as e:
            print('The Exception message is:', e)
            return render_template('index.html', result="Error: Something went wrong, please try again.")

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)  # running the app
