# __Author__: 'Brian Westerman'
# __Date__: 2/15/16
# __File__: analysis.py

import numpy as np
import scipy.stats as st
import scipy.cluster.vq as vq
import math
import random
import data as dt

# Takes in a list of column headers and the Data object and returns a list of 2-element lists with the minimum and
# maximum values for each column
def dataRange(colHeaders, data):

    ranges = []
    for col in colHeaders:
        ranges.append([np.min(data.get_column(col)), np.max(data.get_column(col))])
    return np.array(ranges)

# Takes in a list of column headers and the Data object and returns a list of the mean values for each column
def mean(colHeaders, data):

    return np.mean(data.get_data(colHeaders), axis=0)

# Takes in a list of column headers and the Data object and returns a list of the standard deviation for each column
def stdev(colHeaders, data):

    return np.std(data.get_data(colHeaders), axis=0)

# Takes in a list of column headers and the Data object and returns a matrix with each column normalized so its minimum
# value is mapped to zero and its maximum value is mapped to 1
def normalizeColumnsSeparately(colHeaders, data):

    matrix = data.get_data(colHeaders)
    mins = dataRange(colHeaders, data)[:, 0]
    maxes = dataRange(colHeaders, data)[:, 1]
    normalized = np.matrix(((matrix - mins) / (maxes - mins)))
    return normalized

# Takes in a list of column headers and the Data object and returns a matrix with each entry normalized so that the
# minimum value (of all the data in this set of columns) is mapped to zero and its maximum value is mapped to 1
def normalizeColumnsTogether(colHeaders, data):

    matrix = data.get_data(colHeaders)
    min = np.min(data.matrix_data)
    max = np.max(data.matrix_data)
    normalized = np.matrix(((matrix - min) / (max - min)))
    return normalized

# Takes in a list of column headers and the Data object and returns a list of the variance for each column
def variance(colHeaders, data):

    return np.var(data.get_data(colHeaders), axis=0)

# Takes in a list of column headers and the Data object and returns a list of the mean values for each column
def median(colHeaders, data):

    return np.median(data.get_data(colHeaders), axis=0)

# Takes in a list of column headers and the Data object and returns a list of the most common values for each column
def modeValue(colHeaders, data):

    return st.mode(data.get_data(colHeaders), axis=0)[0]

# Takes in a list of column headers and the Data object and returns a list of the highest frequencies for each column
def modeFreq(colHeaders, data):

    return st.mode(data.get_data(colHeaders), axis=0)[1]

# Takes in a list of column headers and the Data object and returns a list of the range (max - min) for each column
def rangeDiff(colHeaders, data):

    hilo = dataRange(colHeaders, data)
    result = []
    for i in np.arange(len(hilo)):
        result.append(hilo[i][1] - hilo[i][0])
    return result

# Runs linear regression for one or more independent variables
# Parameters: a list of headers for the independent variables, a single header for the dependent variable, and data
def linear_regression(d, ind, dep):

    y = d.get_column(dep)
    A = d.get_data(ind)
    A = np.hstack((A, np.ones((A.shape[0], 1))))

    # The matrix A.T * A is the covariance matrix of the independent
    # data, and we will use it for computing the standard error of the
    # linear regression fit below
    AAinv = np.linalg.inv(np.dot(A.T, A))

    # This solves the equation y = Ab, where A is a matrix of the
    # independent data, b is the set of unknowns as a column vector,
    # and y is the dependent column of data.  The return value x
    # contains the solution for b
    x = np.linalg.lstsq(A, y)

    # the solution that provides the best fit regression
    b = x[0]
    # the number of data points
    N = len(y)
    # the number of coefficients
    C = len(b)
    # This is the number of degrees of freedom of the error
    df_e = N - C
    # This is the number of degrees of freedom of the model fit
    # It means if you have C-1 of the values of b you can find the last one
    df_r = C - 1

    # the error of the model prediction
    error = y - np.dot(A, b)

    # the sum squared error
    sse = np.dot(error.T, error) / df_e

    # the standard error
    stderr = np.sqrt(np.diagonal(sse[0, 0] * AAinv))

    # the t-statistic
    t = b.T / stderr

    # the probability of the coefficient indicating a random relationship (slope = 0)
    p = (1 - st.t.cdf(abs(t), df_e))  # if p-value is double what it's supposed to be, take away 2 for one-tailed test

    # the r^2 coefficient indicating the quality of the fit
    r2 = 1 - error.var() / y.var()

    return b, sse[0, 0], r2, t, p

