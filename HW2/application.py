# Make a flask API for our ML Model
# Import the WSGI applicationlication library
import pyrebase
from datetime import datetime
import numpy as np
import pickle
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restplus import Api, Resource, fields
from flask import Flask, request, jsonify

config = {
  "apiKey": "AIzaSyAf_ekbHs_4aRjP4neDhOplI4DKlOMnOGo",
  "authDomain": "ds-hw2-cb.firebaseapp.com",
  "databaseURL": "https://ds-hw2-cb.firebaseio.com",
  "projectId": "ds-hw2-cb",
  "storageBucket": "ds-hw2-cb.appspot.com",
  "messagingSenderId": "766659253302",
  "appId": "1:766659253302:web:6eb51ffff0191a5ab1f497",
  "measurementId": "G-CYJXKCXTT5"
}

firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
auth = firebase.auth()

email = "chris.barnes.2000@me.com"
password = "chris1217"

# user = auth.create_user_with_email_and_password(email, password)

# Log the user in
user = auth.sign_in_with_email_and_password(email, password)
# before the 1 hour expiry:
user = auth.refresh(user['refreshToken'])
# now we have a fresh token
user['idToken']


# Get a reference to the database service
db = firebase.database()


# ---------------------------


# Define application and api object
application = Flask(__name__)
api = Api(application, version='1.0', title='Logistic Regression',
          description='Logistic Regression')
ns = api.namespace('DS2_3_docker_and_aws', description='Methods')

# Define arguments for our API, in this case, it is going to be just a comma separated string
single_parser = api.parser()
single_parser.add_argument('input', type=str, required=True, help='input CSV')

# Load objects from pickle files
labelEncoder1 = pickle.load(open('pickle_files/labelEncoder1.pickle', 'rb'))
labelEncoder2 = pickle.load(open('pickle_files/labelEncoder2.pickle', 'rb'))
standardScaler = pickle.load(open('pickle_files/standardScaler.pickle', 'rb'))
onehotencoder = pickle.load(open('pickle_files/onehotencoder.pickle', 'rb'))
model = pickle.load(open('pickle_files/log_reg_model.pickle', 'rb'))


@ns.route('/prediction')
class LogRegPrediction(Resource):
    """Applicationlies pre-trained Logistic Regression model to input data"""
    @api.doc(parser=single_parser, description='Upload input data')
    def post(self):
        # Parse arguments
        args = single_parser.parse_args()

        # Get input data in string format
        input_data = args.input

        # Convert data to numpy array
        dataset = np.array(input_data.split(','))

        # Get only the data that we need
        X = dataset[3:]

        # Applicationly label encoders to categorical data
        X[1] = int(labelEncoder1.transform([X[1]]))
        X[2] = int(labelEncoder2.transform([X[2]]))

        # Scale the data using our standardScaler
        X = standardScaler.transform([X])

        # Make the prediction
        prediction = model.predict(X)
        # print(prediction[0])



        # data to save
        data = {
            "name": "ML Prediction",
            "prediction": str(prediction),
            "date": str(datetime.now()),
        }

        # Pass the user's idToken to the push method
        results = db.child("users").push(data, user['idToken'])

        # Return prediction
        return {'prediction': str(prediction)}


if __name__ == '__main__':
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production application.
    # application.debug = True
    application.run()
