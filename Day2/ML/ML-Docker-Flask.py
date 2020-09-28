'''
we have two label encoders, one one-hot encoder, one scaler and one logistic regression model

'''


# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import metrics

from sklearn.linear_model import LogisticRegression

# For saving ML models
import pickle

# ---------------

# Step 1 - Preprocessing!

# Importing the dataset
dataset = pd.read_csv('Churn_Modelling.csv')

X = dataset.iloc[:, 3:13].values
y = dataset.iloc[:, 13].values

# Encode labels and save to pickle file
labelEncoder = LabelEncoder()
X[:, 1] = labelEncoder.fit_transform(X[:, 1])
filename = 'labelEncoder1.pickle'
pickle.dump(labelEncoder, open(filename, 'wb'))

labelEncoder = LabelEncoder()
X[:, 2] = labelEncoder.fit_transform(X[:, 2])
filename = 'labelEncoder2.pickle'
pickle.dump(labelEncoder, open(filename, 'wb'))

onehotencoder = OneHotEncoder()
X = onehotencoder.fit_transform(X).toarray()
X = X[:, 1:]
filename = 'onehotencoder.pickle'
pickle.dump(onehotencoder, open(filename, 'wb'))

# Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Scale our data and save too pickle file
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

filename = 'standardScaler.pickle'
pickle.dump(sc, open(filename, 'wb'))

# ---------------

# Step 2 - Define Model
log_reg = LogisticRegression(solver='lbfgs')
log_reg.fit(X_train, y_train)

# Save to pickle file
filename = 'log_reg_model.pickle'
pickle.dump(log_reg, open(filename, 'wb'))

# ---------------

# Step 3 - Evaluate the model
y_pred = log_reg.predict(X_test)

print(f'confusion matrix: \n{metrics.confusion_matrix(y_pred, y_test)}')
print(f'accuracy: {metrics.accuracy_score(y_pred, y_test)}')
print(f'recall: {metrics.recall_score(y_pred, y_test)}')

# ---------------

# Test to see if we can load the model and predict again
filename = 'log_reg_model.pickle'
model = pickle.load(open(filename, 'rb'))

y_pred = model.predict(X_test)
metrics.accuracy_score(y_pred, y_test)