# Runs linear regression through solving the normal equation b = (A.T*A)^-1 * A.T*y
def linear_regression_ne(d, ind, dep):

    y = d.get_column(dep)
    A = d.get_data(ind)
    A = np.hstack((A, np.ones((A.shape[0], 1))))

    # The matrix A.T * A is the covariance matrix of the independent
    # data, and we will use it for computing the standard error of the
    # linear regression fit below
    AAinv = np.linalg.inv(np.dot(A.T, A))

    # This solves the normal equation b = (A.T*A)^-1 * A.T*y, where A is a matrix of the
    # independent data, b is the set of unknowns as a column vector,
    # and y is the dependent column of data
    b = np.linalg.inv(np.dot(A.T, A)) * np.dot(A.T, y)

    # the number of data points
    N = len(y)
    # the number of coefficients
    C = len(b)
    # This is the number of degrees of freedom of the error
    df_e = N - C
    # This is the number of degrees of freedom of the model fit
    # It means if you have C-1 of the values of b you can find the last one
    df_r = C - 1

    # the error of the model prediction
    error = y - np.dot(A, b)

    # the sum squared error
    sse = np.dot(error.T, error) / df_e

    # the standard error
    stderr = np.sqrt(np.diagonal(sse[0, 0] * AAinv))

    # the t-statistic
    t = b.T / stderr

    # the probability of the coefficient indicating a random relationship (slope = 0)
    p = 2 * (1 - st.t.cdf(abs(t), df_e))  # if p-value is double what it's supposed to be, take away 2 for one-tailed test

    # the r^2 coefficient indicating the quality of the fit
    r2 = 1 - error.var() / y.var()

    return b, sse[0, 0], r2, t, p

# Runs linear regression through gradient descent
def linear_regression_gd(d, ind, dep):

    # Calculate the regularized cost function:
    # J(theta) = 1/2*(sum(h - y)^2 + lambda*sum(theta^2))
    def calcCost(h, y, theta):
        m = y.shape[0]
        J = 1/2 * (np.sum(np.square(h - y)) + (regLambda * np.sum(np.dot(theta.T, theta))))
        return J

    # the dependent variable data
    y = d.get_column(dep)
    # the independent variable data
    A = d.get_data(ind)
    A = np.hstack((A, np.ones((A.shape[0], 1))))
    # The matrix A.T * A is the covariance matrix of the independent
    # data, and we will use it for computing the standard error of the
    # linear regression fit below
    AAinv = np.linalg.inv(np.dot(A.T, A))
    # the number of independent variables
    j1 = A.shape[1]
    # the number of data points
    m = A.shape[0]
    # the point at which gradient descent is halted
    targetCost = 50
    # the learning rate
    alpha = 0.005
    # the regularization coefficient
    regLambda = 0.1
    # helps us initialize the weights to useful values between -epsilon and epsilon
    epsilon = 0.13

    # randomly initialize weights for each independent variable and a bias term (y-intercept)
    theta = np.random.rand(1, j1) * (2*epsilon) - epsilon

    # train the model by updating the weights through gradient descent
    # while (cost >= targetCost):
    for j in range(5000):
        # initialize a matrix to store the predictions
        h = np.zeros((m, 1))
        # initialize a count to accumulate adjustments to the weights
        delta = np.zeros((1, A.shape[1]))
        # determine delta matrix for each layer
        for i in range(m):
            # predict value
            z = A[i, :] * theta.T
            error = z - y[i]
            h[i, :] = z
            # calculate adjustments for weights for this iteration
            adjustments = np.dot(error, A[i, :])
            # accumulate adjustments
            delta += adjustments
        # adjust weights using regularization
        adjustBias = alpha * (delta[:, -1] / m)
        adjustWeights = alpha * (delta[:, :-1] / m + ((regLambda/m) * theta[:, :-1]))
        theta[:, -1] -= adjustBias
        theta[:, :-1] -= adjustWeights
        cost = calcCost(h, y, theta)
        print("cost: ", cost)

    # the solution that provides the best fit regression
    b = theta.T
    # the number of data points
    N = len(y)
    # the number of coefficients
    C = len(b)
    # This is the number of degrees of freedom of the error
    df_e = N - C
    # This is the number of degrees of freedom of the model fit
    # It means if you have C-1 of the values of b you can find the last one
    df_r = C - 1

    # the error of the model prediction
    error = y - np.dot(A, b)

    # the sum squared error
    sse = np.dot(error.T, error) / df_e

    # the standard error
    stderr = np.sqrt(np.diagonal(sse[0, 0] * AAinv))

    # the t-statistic
    t = b.T / stderr

    # the probability of the coefficient indicating a random relationship (slope = 0)
    p = 2 * (1 - st.t.cdf(abs(t), df_e))  # if p-value is double what it's supposed to be, take away 2 for one-tailed test

    # the r^2 coefficient indicating the quality of the fit
    r2 = 1 - error.var() / y.var()

    return b, sse[0, 0], r2, t, p

