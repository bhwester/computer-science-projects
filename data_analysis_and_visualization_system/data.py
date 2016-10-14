# __Author__: 'Brian Westerman'
# __Date__: 2/15/16
# __File__: data.py

"""
getters, setters, adders, deleters in both raw and numeric format?
update method to equivocate raw data and numeric data? Call in read method?
how to deal with NaNs?
"""

import sys
import copy
import operator
import numpy as np
import csv
import analysis

class Data:

    # Constructor
    def __init__(self, filename=None, dataset=None):

        # create and initialize fields for the class
        self.raw_headers = []
        self.raw_types = []
        if dataset == None:
            self.raw_data = []
            self.header2raw = {}
            self.matrix_data = np.matrix([])
            self.header2matrix = {}
        else:
            self.raw_headers = dataset[0]
            self.raw_types = dataset[1]
            self.raw_data = dataset[2:]
            self.header2raw = {}
            self.matrix_data = np.matrix([])
            self.header2matrix = {}
            for i in range(len(self.raw_headers)):
                self.header2raw[self.raw_headers[i]] = i
            return

        if filename != None:
            self.read(filename)

    # puts the original data in string format into a list of lists, with one sublist for each data point
    def read(self, filename):

        # make a new file reader object
        fp = open(filename, 'rU')
        reader = csv.reader(fp, delimiter=',', skipinitialspace=True)

        # assign the headers and types
        # .__next__() NECESSARY FOR PYTHON 3.5 -- CHANGE TO .next() FOR PYTHON 2.7
        self.raw_headers = reader.__next__()
        self.raw_types = reader.__next__()

        # fill in the raw data
        for row in reader:
            self.raw_data.append(row)

        # map the headers to their column index in the raw data
        for i in range(len(self.raw_headers)):
            self.header2raw[self.raw_headers[i]] = i

        # go through each column of numeric data and convert the string data to numeric form (floats)
        # map the headers to their column index in the numeric data
        numeric_matrix = np.zeros((len(self.raw_data), len(self.raw_headers)), dtype='float64')
        cols = 0
        for i in range(len(self.raw_headers)):
            if self.raw_types[i] == "numeric" or self.raw_types[i] == "int" or self.raw_types[i] == "float":
                self.header2matrix[self.raw_headers[i]] = cols
                for j in range(len(self.raw_data)):
                    temp = copy.deepcopy(self.raw_data[j][i])
                    numeric_matrix[j, cols] = temp
                cols += 1

        # delete any other columns that were copied over
        if cols < len(self.raw_headers):
            numeric_matrix = numeric_matrix[:, :cols]

        # copy the matrix data to self.matrix_data and free some memory
        self.matrix_data = np.matrix(numeric_matrix)
        del numeric_matrix

    # returns a list of all of the headers in the raw data
    def get_raw_headers(self):

        return self.raw_headers

    # returns a list of all of the types in the raw data
    def get_raw_types(self):

        return self.raw_types

    # returns the number of columns in the raw data set
    def get_raw_num_columns(self):

        return len(self.raw_headers)

    # returns the number of rows in the raw data set
    def get_raw_num_rows(self):

        return len(self.raw_data)

    # returns a row of raw data (the type is list) given a row index (int) in the raw data
    def get_raw_row(self, row):

        return self.raw_data[row]

    # returns a column of raw data (the type is list) given a column header (string) in the raw data
    def get_raw_column(self, colHeader):

        # find the column index that colHeader is in
        col = self.header2raw[colHeader]

        # piece together a list containing the correctly indexed element of each row
        column = []
        for row in self.raw_data:
            column.append(row[col])

        return column

    # takes a row index (an int) and column header (a string) and returns the raw data (a string) at that location
    def get_raw_value(self, row, colHeader):

        # find the column index that colHeader is in
        col = self.header2raw[colHeader]

        return self.raw_data[row][col]

    # takes a list of column headers and return a matrix with the raw data for all rows but just the specified columns,
    # optional to also allow the caller to specify a specific set of rows
    def get_raw_data(self, colHeaders, rows=None):

        if rows != None:
            rowRange = np.array(rows)
        else:
            rowRange = range(len(self.raw_data))

        raw_data_matrix = np.zeros((len(rowRange), len(colHeaders)))
        for i in rowRange:
            for j in range(len(colHeaders)):
                header = self.header2raw[colHeaders[j]]
                raw_data_matrix[i-rowRange[0], j] = str(self.raw_data[i][header]) # adjust to fit regular matrices

        return raw_data_matrix

    # returns a list of all of the headers in the numeric data
    def get_headers(self):

        # return list(self.header2matrix.keys())
        return [x[0] for x in sorted(self.header2matrix.items(), key=operator.itemgetter(1))]

    # returns the number of columns in the numeric data set
    def get_num_columns(self):

        return self.matrix_data.shape[0]

    # returns the number of rows in the numeric data set
    def get_num_rows(self):

        return self.matrix_data.shape[1]

    # returns a row of data (the type is list) given a row index (int) in the numeric data
    def get_row(self, row):

        return self.matrix_data[row, :]

    # returns a column of data (the type is list) given a column header (string) in the numeric data
    def get_column(self, colHeader):

        if type(colHeader) == str:
            return self.matrix_data[:, self.header2matrix[colHeader]]
        elif type(colHeader) == int:
            return self.matrix_data[:, colHeader]
        else:
            return

    # takes a row index (an int) and column header (a string) and returns the numeric data (a float) at that location
    def get_value(self, row, colHeader):

        return self.matrix_data[row, self.header2matrix[colHeader]]

    # takes a list of column headers and return a matrix with the numeric data for all rows but just the specified
    # columns, optional to also allow the caller to specify a specific set of rows
    # start index and stop index?
    def get_data(self, colHeaders, rows=None):

        if rows != None:
            rowRange = np.array(rows)
        else:
            rowRange = np.arange(len(self.matrix_data))

        headers = [self.header2matrix[colHeader] for colHeader in colHeaders]
        matrix = np.hstack((self.matrix_data[rowRange, col] for col in headers))
        return matrix

    # updates a row of raw data in the Data object
    def set_raw_row(self, data, row):

        try:
            for i in range(len(data)):
                self.raw_data[row][i] = data[i]
            print("Row %i updated in raw data." % row)
        except: print("Error: index out of bounds. Row %i not updated." % row)



    # updates a row of numeric data in the Data object
    def set_row(self, data, row):

        try:
            self.matrix_data[row, :] = data
            print("Row %i updated in numeric data." % row)
        except: print("Error: index out of bounds. Row %i not updated." % row)

    # updates a column of data in the Data object
    def set_column(self, data, colHeader, type=None):

        numCol = self.header2matrix[colHeader]
        rawCol = self.header2raw[colHeader]
        if type != None:
            self.raw_types[rawCol] = type
        try:
            for i in range(len(self.matrix_data)):
                self.raw_data[i][rawCol] = str(np.array(data[i])[0, 0])
            self.matrix_data[:, numCol] = data
            print("Column %s updated.")
        except: print("Error: improper column title. Column '%s' not updated." % colHeader)

    # updates an individual value in the Data object
    def set_value(self, value, row, colHeader):

        numCol = self.header2matrix[colHeader]
        rawCol = self.header2raw[colHeader]
        try:
            self.matrix_data[row, numCol] = value
            self.raw_data[row][rawCol] = str(value)
            print("Value (%i, '%s') updated to ", value, "." % row, colHeader, value)
        except: print("Error: index out of bounds or improper column title. Value ", value, " not updated.")

    # adds a row of raw data to the Data object
    def add_raw_row(self, data):
        # incorporate type checking to allow each column in the row to be the correct type and prevent data from being
        # added if that's not the case
        try:
            if len(data) != len(self.raw_headers):
                print("Error: improper data dimensions. Row not added.")
                return
            self.raw_data.append([])
            for col in data:
                self.raw_data[-1].append(str(col))
            print("Row added to raw data.")
        except:
            print("Error: improper data dimensions. Row not added.")

    # adds a row of numeric data to the Data object
    def add_row(self, data):

        try:
            self.matrix_data = np.vstack((self.matrix_data, np.array(data)))
            print("Row added to numeric data.")
        except:
            print("Error: improper data dimensions. Row not added.")

    # adds a column of data to the Data object
    def add_column(self, data, colHeader, type):

        try:
            self.raw_headers.append(colHeader)
            self.raw_types.append(type)
            self.header2raw[colHeader] = len(self.header2raw)
            if type == 'numeric' or type == 'int' or type == 'float':
                self.header2matrix[colHeader] = len(self.header2matrix)
                newdata = np.array(data).reshape(len(self.matrix_data), 1)
                self.matrix_data = np.hstack([self.matrix_data, newdata])
            # ADD BACK IN
            # for i in range(len(self.raw_data)): # modify so that individual values are added rather than one-element matrices
            #     self.raw_data[i].append(str(np.array(data[i])[0, 0]))
            print("Column %s added." % colHeader)
        except: print("Error: improper data dimensions. Column %s not added." % colHeader)

    # deletes a row of data from the Data object
    def delete_row(self, row):

        try:
            self.matrix_data = np.delete(self.matrix_data, row, axis=0)
            del self.raw_data[row]
            print ("Row %i deleted." % row)
        except: print("Error: index out of bounds. Row %i not deleted." % row)

    # deletes a column of data from the Data object
    def delete_column(self, colHeader):

        try:
            try:
                numCol = self.header2matrix[colHeader]
                del self.header2matrix[colHeader]
                self.matrix_data = np.delete(self.matrix_data, numCol, axis=1)
            except KeyError:
                pass
            rawCol = self.header2raw[colHeader]
            del self.raw_headers[rawCol]
            del self.raw_types[rawCol]
            del self.header2raw[colHeader]
            for i in range(len(self.raw_data)):
                del self.raw_data[i][rawCol]
            print("Column %s deleted." % colHeader)
        except: print("Error: improper column title. Column %s not deleted." % colHeader)

    # prints out the data to the command line
    def printData(self, numRows=999999):

        print("\n\nData:")
        print(self.raw_headers)
        print(self.raw_types)
        print(self.matrix_data[:numRows, :])
        print(self.raw_data[:numRows])

    # writes out a selected set of headers to a specified file
    def writeHeaders(self, filename, headers=None):

        if headers != None:
            with open(filename, 'w') as f:
                f.write(headers)
            f.close()
        else:
            print("No headers given")


