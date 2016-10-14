# Template by Bruce Maxwell
# Spring 2015
# CS 251 Project 8
#
# Classifier class and child definitions

import sys
import data
import analysis as an
import numpy as np
import scipy.cluster.vq as vq
import sklearn.metrics as cm


class Classifier:

    def __init__(self, type):
        '''The parent Classifier class stores only a single field: the type of
        the classifier.  A string makes the most sense.

        '''
        self._type = type

    def type(self, newtype=None):
        '''Set or get the type with this function'''
        if newtype != None:
            self._type = newtype
        return self._type

    def confusion_matrix(self, truecats, classcats):
        '''Takes in two Nx1 matrices of zero-index numeric categories and
        computes the confusion matrix. The rows represent true
        categories, and the columns represent the classifier output.

        '''

        counts = cm.confusion_matrix(truecats, classcats)

        # numCats = len(np.unique(truecats))
        # cmtx = np.empty((3, 3))
        # counts = np.empty((numCats+1, numCats+1))
        # for i in range(numCats):
        #     for j in range(numCats):
        #         counts[i, j] =
        # accuracy = len([x for x in truecats == classcats])
        # cmtx[0, 0] =
        # cmtx[0, 1] =
        # cmtx[1, 0] =
        # cmtx[1, 1] =

        return counts

    def confusion_matrix_str(self, cmtx):
        '''Takes in a confusion matrix and returns a string suitable for printing.'''
        s = '\n\nConfusion matrix:\n\n'
        for i in range(cmtx.shape[0]):
            s += str(cmtx[i, :]) + '\n'

        return s

    def __str__(self):
        '''Converts a classifier object to a string.  Prints out the type.'''
        return str(self._type)


class NaiveBayes(Classifier):
    '''NaiveBayes implements a simple NaiveBayes classifier using a
    Gaussian distribution as the pdf.

    '''

    def __init__(self, dataObj=None, headers=[], categories=None):
        '''Takes in a Data object with N points, a set of F headers, and a
        matrix of categories, one category label for each data point.'''

        # call the parent init with the type
        Classifier.__init__(self, 'Naive Bayes Classifier')

        # store the headers used for classification
        self.headers = headers
        # number of classes and number of features
        # original class labels
        # unique data for the Naive Bayes: means, variances, scales
        # if given data,
        if dataObj != None:
            # call the build function
            self.build(dataObj.get_data(headers), categories)

    def build(self, A, categories):
        '''Builds the classifier given the data points in A and the categories'''

        # figure out how many categories there are and get the mapping (np.unique)
        unique, mapping = np.unique(np.array(categories.T), return_inverse=True)
        self.num_classes = len(unique)
        self.num_features = A.shape[1]
        self.class_labels = np.matrix(mapping).T
        # create the matrices for the means, vars, and scales
        # the output matrices will be categories (C) x features (F)
        self.class_means = np.zeros((self.num_classes, self.num_features))
        self.class_vars = np.zeros((self.num_classes, self.num_features))
        self.class_scales = np.zeros((self.num_classes, self.num_features))
        # compute the means/vars/scales for each class
        for i in range(self.num_classes):
            data = A[(mapping == i), :]
            self.class_means[i, :] = np.mean(data, axis=0)
            self.class_vars[i, :] = np.var(data, axis=0)
            self.class_scales[i, :] = 1/np.sqrt(2*np.pi*np.var(data, axis=0))
        # store any other necessary information: # of classes, # of features, original labels

        return

    def classify(self, A, return_likelihoods=False):
        '''Classify each row of A into one category. Return a matrix of
        category IDs in the range [0..C-1], and an array of class
        labels using the original label values. If return_likelihoods
        is True, it also returns the NxC likelihood matrix.

        '''

        # error check to see if A has the same number of columns as
        # the class means
        assert A.shape[1] == self.class_means.shape[1]

        # make a matrix that is N x C to store the probability of each
        # class for each data point
        P = np.matrix(np.zeros((A.shape[0], self.num_classes))) # a matrix of zeros that is N (rows of A) x C (number of classes)

        # calculate the probabilities by looping over the classes
        # with numpy-fu you can do this in one line inside a for loop
        for i in np.arange(P.shape[1]):
            P[:, i] = np.multiply(self.class_scales[i, :], np.exp(-np.square(A-self.class_means[i, :])/(2*self.class_vars[i, :]))).prod(axis=1)

        # calculate the most likely class for each data point
        cats = np.argmax(P, axis=1) # take the argmax of P along axis 1
        print("Cats:")
        print(cats)

        # use the class ID as a lookup to generate the original labels
        # FIXME: labels: get lookup to work
        print("Class labels:")
        print(self.class_labels)
        # labels = self.class_labels[cats] isn't working
        labels = self.class_labels[cats[:, 0], 0]
        print("Labels:")
        print(labels)

        if return_likelihoods:
            return cats, labels, P

        return cats, labels

    def __str__(self):
        '''Make a pretty string that prints out the classifier information.'''
        s = "\nNaive Bayes Classifier\n"
        for i in range(self.num_classes):
            s += 'Class %d --------------------\n' % (i)
            s += 'Mean  : ' + str(self.class_means[i,:]) + "\n"
            s += 'Var   : ' + str(self.class_vars[i,:]) + "\n"
            s += 'Scales: ' + str(self.class_scales[i,:]) + "\n"

        s += "\n"
        return s
        
    def write(self, filename):
        '''Writes the Bayes classifier to a file.'''
        # extension
        return

    def read(self, filename):
        '''Reads in the Bayes classifier from the file'''
        # extension
        return

    