# Runs linear regression through a three-layer perceptron trained by gradient descent
def linear_regression_nn(d, ind, dep):

    # Tanh function to get "activations" in [-1, 1] for nodes in the hidden layer:
    # g(z) = 2/(1+e^(-2z)) - 1
    # flattening function that returns a value from -1 to 1
    def tanh(z):
        return 2/(1 + np.exp(-2*z)) - 1

    # Derivative of tanh function to compute the gradient for nodes in the hidden layer:
    # g'(z) = tanh(z)*(1-tanh(z))
    def dtanh(z):
        return np.multiply(tanh(z), (1 - tanh(z)))

    # Calculate error term of hidden layer:
    # error2 = (theta2.T*error3) .* g'(z2)
    def calcErrorTerm(theta, error, z):
        return np.multiply(np.dot(theta[:, :-1].T, error), dtanh(z))

    # Calculate the regularized cost function:
    # J(theta) = (1/2)*(sum(h - y)^2 + lambda*(sum(theta1^2)+sum(theta2^2))
    def calcCost(h, y, theta1, theta2):
        m = y.shape[0]
        J = 1/2 * (np.sum(np.square(h - y)) +
                   (regLambda * (np.sum(np.dot(theta1.T, theta1)) + np.sum(np.dot(theta2.T, theta2)))))
        return J

    # the dependent variable data
    y = d.get_column(dep)
    # the independent variable data
    A = d.get_data(ind)
    A = np.hstack((A, np.ones((A.shape[0], 1))))
    # The matrix A.T * A is the covariance matrix of the independent
    # data, and we will use it for computing the standard error of the
    # linear regression fit below
    AAinv = np.linalg.inv(np.dot(A.T, A))
    # the number of independent variables
    j1 = A.shape[1]
    # the number of nodes in the hidden layer (two larger than the input layer)
    j2 = A.shape[1] + 2
    # the number of nodes in the output layer (only 1 for linear regression)
    j3 = 1
    # the number of data points
    m = A.shape[0]
    # the point at which gradient descent is halted
    targetCost = 50
    # the learning rate
    alpha = 0.01
    # the regularization coefficient
    regLambda = 0.001
    # helps us initialize the weights to useful values between -epsilon and epsilon
    epsilon = 0.13

    # randomly initialize weights for each independent variable and a bias term (y-intercept)
    theta1 = np.random.rand(j2-1, j1) * (2*epsilon) - epsilon
    theta2 = np.random.rand(j3, j2) * (2*epsilon) - epsilon

    # train the model by updating the weights through gradient descent
    # while (cost >= targetCost):
    for j in range(10000):
        # initialize a matrix to store the predictions
        h = np.zeros((m, 1))
        # initialize a count to accumulate adjustments to the weights
        delta1 = np.zeros((j2-1, j1))
        delta2 = np.zeros((j3, j2))
        # determine delta matrices for each layer
        for i in range(m):
            # Forward propagation
            a1 = A[i].T  # bias term already at the end
            z2 = np.dot(theta1, a1)
            a2 = np.vstack((tanh(z2), np.ones((1, 1))))  # bias term added to the end
            z3 = np.dot(theta2, a2)
            h[i, :] = z3
            # Backpropagation
            actual = y[i].T
            error3 = z3 - actual
            error2 = calcErrorTerm(theta2, error3, z2)
            # Calculate adjustments for weights for this iteration
            adjustments1 = np.dot(error2, a1.T)
            adjustments2 = np.dot(error3, a2.T)
            # Accumulate adjustments
            delta1 += adjustments1
            delta2 += adjustments2
        # adjust weights using regularization
        adjustBias = alpha * (delta1[:, -1] / m)
        adjustWeights = alpha * (delta1[:, :-1] / m + ((regLambda/m) * theta1[:, :-1]))
        theta1[:, -1] -= adjustBias
        theta1[:,:-1] -= adjustWeights
        adjustBias = alpha * (delta2[:, -1] / m)
        adjustWeights = alpha * (delta2[:, :-1] / m + ((regLambda/m) * theta2[:, :-1]))
        theta2[:, -1] -= adjustBias
        theta2[:,:-1] -= adjustWeights
        cost = calcCost(h, y, theta1, theta2)
        print("cost: ", cost)

    # the solution that provides the best fit regression, averaging weights from each independent variable
    # to its connected nodes in the hidden layer
    b = np.matrix(np.average(theta1, axis=0)).T
    # the number of data points
    N = len(y)
    # the number of coefficients
    C = len(b)
    # This is the number of degrees of freedom of the error
    df_e = N - C
    # This is the number of degrees of freedom of the model fit
    # It means if you have C-1 of the values of b you can find the last one
    df_r = C - 1

    # the error of the model prediction
    error = y - np.dot(A, b)
    print(y)
    print(np.dot(A, b))
    print(error)

    # the sum squared error
    sse = np.dot(error.T, error) / df_e

    # the standard error
    stderr = np.sqrt(np.diagonal(sse[0, 0] * AAinv))

    # the t-statistic
    t = b.T / stderr

    # the probability of the coefficient indicating a random relationship (slope = 0)
    p = 2 * (1 - st.t.cdf(abs(t), df_e))  # if p-value is double what it's supposed to be, take away 2 for one-tailed test

    # the r^2 coefficient indicating the quality of the fit
    r2 = 1 - error.var() / y.var()

    return b, sse[0, 0], r2, t, p

