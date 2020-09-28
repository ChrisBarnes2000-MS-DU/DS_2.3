# Make a flask API for our ML Model

# Import the WSGI application library
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

# Import FLASK
from flask import Flask, request, jsonify

# Import RESTPLUS libraries
from flask_restplus import Api, Resource, fields

# Import DS libraries
import pickle
import numpy as np

import boto3

# Define app and api object
app = Flask(__name__)
api = Api(app, version='1.0', title='Logistic Regression',
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
    """Applies pre-trained Logistic Regression model to input data"""
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

        # Apply label encoders to categorical data
        X[1] = int(labelEncoder1.transform([X[1]]))
        X[2] = int(labelEncoder2.transform([X[2]]))

        # Scale the data using our standardScaler
        X = standardScaler.transform([X])

        # Make the prediction
        prediction = model.predict(X)

        # Return prediction
        return {'prediction': str(prediction)}


if __name__ == '__main__':
    # ssm = boto3.client('ssm', region_name='us-east-1')
    # response = ssm.get_parameters(Names=['API_KEY'],
    #                               WithDecryption=True)
    # api_key = response['Parameters'][0]['Value']
    # my_nasa_apod_url = my_nasa_apod_url.format(my_api_key=nasa_api_key)

    app.run(host='0.0.0.0', port=8000)