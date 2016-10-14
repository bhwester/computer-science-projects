# Author: Brian Westerman
# Date: 4/28/2016
# CS251 Final Project

import numpy as np
import pandas as pd
import sklearn.linear_model as sklearnLinearModel
import sklearn.svm as sklearnSVM
import matplotlib.pyplot as plt

# Read in data
fundedCompanies = pd.read_excel("/Users/Brian/Downloads/cb_data_xlsx_sample.xlsx", \
        sheetname="Funded Companies")
rounds = pd.read_excel("/Users/Brian/Downloads/cb_data_xlsx_sample.xlsx", \
        sheetname="Rounds")

# Keep only the features of interest
fundedCompaniesVars = fundedCompanies[['funding_rounds', 'funding_total_usd']]
roundsVars = rounds[['funding_round_type', 'raised_amount_usd', 'investor_count']]

# Clean up the data a bit
fundedCompaniesVars = fundedCompaniesVars.dropna(axis=0)  # get rid of any rows with NaN
roundsVars = roundsVars.dropna(axis=0)

# Initialize the machine learning models
linearModel = sklearnLinearModel.LinearRegression()
classifierSVM = sklearnSVM.SVC()


# Fit the models to the data

inputRegression = np.matrix(fundedCompaniesVars['funding_rounds']).T
outputRegression = np.matrix(fundedCompaniesVars['funding_total_usd']).T
linearModel.fit(inputRegression, outputRegression)

inputClassification = np.matrix(roundsVars[['investor_count', 'raised_amount_usd']])
outputClassification = np.array(roundsVars['funding_round_type'])
classifierSVM.fit(inputClassification, outputClassification)


# Evaluate performance of supervised learning models
predictionsRegression = linearModel.predict(inputRegression)
predictionsClassification = classifierSVM.predict(inputClassification)
r2 = linearModel.score(np.matrix(fundedCompaniesVars['funding_rounds']).T, np.matrix(fundedCompaniesVars['funding_total_usd']).T)
accuracy = classifierSVM.score(np.matrix(roundsVars[['investor_count', 'raised_amount_usd']]), np.array(roundsVars['funding_round_type']))
print("R^2 of regression: ", r2)
print("Accuracy of classifier: ", accuracy)


# Plot the models

plt.figure(1)  # makes a new figure
plt.title('Linear Regression of Total Funding vs. Funding Rounds')
plt.xlabel('Funding rounds')
plt.ylabel('Total funding in hundreds of millions of dollars')
plt.axis([0, 10, 0, 100000000])
plt.scatter(inputRegression, outputRegression)
m = linearModel.coef_
b = linearModel.intercept_
plt.plot(inputRegression, inputRegression*m+b, color='red')

plt.figure(2)  # makes a new figure
plt.title('Support Vector Machine Classification of Funding Round Type from Amount Raised and Investor Count')
plt.xlabel('Number of investors')
plt.ylabel('Amount raised in hundreds of millions of dollars')
plt.axis([0, 14, 0, 250000000])
classes = {0:'venture', 1:'seed', 2:'angel', 3:'private_equity'}
colors = {'venture':'red', 'seed':'green', 'angel':'blue', 'private_equity':'yellow'}
for i in range(4):
	label = predictionsClassification == classes[i]
	color = colors[classes[i]]
	plt.scatter(inputClassification[label, 0], inputClassification[label, 1], color=color)

# Display the plots
plt.show()