# A test function that reads in a data set and does a multiple linear regression fit
def testRegression(data):

    headers = list(data.get_headers())
    dep = [header for header in headers if header == 'Y'][0]
    ind = [header for header in headers if header != 'Y']

    b, sse, r2, t, p = linear_regression(data, ind, dep)

    print("\nCoefficients: ", b)
    print("Sum squared error: ", sse)
    print("R-squared: ", r2)
    print("t-statistic: ", t)
    print("p-value: ", p)

    # testRegression called in data.py

# Calculates Principal Components Analysis on the passed-in Data object using Singular Value Decomposition
def pca(data, headers, norm=True):

    if norm:
        A = normalizeColumnsSeparately(headers, data)
    else:
        A = data.get_data(headers)
    m = np.mean(A, axis=0)
    D = A - m
    U, S, V = np.linalg.svd(D, full_matrices=False)
    evals = np.matrix(np.square(S) / (A.shape[0]-1))
    evecs = V
    projectedData = D * V.T

    pcadata = dt.PCAData(projectedData, evecs, evals, m, list(headers))

    return pcadata

def kmeans_numpy(data, headers, K, whiten=True):
    '''Takes in a Data object, a set of headers, and the number of clusters to create
    Computes and returns the codebook, codes, and representation error.
    '''

    A = data.get_data(headers)
    W = vq.whiten(A)
    codebook, bookerror = vq.kmeans2(W, K)
    codes, error = vq.vq(W, codebook)

    return codebook, codes, error