""" Holds information for data in PCA space"""
class PCAData(Data):

    # Constructor
    def __init__(self, data, evecs, evals, means, headers):

        Data.__init__(self)
        self.matrix_data = data  # numpy matrix of projected data
        self.evecs = evecs  # numpy matrix with evecs on rows
        self.evals = evals  # one row numpy matrix
        self.means = means  # one row numpy matrix
        self.headers = headers  # list

        for i in range(len(headers)):
            self.header2matrix[headers[i]] = i
        for i in range(self.matrix_data.shape[0]):
            self.raw_data.append(self.matrix_data[i, :].tolist()[0])

    # Accessor for self.matrix_data
    def get_matrix_data(self):
        return self.matrix_data

    # Accessor for self.evecs
    def get_eigenvectors(self):
        return self.evecs

    # Accessor for self.evals
    def get_eigenvalues(self):
        return self.evals

    # Accessor for self.means
    def get_data_means(self):
        return self.means

    # Accessor for self.headers
    def get_data_headers(self):
        return self.headers



if __name__ == "__main__":

    # # Load the data files into a Data object
    # dataClean = Data(filename='data-clean.csv')
    # dataGood = Data(filename='data-good.csv')
    # dataNoisy = Data(filename='data-noisy.csv')
    #
    # # Run multiple linear regression on the Data objects
    # analysis.testRegression(dataClean)
    # analysis.testRegression(dataGood)
    # analysis.testRegression(dataNoisy)

    data = Data(filename='GOOG-NASDAQ_TSLA.csv')

    # print out some analyses
    print("\n\nDescriptive statistics of Tesla's stock data (daily open and close prices and trading volume:")
    print("Mean: ", analysis.mean(['Open', 'Close', 'Volume'], data))
    print("Standard deviation: ", analysis.stdev(['Open', 'Close', 'Volume'], data))
    print("Ranges: ", analysis.dataRange(['Open', 'Close', 'Volume'], data))
    print("Normalized columns: ", analysis.normalizeColumnsSeparately(['Open', 'Close', 'Volume'], data))
    print("Normalized globally: ", analysis.normalizeColumnsTogether(['Open', 'Close', 'Volume'], data))
    print("Variance: ", analysis.variance(['Open', 'Close', 'Volume'], data))
    print("Median: ", analysis.median(['Open', 'Close', 'Volume'], data))
    print("Mode value: ", analysis.modeValue(['Open', 'Close', 'Volume'], data))
    print("Mode frequency: ", analysis.modeFreq(['Open', 'Close', 'Volume'], data))
    print("Range value: ", analysis.rangeDiff(['Open', 'Close', 'Volume'], data), "\n")

    data.printData(20)

    # manipulate the data to show their efficacy
    data.set_value(0.0001, 5, 'Open')
    data.set_column(data.get_column('Open'), 'Close')
    data.add_column(data.get_column('Volume'), 'Volume2', 'numeric')
    data.add_raw_row(['6/28/10', 2.0, 3.0, 4.0, 5.0, 1000.0, 3])
    data.add_row([1.0, 2.0, 3.0, 4.0, 5.0, 6])

    # Here I print out the whole data set to show its full five-year comprehensive glory
    data.printData(20)

    # run some more methods to test
    print(data.get_data(['High', 'Low'], range(30, 50)))
    data.delete_column('Date')
    data.delete_row(0)

    data.printData(20)

    # print out some more stats about the dataset
    print("Extra stats:")
    print("Headers: ", data.get_headers())
    print("Types: ", data.get_raw_types())
    print("Column numbers: ", data.get_num_columns())
    print("Row numbers: ", data.get_num_rows())
    print("Row 3: ", data.get_row(2))
    print("Column \'Open\': ", data.get_column('Open'))

    data.set_raw_row(data.get_raw_row(5), 6)
    data.set_row(data.get_row(3), 4)

    data.printData(20)