class KNN(Classifier):

    def __init__(self, dataObj=None, headers=[], categories=None, K=None):
        '''Take in a Data object with N points, a set of F headers, and a
        matrix of categories, with one category label for each data point.'''

        # call the parent init with the type
        Classifier.__init__(self, 'KNN Classifier')

        # store the headers used for classification
        self.headers = headers
        # number of classes and number of features
        # original class labels
        # unique data for the KNN classifier: list of exemplars (matrices)
        # if given data,
        if dataObj != None:
            # call the build function
            self.build(dataObj.getData(headers), categories)

    def build(self, A, categories, K=None):
        '''Builds the classifier given the data points in A and the categories'''

        # figure out how many categories there are and get the mapping (np.unique)
        unique, mapping = np.unique(np.array(categories.T), return_inverse=True)
        self.num_classes = len(unique)
        self.num_features = A.shape[1]
        self.class_labels = np.matrix(mapping).T
        # for each category i, build the set of exemplars
        self.exemplars = []
        for i in range(self.num_classes):
            data = A[(mapping == i), :]
            if K is None:
                self.exemplars.append(data)
            else:
                # run K-means on the rows of A where the category/mapping is i
                codebook, bookerror = vq.kmeans2(data, K)
                print(codebook)  # FIXME: numpy.linalg.linalg.LinAlgError: Matrix is not positive definite
                self.exemplars.append(codebook)
        # store any other necessary information: # of classes, # of features, original labels

        return

    def classify(self, A, K=3, return_distances=False):
        '''Classify each row of A into one category. Return a matrix of
        category IDs in the range [0..C-1], and an array of class
        labels using the original label values. If return_distances is
        True, it also returns the NxC distance matrix.

        The parameter K specifies how many neighbors to use in the
        distance computation. The default is three.'''

        # error check to see if A has the same number of columns as the class means
        assert A.shape[1] == self.num_features

        # make a matrix that is N x C to store the distance to each class for each data point
        N = A.shape[0]
        D = np.zeros((N, self.num_classes)) # a matrix of zeros that is N (rows of A) x C (number of classes)
        
        for i in range(self.num_classes):
            # make a temporary matrix that is N x M where M is the number of exemplars (rows in exemplars[i])
            M = self.exemplars[i].shape[0]
            temp = np.zeros((N, M))
            # calculate the distance from each point in A to each point in exemplar matrix i (for loop)
            for j in range(N):
                for k in range(M):
                    temp[j, k] = np.sqrt(np.sum(np.square(A[j, :] - self.exemplars[i][k, :])))
            np.sort(temp, axis=1)
            D[:, i] = np.sum(temp[:, 0:K], axis=1)

        # calculate the most likely class for each data point
        cats = np.matrix(np.argmin(D, axis=1)).T # take the argmin of D along axis 1
        print("Cats:")
        print(cats)

        # use the class ID as a lookup to generate the original labels
        # FIXME: labels: get lookup to work
        print("Class labels:")
        print(self.class_labels)
        # labels = self.class_labels[cats] isn't working
        labels = self.class_labels[cats[:, 0], 0]
        print("Labels:")
        print(labels)

        if return_distances:
            return cats, labels, D

        return cats, labels

    def __str__(self):
        '''Make a pretty string that prints out the classifier information.'''
        s = "\nKNN Classifier\n"
        for i in range(self.num_classes):
            s += 'Class %d --------------------\n' % (i)
            s += 'Number of Exemplars: %d\n' % (self.exemplars[i].shape[0])
            s += 'Mean of Exemplars  :' + str(np.mean(self.exemplars[i], axis=0)) + "\n"

        s += "\n"
        return s


    def write(self, filename):
        '''Writes the KNN classifier to a file.'''
        # extension
        return

    def read(self, filename):
        '''Reads in the KNN classifier from the file'''
        # extension
        return
    