def kmeans_init(dataMatrix, K, categories=''):

    if categories == '':
        # Return K random data points from data
        return dataMatrix[random.sample(range(dataMatrix.shape[0]), K), :]
    else:
        # Given an Nx1 matrix of labels, compute the mean values of each category and return those as the initial set of means
        means = np.zeros((K, dataMatrix.shape[1]))
        for i in range(K):
            # Grab the data that matches the ith category
            indicesOfInterest = np.array(categories[:, 0] == i)
            rowsOfInterest = np.array(categories[:, 0] == i)
            for j in range(dataMatrix.shape[1]-1):
                rowsOfInterest = np.hstack((rowsOfInterest, indicesOfInterest))
            dataOfInterest = dataMatrix[rowsOfInterest == True]
            # Compute feature-wise means and add to the matrix of K means
            means[i, :] = np.mean(dataOfInterest, axis=0)
        return means

def kmeans_classify(dataMatrix, means):

    K = means.shape[0]
    N = dataMatrix.shape[0]
    codes = np.zeros((N, 1))
    errors = np.zeros((N, 1))
    # Loop through N data points, each time computing errors (distances) for K clusters and classifying the point
    for i in range(N):
        winner = 65535  # a large number
        codes[i, 0] = 0
        for j in range(K):
            ssd = np.sqrt(np.sum(np.square(dataMatrix[i] - means[j])))
            if ssd < winner:
                errors[i, 0] = ssd
                winner = ssd
                codes[i, 0] = j

    return codes, errors

def kmeans_algorithm(A, means):

    # set up some useful constants
    MIN_CHANGE = 1e-7
    MAX_ITERATIONS = 100
    D = means.shape[1]
    K = means.shape[0]
    N = A.shape[0]

    # iterate no more than MAX_ITERATIONS
    for i in range(MAX_ITERATIONS):
        # calculate the codes
        codes, errors = kmeans_classify(A, means)

        # calculate the new means
        newmeans = np.zeros_like(means)
        counts = np.zeros((K, 1))
        for j in range(N):
            newmeans[codes[j, 0], :] += A[j,:]
            counts[codes[j, 0], 0] += 1.0

        # finish calculating the means, taking into account possible zero counts
        for j in range(K):
            if counts[j,0] > 0.0:
                newmeans[j, :] /= counts[j, 0]
            else:
                newmeans[j, :] = A[random.randint(0, A.shape[0]), :]

        # test if the change is small enough
        diff = np.sum(np.square(means - newmeans))
        means = newmeans
        if diff < MIN_CHANGE:
            break

    # call classify with the final means
    codes, errors = kmeans_classify(A, means)

    # return the means, codes, and errors
    return means, codes, errors

def kmeans(data, headers, K, whiten=True, categories=''):
    '''Takes in a Data object, a set of headers, and the number of clusters to create
    Computes and returns the codebook, codes and representation errors.
    If given an Nx1 matrix of categories, it uses the category labels
    to calculate the initial cluster means.
    '''

    A = data.get_data(headers)
    if whiten:
        W = vq.whiten(A)
    else:
        W = A
    codebook = kmeans_init(W, K, categories)
    codebook, codes, errors = kmeans_algorithm(W, codebook)

    return codebook, codes, errors