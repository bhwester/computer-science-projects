# __Author__: 'Brian Westerman'
# __Date__: 2/15/16
# __File__: display.py

import tkinter as tk
import tkinter.font as tkf
import tkinter.filedialog as tkfd
import operator
import math
import random
import analysis
import data
import view
import classifiers
import numpy as np
import scipy.stats as st
import csv

# Create a class to build and manage the display
class DisplayApp:

    def __init__(self, width, height):

        # create a View object
        self.view = view.View()

        # create a tk object, which is the root window
        self.root = tk.Tk()

        # width and height of the window
        self.initDx = width
        self.initDy = height

        # set up the geometry for the window
        self.root.geometry("%dx%d+50+30" % (self.initDx, self.initDy))

        # set the title of the window
        self.root.title("Three guys walk into a bar. A duck walks in. The three guys look confused. Then a horse leaps "
                        "up from behind the counter and says, 'Why the long face?'")

        # set the maximum size of the window for resizing
        self.root.maxsize(1600, 900)

        # create a Data object to hold incoming data
        self.filename = None
        self.dataFiles = None
        self.currentData = None
        self.PCAData = {}
        self.currentAxes = None
        self.PCAAxes = {}
        self.points = np.matrix([[]])
        self.viewPoints = np.matrix([[]])
        self.legend = None

        # set up variables for linear regression
        self.regressionEndpoints = None
        self.viewRegressionEndpoints = None
        self.regressionInfo = None
        self.regressionLine = []
        self.regressionLine = None

        # setup the menus
        self.buildMenus()

        # build the controls
        self.buildControls()

        # build the Canvas
        self.buildCanvas()

        # build the axes
        self.axisEndpoints = np.matrix([[0, 0, 0, 1],
                                        [1, 0, 0, 1],
                                        [0, 0, 0, 1],
                                        [0, 1, 0, 1],
                                        [0, 0, 0, 1],
                                        [0, 0, 1, 1]])
        self.buildAxes()

        # bring the window to the front
        self.root.lift()

        # - do idle events here to get actual canvas size
        self.root.update_idletasks()

        # now we can ask the size of the canvas
        print(self.canvas.winfo_geometry())

        # set up the key bindings
        self.setBindings()

        # set up variables involved with the application state
        self.objects = [] # list of data objects that will be drawn in the canvas
        self.baseClick1 = None # used to keep track of mouse movement 1
        self.baseClick2 = None # used to keep track of mouse movement 2
        self.baseClick3 = None # used to keep track of mouse movement 3
        self.baseClick4 = None # used to keep track of mouse movement 4
        self.numDataPoints = 100
        self.origScale = 1
        self.viewExtent = self.view.extent

        # capture whether the x and y data distribution are uniform or gaussian, from project 1
        self.xDistribution = 0 # defaults to uniform
        self.yDistribution = 0 # defaults to uniform

    def buildMenus(self):

        # create a new menu
        menu = tk.Menu(self.root)

        # set the root menu to our new menu
        self.root.config(menu = menu)

        # create a variable to hold the individual menus
        menulist = []

        # create a file menu
        filemenu = tk.Menu(menu)
        menu.add_cascade(label = "File", menu = filemenu)
        menulist.append(filemenu)

        # create another menu for kicks
        cmdmenu = tk.Menu(menu)
        menu.add_cascade(label = "Command", menu = cmdmenu)
        menulist.append(cmdmenu)

        # menu text for the elements
        # the first sublist is the set of items for the file menu
        # the second sublist is the set of items for the option menu
        menutext = [['Open  \xE2\x8C\x98-O', 'Quit  \xE2\x8C\x98-Q', 'Clear data  \xE2\x8C\x98-N'],
                     ['Plot data  \xE2\x8C\x98-P', 'Run linear regression  \xE2\x8C\x98-R']]

        # menu callback functions (note that some are left blank,
        # so that you can add functions there if you want).
        # the first sublist is the set of callback functions for the file menu
        # the second sublist is the set of callback functions for the option menu
        menucmd = [[self.handleOpen, self.handleQuit, self.clearData],
                    [self.handlePlotData, self.handleLinearRegression]]

        # build the menu elements and callbacks
        for i in range(len(menulist)):
            for j in range(len(menutext[i])):
                if menutext[i][j] != '-':
                    menulist[i].add_command(label = menutext[i][j], command=menucmd[i][j])
                else:
                    menulist[i].add_separator()

    # build a frame and put controls in it
    def buildControls(self):

        ### Control ###

        # make a status panel on the bottom
        bottomStatusPanel = tk.Frame(self.root)
        bottomStatusPanel.pack(side=tk.BOTTOM, padx=2, pady=2, fill=tk.Y)

        # use a label to set the size of the status panel
        label = tk.Label(bottomStatusPanel, text="Status Panel")
        label.pack(side=tk.TOP, pady=10)

        # make a separator frame
        sep = tk.Frame(self.root, width=self.initDx, height=2, bd=1, relief=tk.SUNKEN)
        sep.pack(side=tk.BOTTOM, padx = 2, pady = 2, fill=tk.Y)

        # make a control frame on the right
        self.rightControlFrame = tk.Frame(self.root)
        self.rightControlFrame.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

        # use a label to set the size of the right panel
        label = tk.Label(self.rightControlFrame, text="Control Panel", width=20)
        label.pack(side=tk.TOP, pady=10)

        # make a separator frame
        sep = tk.Frame(self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN)
        sep.pack(side=tk.RIGHT, padx = 2, pady = 2, fill=tk.Y)

        # make a button that selects the axes
        selectAxesButton = tk.Button(self.rightControlFrame, text="Select axes",
                                    command=self.handleChooseAxes)
        selectAxesButton.pack(side=tk.TOP, pady=5)

        # make a button that plots the data
        plotDataButton = tk.Button(self.rightControlFrame, text="Plot data",
                                    command=self.handlePlotData)
        plotDataButton.pack(side=tk.TOP, pady=5)

        # make a button that clusters the data
        clusterDataButton = tk.Button(self.rightControlFrame, text="Cluster data",
                                    command=self.handleClusterData)
        clusterDataButton.pack(side=tk.TOP, pady=5)

        # make a button that classifies the data
        classifyDataButton = tk.Button(self.rightControlFrame, text="Classify data",
                                    command=self.handleClassifyData)
        classifyDataButton.pack(side=tk.TOP, pady=5)

        # make a button that selects the axes
        selectPCAAxesButton = tk.Button(self.rightControlFrame, text="Add PCA analysis",
                                    command=self.handleChoosePCAAxes)
        selectPCAAxesButton.pack(side=tk.TOP, pady=5)

        # make a listbox that displays all PCA analysis entries
        self.PCAEntries = tk.Listbox(self.rightControlFrame)
        self.PCAEntries.pack(side=tk.TOP, pady=5)

        # make a button that projects the data onto its selected principal components
        projectPCADataButton = tk.Button(self.rightControlFrame, text="Project PCA data", command=self.projectData)
        projectPCADataButton.pack(side=tk.TOP, pady=5)

        # make a button that clusters the PCA data
        clusterPCADataButton = tk.Button(self.rightControlFrame, text="Cluster PCA data",
                                    command=self.handleClusterData)
        clusterPCADataButton.pack(side=tk.TOP, pady=5)

        # make a button that classifies the PCA data
        classifyPCADataButton = tk.Button(self.rightControlFrame, text="Classify PCA data",
                                    command=self.handleClassifyData)
        classifyPCADataButton.pack(side=tk.TOP, pady=5)

        # make a button that deletes a PCA analysis entry
        deletePCAEntryButton = tk.Button(self.rightControlFrame, text="Delete PCA entry", command=self.deletePCAEntry)
        deletePCAEntryButton.pack(side=tk.TOP, pady=5)

        # make a button that resets the view to default
        resetViewButton = tk.Button(self.rightControlFrame, text="Reset view to default",
                                    command=self.resetView)
        resetViewButton.pack(side=tk.TOP, pady=5)

        # make a button that moves the view to the XY plane
        hotKeyXYButton = tk.Button(self.rightControlFrame, text="Rotate to XY plane", command=self.hotKeyXY)
        hotKeyXYButton.pack(side=tk.TOP, pady=5)

        # make a button that moves the view to the XZ plane
        hotKeyXZButton = tk.Button(self.rightControlFrame, text="Rotate to XZ plane", command=self.hotKeyXZ)
        hotKeyXZButton.pack(side=tk.TOP, pady=5)

        # make a button that moves the view to the YZ plane
        hotKeyYZButton = tk.Button(self.rightControlFrame, text="Rotate to YZ plane", command=self.hotKeyYZ)
        hotKeyYZButton.pack(side=tk.TOP, pady=5)

        return

    # create the canvas object
    def buildCanvas(self):

        self.canvas = tk.Canvas(self.root, width=self.initDx, height=self.initDy)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        return

    def setBindings(self):

        # bind mouse motions to the canvas
        self.canvas.bind('<Button-1>', self.handleMouseButton1)
        self.canvas.bind('<Button-2>', self.handleMouseButton2)
        self.canvas.bind('<Control-Button-1>', self.handleMouseButton2)
        self.canvas.bind('<Command-Button-1>', self.handleMouseButton3)
        self.canvas.bind('<Command-Button-2>', self.handleMouseButton4)
        self.canvas.bind('<Shift-Command-Button-1>', self.handleShiftCommandMouseButton1)
        self.canvas.bind('<B1-Motion>', self.handleMouseButton1Motion)
        self.canvas.bind('<B2-Motion>', self.handleMouseButton2Motion)
        self.canvas.bind('<Control-B1-Motion>', self.handleMouseButton2Motion)
        self.canvas.bind('<Command-B1-Motion>', self.handleMouseButton3Motion)
        self.canvas.bind('<Command-B2-Motion>', self.handleMouseButton4Motion)

        # bind command sequences to the root window
        self.root.bind('<Command-o>', self.handleOpen)
        self.root.bind('<Command-q>', self.handleQuit)
        self.root.bind('<Command-p>', self.handlePlotData)
        self.root.bind('<Command-r>', self.handleLinearRegression)
        self.root.bind('<Command-c>', self.clearData)
        self.root.bind('<Command-n>', self.resetView)
        self.root.bind('<Command-x>', self.hotKeyXY)
        self.root.bind('<Command-y>', self.hotKeyYZ)
        self.root.bind('<Command-z>', self.hotKeyXZ)

    def handleOpen(self, event=None):

        # Get a list of files the user has selected
        self.filename = []
        files = list(tkfd.askopenfilenames(parent=self.root, title="Choose a data file", initialdir='.'))
        for i in range(len(files)):
            self.filename.append(files[i])

        # Create a list of Data objects corresponding to the files the user has selected
        self.dataFiles = []
        for i in range(len(self.filename)):
            self.dataFiles.append(data.Data(filename=self.filename[i]))
        self.currentData = self.dataFiles[0]

    # builds the axes
    def buildAxes(self):

        # Make a local copy of the VTM
        vtm = self.view.build()

        # Compute axis endpoints
        x0 = vtm * self.axisEndpoints[0, :].T
        x1 = vtm * self.axisEndpoints[1, :].T
        y0 = vtm * self.axisEndpoints[2, :].T
        y1 = vtm * self.axisEndpoints[3, :].T
        z0 = vtm * self.axisEndpoints[4, :].T
        z1 = vtm * self.axisEndpoints[5, :].T

        # Generates three line objects, one for each axis, with the transformed endpoints as the pixel locations for the lines
        xAxis = self.canvas.create_line(int(x0[0]), int(x0[1]), int(x1[0]), int(x1[1]), fill='black')
        yAxis = self.canvas.create_line(int(y0[0]), int(y0[1]), int(y1[0]), int(y1[1]), fill='black')
        zAxis = self.canvas.create_line(int(z0[0]), int(z0[1]), int(z1[0]), int(z1[1]), fill='black')
        self.axes = []
        self.axes.append(xAxis)
        self.axes.append(yAxis)
        self.axes.append(zAxis)

        # Generates three text objects, one for each axis, centered at each axis endpoint
        xLabel = self.canvas.create_text(int(x1[0]), int(x1[1]), text='X', fill='black')
        yLabel = self.canvas.create_text(int(y1[0]), int(y1[1]), text='Y', fill='black')
        zLabel = self.canvas.create_text(int(z1[0]), int(z1[1]), text='Z', fill='black')
        self.axes.append(xLabel)
        self.axes.append(yLabel)
        self.axes.append(zLabel)

    # updates the axes if the VTM is modified
    def updateAxes(self):

        # Make a local copy of the VTM
        vtm = self.view.build()

        # Update all points in self.axisEndpoints
        x0 = vtm * self.axisEndpoints[0, :].T
        x1 = vtm * self.axisEndpoints[1, :].T
        y0 = vtm * self.axisEndpoints[2, :].T
        y1 = vtm * self.axisEndpoints[3, :].T
        z0 = vtm * self.axisEndpoints[4, :].T
        z1 = vtm * self.axisEndpoints[5, :].T

        # Update the canvas coordinates of all the axis endpoints and axis labels
        self.canvas.coords(self.axes[0], int(x0[0]), int(x0[1]), int(x1[0]), int(x1[1]))
        self.canvas.coords(self.axes[1], int(y0[0]), int(y0[1]), int(y1[0]), int(y1[1]))
        self.canvas.coords(self.axes[2], int(z0[0]), int(z0[1]), int(z1[0]), int(z1[1]))
        self.canvas.coords(self.axes[3], int(x1[0]), int(x1[1]))
        self.canvas.coords(self.axes[4], int(y1[0]), int(y1[1]))
        self.canvas.coords(self.axes[5], int(z1[0]), int(z1[1]))

    def buildPoints(self, headers, dataset=None, fillColors=None, PCAData=False, clustering=False, classification=False):

        # headers is always length 5, {X, Y, [Z || None, ][Color || None, ][Size || None]}
        # Z, Color, and Size are optional (X and Y are mandatory); if not chosen replaced by None

        self.clearData()
        if dataset == None:
            dataset = self.currentData
        colorPoints = []
        sizePoints = []

        # Modify to allow for plotting PCA data?
        # Consider normalizing using standard deviation when implementing machine learning or doing dimensionality reduction

        # Good handling of the various possible axis choices.  I think you could
        # simplify the process by making the color and size independent (you
        # either choose them or not).  You can do that by always generating a
        # colors list and a sizes list.  If the user picks an axis for either,
        # then generate the appropriate colors/sizes for each data point.  If
        # they don't pick an axis, then make the corresponding list have the
        # same value for each data point.  Then you can compress your code a
        # good bit and have a single drawing loop that always works for every
        # combination.

        # In the legend, the eigenvector directions should not be labeled as
        # original data columns.  Each eigenvector has one coefficient that
        # corresponds to a single original data column, but the eigenvectors
        # themselves represent unique directions in the data space.  They should
        # get names like PCA0, PCA1, and so on.
        # Instead of X, Y, Z, Color, Size

        z = False if headers[2] is None else True
        color = False if headers[3] is None else True
        size = False if headers[4] is None else True
        # Capture only the headers (always length 5, can include None) that carry information
        headers = [header for header in headers if header is not None]

        # Normalize color and size axes
        if not z:  # no Z axis chosen
            if color and size:  # color and size chosen
                colorPoints = analysis.normalizeColumnsSeparately([headers[2]], dataset)
                sizePoints = analysis.normalizeColumnsSeparately([headers[3]], dataset)
            elif color:  # only color chosen
                colorPoints = analysis.normalizeColumnsSeparately([headers[2]], dataset)
            elif size:  # only size chosen
                sizePoints = analysis.normalizeColumnsSeparately([headers[2]], dataset)
            else:
                pass  # no color or size chosen
        if z:  # Z axis chosen
            if color and size:  # color and size chosen
                colorPoints = analysis.normalizeColumnsSeparately([headers[3]], dataset)
                sizePoints = analysis.normalizeColumnsSeparately([headers[4]], dataset)
            elif color:  # only color chosen
                colorPoints = analysis.normalizeColumnsSeparately([headers[3]], dataset)
            elif size:  # only size chosen
                sizePoints = analysis.normalizeColumnsSeparately([headers[3]], dataset)
            else:  # no color or size chosen
                pass

        # Create text string for legend
        if PCAData:  # PCA data, label as eigenvectors
            if len(headers) == 2:
                legendText = "Legend\n\nX: PCA0\nY: PCA1"
            elif len(headers) == 3:
                legendText = "Legend\n\nX: PCA0\nY: PCA1\nZ: PCA2"
            elif len(headers) == 4:
                if not clustering or classification:
                    legendText = "Legend\n\nX: PCA0\nY: PCA1\nZ: PCA2\nColor: PCA3"
                else:
                    legendText = "Legend\n\nX: PCA0\nY: PCA1\nZ: PCA2"
            elif len(headers) == 5:
                if not clustering or classification:
                    legendText = "Legend\n\nX: PCA0\nY: PCA1\nZ: PCA2\nColor: PCA3\nSize: PCA4"
                else:
                    legendText = "Legend\n\nX: PCA0\nY: PCA1\nZ: PCA2\nSize: PCA4"
            else:
                legendText = "Error in size of headers"
        else:  # normal data, label as {X, Y, Z, Color, Size}
            if not z:  # no Z axis chosen
                if color and size:  # color and size chosen
                    if not clustering or classification:
                        legendText = "Legend\n\nX: " + headers[0] + "\nY: " + headers[1] + \
                            "\nColor: " + headers[2] + "\nSize: " + headers[3]
                    else:
                        legendText = "Legend\n\nX: " + headers[0] + "\nY: " + headers[1] + "\nSize: " + headers[3]
                elif color:  # only color chosen
                    if not clustering or classification:
                        legendText = "Legend\n\nX: " + headers[0] + "\nY: " + headers[1] + "\nColor: " + headers[2]
                    else:
                        legendText = "Legend\n\nX: " + headers[0] + "\nY: " + headers[1]
                elif size:  # only size chosen
                    legendText = "Legend\n\nX: " + headers[0] + "\nY: " + headers[1] + "\nSize: " + headers[2]
                else:  # no color or size chosen
                    legendText = "Legend\n\nX: " + headers[0] + "\nY: " + headers[1]
            else:  # Z axis chosen
                if color and size:  # color and size chosen
                    if not clustering or classification:
                        legendText = "Legend\n\nX: " + headers[0] + "\nY: " + headers[1] + "\nZ: " + headers[2] + \
                            "\nColor: " + headers[3] + "\nSize: " + headers[4]
                    else:
                        legendText = "Legend\n\nX: " + headers[0] + "\nY: " + headers[1] + \
                            "\nZ: " + headers[2] + "\nSize: " + headers[4]
                elif color:  # only color chosen
                    if not clustering or classification:
                        legendText = "Legend\n\nX: " + headers[0] + "\nY: " + headers[1] + "\nZ: " + headers[2] + "\nColor: " + headers[3]
                    else:
                        legendText = "Legend\n\nX: " + headers[0] + "\nY: " + headers[1] + "\nZ: " + headers[2]
                elif size:  # only size chosen
                    legendText = "Legend\n\nX: " + headers[0] + "\nY: " + headers[1] + "\nZ: " + headers[2] + "\nSize: " + headers[3]
                else:  # no color or size chosen
                    legendText = "Legend\n\nX: " + headers[0] + "\nY: " + headers[1] + "\nZ: " + headers[2]

        # Create the legend
        self.canvas.delete(self.legend)
        self.legend = self.canvas.create_text(590, 15, text=legendText, anchor=tk.NE, justify=tk.CENTER)

        # Build self.points by normalizing the X, Y[, Z] headers
        if color and size:
            headers = headers[:-2]
        elif color or size:
            headers = headers[:-1]  # otherwise don't chop off any headers
        self.currentAxes = headers
        self.points = analysis.normalizeColumnsSeparately(headers, dataset)
        if z:
            self.points = np.hstack((self.points,
                                     np.ones((len(self.points), 1))))
        else:
            self.points = np.hstack((self.points,
                                     np.zeros((len(self.points), 1)),
                                     np.ones((len(self.points), 1))))

        # Make a local copy of the VTM and transform the 3D data to fit the current axis alignment
        vtm = self.view.build()
        self.viewPoints = (vtm * self.points.T).T

        # Plot each point in the canvas, specifying the color and/or size if selected when choosing axes
        self.dx = []
        for i in range(len(self.viewPoints)):

            # if size was given, set the size (normalized 0 => 1, normalized 1 => 10)
            if len(sizePoints) != 0:
                self.dx.append(int(sizePoints[i] * 9 + 1))
            else:
                self.dx.append(3) # defaults point radius to 3 if the size axis was not chosen

            # If color was given, set the color
            if len(colorPoints) != 0:
                v = colorPoints[i]
                fillColor = '#%02X%02X%02X' % (int(255*v), int(255*v), int(255*(1-v)))
            else:
                fillColor = '#%02X%02X%02X' % (0, 0, 0)

            if clustering:  # override fillColor
                # Assign fillColor=fillColors[i] based on the ClusterID column of the data
                fillColor = fillColors[int(dataset.get_value(i, "ClusterID"))]
            if classification:  # override fillColor
                # Assign fillColor=fillColors[i] based on the Labels/etc. column of the data
                fillColor = fillColors[int(dataset.get_value(i, "class"))]  # may not be called 'Labels', could be 'class' or something else

            # Draw points in the canvas
            pt = self.canvas.create_oval(self.viewPoints[i][0, 0]-self.dx[i],
                                         self.viewPoints[i][0, 1]-self.dx[i],
                                         self.viewPoints[i][0, 0]+self.dx[i],
                                         self.viewPoints[i][0, 1]+self.dx[i],
                                         fill=fillColor,
                                         outline='')

            self.objects.append(pt)

    def updatePoints(self):

        # Exit if there are no data objects in the canvas
        if len(self.objects) == 0:
            return

        # Normalize data points
        if len(self.currentAxes) == 2:
            mins = np.min(self.points[:, :-2], axis=0)
            maxes = np.max(self.points[:, :-2], axis=0)
            self.points = np.divide((self.points[:, :-2] - mins), (maxes - mins))
            self.points = np.hstack((self.points,
                                     np.zeros((self.points.shape[0], 1)),
                                     np.ones((self.points.shape[0], 1))))
        else:
            mins = np.min(self.points[:, :-1], axis=0)
            maxes = np.max(self.points[:, :-1], axis=0)
            self.points = np.divide((self.points[:, :-1] - mins), (maxes - mins))
            self.points = np.hstack((self.points, np.ones((self.points.shape[0], 1))))

        # Make a local copy of the VTM
        vtm = self.view.build()
        self.viewPoints = (vtm * self.points.T).T

        # Plot each point in the canvas
        for i in range(len(self.viewPoints)):
            # Letting the user specify the type of graphics object to use in the plot is a nice extension
            self.canvas.coords(self.objects[i],
                               self.viewPoints[i, 0]-self.dx[i],
                               self.viewPoints[i, 1]-self.dx[i],
                               self.viewPoints[i, 0]+self.dx[i],
                               self.viewPoints[i, 1]+self.dx[i])

    def handlePlotData(self, event=None):

        if not self.currentAxes or self.currentAxes == []:
            print("Error: axes not yet selected. Choose a parameter for at least the x axis and y axis.")
            return
        self.buildPoints(self.currentAxes, dataset=self.currentData)

    def handleChooseAxes(self, event=None):

        try:
            # Create a list of headers the user can choose from to plot on each of the five possible axes
            headers = self.currentData.get_headers()
            # Create a dialog box
            dialogBox = PlotDialog(parent=self.root, headers=headers)
            # grab the results
            try:
                selections = dialogBox.choices
            except:
                return

            if selections[0] is None or selections[1] is None:
                print("Error: not enough selections. Choose a parameter for at least the x axis and y axis.")
                return
            self.currentAxes = selections
        except:
            print("Error: no data loaded. Open a file first.")

    def handleChoosePCAAxes(self, event=None):

        # Allow for self.currentData to be transferred back to original Data object
        try:
            # Create a list of headers the user can choose from to select their PCA axes
            headers = self.currentData.get_headers()
            # Create a dialog box
            dialogBox = PCADialog(parent=self.root, headers=headers)

            # Grab the results
            try:
                selections = dialogBox.choices
                title = dialogBox.titleChoice
            except:
                return

            if selections is None or selections[0] is None or selections[1] is None:
                print("Error: not enough selections. Choose at least two axes.")
                return

            # Add a dictionary entry with the title and the PCA axis selections
            self.PCAAxes[title] = selections
            # Add this title to the PCA entries listbox
            self.PCAEntries.insert(tk.END, title)

            # Run PCA on the selected axes
            pcadata = analysis.pca(self.currentData, self.PCAAxes[title], norm=True)
            self.PCAData[title] = pcadata

        except:
            print("Error: no data loaded. Open a file first.")

    def projectData(self, event=None):

        selection = self.PCAEntries.get(self.PCAEntries.curselection())
        headers = self.PCAAxes[selection]
        # Fills in headers so that there is information for all axes for buildPoints
        while len(headers) < 5:
            headers.append(None)
        # Makes sure only 5 axes are passed into buildPoints
        if len(headers) > 5:
            headers = headers[:5]
        currentPCAData = self.PCAData[selection]

        self.buildPoints(headers, dataset=currentPCAData, PCAData=True)

    def displayPCATable(self, event=None):

        try:
            selection = self.PCAEntries.get(self.PCAEntries.curselection())
            currentPCAData = self.PCAData[selection]
            # Continue implementing
        except:
            print("Error: no entry selected. Please select an entry.")

    def deletePCAEntry(self, event=None):

        try:
            selection = self.PCAEntries.get(self.PCAEntries.curselection())
            self.PCAEntries.delete(self.PCAEntries.curselection())
            del self.PCAAxes[selection]
            del self.PCAData[selection]
        except:
            print("Error: no entry selected. Please select an entry.")

    def handleClusterData(self):

        # Allow for self.currentData to be transferred back to original Data object
        # Allow to work on PCA data as well

        # Create a list of headers the user can choose from to select their clustering axes
        headers = self.currentData.get_headers()
        # Create a dialog box
        dialogBox = ClusterDialog(parent=self.root, headers=headers, PCAChoices=[x[0] for x in sorted(self.PCAAxes.items(), key=operator.itemgetter(1))])

        # Grab the results
        try:
            selections = dialogBox.choices
            data = dialogBox.PCADataChoice
            k = int(dialogBox.kChoice)
        except:
            return

        if selections is None or selections[0] is None or selections[1] is None:
            print("Error: not enough selections. Choose at least two axes.")
            return

        # Allow the user to choose between the regular loaded data and a specific PCA analysis in the listbox
        if data == []:
            data = self.currentData
        codebook, codes, errors = analysis.kmeans(data, selections, k)

        # Add the cluster IDs to the current Data object as a new column
        data.add_column(codes, 'ClusterID', 'numeric')

        # Determine colors to paint each cluster
        # Currently distributed from yellow to blue (change to hue wheel or other?)
        clusters = np.unique(codes)
        fillColors = []
        for i in range(len(clusters)):
            v = clusters[i]/len(clusters)
            fillColor = '#%02X%02X%02X' % (int(255*(1-v)), int(255*(1-v)), int(255*(v)))
            fillColors.append(fillColor)

        # Fills in headers so that there is information for all axes for buildPoints
        while len(selections) < 5:
            selections.append(None)
        # Makes sure only 5 axes are passed into buildPoints
        if len(selections) > 5:
            selections = selections[:5]

        # dataset, fillColors, and clustering all need to be specified
        self.buildPoints(selections, dataset=data, fillColors=fillColors, clustering=True)

    def handleClassifyData(self):

        # Allow for self.currentData to be transferred back to original Data object
        # Allow to work on PCA data and clustered data as well

        # Ask the user to input a filename in the command line
        filename = input("\nYour classifiers will be saved to a file and the confusion matrices will be printed.\n\n"
                         "Enter a file name to store the classified data in: ")

        # Generate classifiers (NBC and KNN) for the passed in data, print out confusion matrices, and write the
        # data with a column added for the predicted labels to a new file
        self.readWriteClassifier(filename, 'iris_proj8_train.csv', 'iris_proj8_test.csv')#'UCI-X-train.csv', 'UCI-X-test.csv', 'UCI-Y-train.csv', 'UCI-Y-test.csv')

        # Get output labels from written file to determine colors to paint each cluster
        classifyData = data.Data(filename)
        # Currently distributed from yellow to blue (change to hue wheel or other?)
        classes = np.unique(np.array(classifyData.get_column('class')))  # may not be called 'Labels', could be 'class' or something else
        fillColors = []
        for i in range(len(classes)):
            v = classes[i]/len(classes)
            fillColor = '#%02X%02X%02X' % (int(255*(1-v)), int(255*(1-v)), int(255*(v)))
            fillColors.append(fillColor)

        # Let the user specify the axes they want to plot in the viewing window (color choice will be replaced by classification colors)
        self.handleChooseAxes()

        # Fill in headers so that there is information for all axes for buildPoints
        selections = self.currentAxes  # or self.PCAAxes[] or handleChoosePCAAxes
        while len(selections) < 5:
            selections.append(None)
        # Make sure only 5 axes get passed into buildPoints
        if len(selections) > 5:
            selections = selections[:5]

        # Plot points in the view window with color specifying the class each point has been classified in
        # dataset, fillColors, and classification all need to be specified
        self.buildPoints(selections, dataset=classifyData, fillColors=fillColors, classification=True)

    def readWriteClassifier(self, filename, train, test, trainLabels=None, testLabels=None, K=None, Kmeans=None):

        # Generate Data objects from train and test sets
        trainData = data.Data(train)
        testData = data.Data(test)

        # Make the data and labels
        if trainLabels != None and testLabels != None:
            trainLabelsData = data.Data(trainLabels)
            testLabelsData = data.Data(testLabels)
            trainLabels1 = trainLabelsData.get_data([trainLabelsData.get_headers()[0]])
            testLabels1 = testLabelsData.get_data([testLabelsData.get_headers()[0]])
            A = trainData.get_data(trainData.get_headers())
            B = testData.get_data(testData.get_headers())
        else:
            trainLabels1 = trainData.get_data([trainData.get_headers()[-1]])
            testLabels1 = testData.get_data([testData.get_headers()[-1]])
            A = trainData.get_data(trainData.get_headers()[:-1])
            B = testData.get_data(testData.get_headers()[:-1])

        # Initialize and build classifiers for NBC and KNN
        nbc = classifiers.NaiveBayes()
        nbc.build(A, trainLabels1)
        knn = classifiers.KNN(K=K)
        knn.build(A, trainLabels1, K=Kmeans)

        # Classify train and test sets for NBC and KNN
        nbcTrainCats, nbcTrainLabels = nbc.classify(A)
        nbcTestCats, nbcTestLabels = nbc.classify(B)
        knnTrainCats, knnTrainLabels = knn.classify(A)
        knnTestCats, knnTestLabels = knn.classify(B)

        # Print out a confusion matrix for each classification
        print(nbc.confusion_matrix_str(nbc.confusion_matrix(nbcTrainLabels, nbcTrainCats)))
        print(nbc.confusion_matrix_str(nbc.confusion_matrix(nbcTestLabels, nbcTestCats)))
        print(knn.confusion_matrix_str(knn.confusion_matrix(knnTrainLabels, knnTrainCats)))
        print(knn.confusion_matrix_str(knn.confusion_matrix(knnTestLabels, knnTestCats)))

        # Make sure the test labels are in the output Data object
        if trainLabels != None and testLabels != None:
            outputData = testData.add_column(testLabels1, 'Labels', 'numeric')
        else:
            outputData = testData

        # Write data to a CSV file
        outputMatrix = outputData.get_data(outputData.get_headers())
        outputMatrix = np.vstack((np.matrix(outputData.get_headers()), np.matrix(outputData.get_raw_types()), outputMatrix))
        np.savetxt(filename, outputMatrix, delimiter=",", fmt="%s")

    def handleLinearRegression(self):

        if self.currentData is None:
            print("Error: no data loaded. Open a file first.")
            return

        # Create a list of headers the user can choose from to select their regression axes
        headers = self.currentData.get_headers()
        # Create a dialog box
        dialogBox = RegressionDialog(parent=self.root, headers=headers)
        # Grab the results
        try:
            selections = dialogBox.choices
        except:
            return

        # Terminate if the user didn't select an independent and dependent variable or pressed cancel
        if selections[0] is None or selections[1] is None:
            print("Error: improper selection of axes. Try again.")
            return

        self.resetView()
        self.buildLinearRegression(selections)

    # selections is a list where the first element is a list of strings of the column headers for the independent
    # variables, and the second element is a string of the column header for the dependent variable
    def buildLinearRegression(self, selections):

        self.currentAxes = []
        for ind in selections[0]:
            self.currentAxes.append(ind)
        self.currentAxes.append(selections[1])

        # Make a local copy of the VTM
        vtm = self.view.build()
        # Don't plot the points; that's done in buildPoints

        # Make a list of headers where the dependent variable will be plotted on the Y axis in index 1
        headers = [self.currentAxes[0]]
        headers.append(self.currentAxes[-1])
        numColumns = 2
        if self.currentAxes[1] != self.currentAxes[-1]:
            for header in self.currentAxes[1:-1]:
                headers.append(header)
                numColumns += 1

        # Make sure if there aren't 5 columns given that the rest are filled in with None so buildPoints works properly
        fillIn = 5 - len(headers)
        for i in range(fillIn):
            headers.append(None)
        if len(headers) > 5:
            headers = headers[:5]
        self.buildPoints(headers, self.currentData)

        # Calculate the linear regression of the independent and dependent variables
        b, sse, r2, t, p = \
            analysis.linear_regression(self.currentData, self.currentAxes[:-1], self.currentAxes[-1])
        # # Calculate the linear regression of the independent and dependent variables using the normal equation
        # bNE, sseNE, r2NE, tNE, pNE = \
        #     analysis.linear_regression_ne(self.currentData, self.currentAxes[:-1], self.currentAxes[-1])
        # # Calculate the linear regression of the independent and dependent variables using gradient descent
        # bGD, sseGD, r2GD, tGD, pGD = \
        #     analysis.linear_regression_gd(self.currentData, self.currentAxes[:-1], self.currentAxes[-1])
        # # Calculate the linear regression of the independent and dependent variables using a three-layer neural network
        # bNN, sseNN, r2NN, tNN, pNN = \
        #     analysis.linear_regression_nn(self.currentData, self.currentAxes[:-1], self.currentAxes[-1])
        m = b[:-1].copy()
        b = b[-1, 0].copy()
        r2 = r2
        print("m: ", m)
        print("b: ", b)
        print("R^2: ", r2)

        # Get the range and fit a regression line to the endpoints of the data in normalized data space
        dataRange = analysis.dataRange(self.currentAxes, self.currentData)

        y0Norm = ((dataRange[0][0] * m + b) - dataRange[-1][0]) / (dataRange[-1][1] - dataRange[-1][0])
        y1Norm = ((dataRange[0][1] * m + b) - dataRange[-1][0]) / (dataRange[-1][1] - dataRange[-1][0])
        print("dataRange:\n", dataRange)
        print("y0Norm:\n", y0Norm)
        print("y1Norm:\n", y1Norm)

        if len(self.currentAxes) == 2:
            # Adjust the above formulas when dealing with multiple linear regression
            self.regressionEndpoints = np.matrix([[0, y0Norm, 0, 1],
                                  [1, y1Norm, 0, 1]])
            self.viewRegressionEndpoints = (vtm * self.regressionEndpoints.T).T

            # Draw the points and the line on the canvas
            pt1 = self.canvas.create_oval(self.viewRegressionEndpoints[0, 0]-1,
                                         self.viewRegressionEndpoints[0, 1]-1,
                                         self.viewRegressionEndpoints[0, 0]+1,
                                         self.viewRegressionEndpoints[0, 1]+1,
                                         fill='red',
                                         outline='')
            pt2 = self.canvas.create_oval(self.viewRegressionEndpoints[1, 0]-1,
                                         self.viewRegressionEndpoints[1, 1]-1,
                                         self.viewRegressionEndpoints[1, 0]+1,
                                         self.viewRegressionEndpoints[1, 1]+1,
                                         fill='red',
                                         outline='')
            line = self.canvas.create_line(int(self.viewRegressionEndpoints[0, 0]),
                                           int(self.viewRegressionEndpoints[0, 1]),
                                           int(self.viewRegressionEndpoints[1, 0]),
                                           int(self.viewRegressionEndpoints[1, 1]),
                                           fill='red')

            # Store the points and line
            self.objects.append(pt1)
            self.objects.append(pt2)
            self.regressionLine = line

        # Add a text window that describes information about the regression line
        if m.shape[0] == 1:
            regressionInfo = "Regression info\n" + "\nSlope: " + ("%.3f" % m) + "\nY intercept: " + ("%.3f" % b) + \
                             "\nR: " + ("%.3f" % np.sqrt(r2)) + "\nR^2: " + ("%.3f" % r2)
        elif m.shape[0] == 2:
            regressionInfo = "Regression info\n" + "\nSlope 1: " + ("%.3f" % m[0]) + "\nSlope 2: " + ("%.3f" % m[1]) + \
                             "\nY intercept: " + ("%.3f" % b) + "\nR: " + ("%.3f" % np.sqrt(r2)) + \
                             "\nR^2: " + ("%.3f" % r2)
        else:
            regressionInfo = "Regression info\n" + "\nSlope 1: " + ("%.3f" % m[0]) + "\nSlope 2: " + ("%.3f" % m[1]) + \
                             "\nSlope 3: " + ("%.3f" % m[2]) + "\nY intercept: " + ("%.3f" % b) + "\nR: " + \
                             ("%.3f" % np.sqrt(r2)) + "\nR^2: " + ("%.3f" % r2)
        self.canvas.delete(self.regressionInfo)
        self.regressionInfo = self.canvas.create_text(590, 115, text=regressionInfo, anchor=tk.NE, justify=tk.CENTER)

    def updateFits(self):

        # Check if there is a regression line plotted on the canvas, if so update it
        if self.regressionEndpoints is None:
            return

        # Make a local copy of the VTM
        vtm = self.view.build()
        self.viewRegressionEndpoints = (vtm * self.regressionEndpoints.T).T

        # Update any points or canvas objects in self.objects that haven't already been updated
        # Assumes that endpoints are at positions -2 and -1, improve design?
        self.canvas.coords(self.objects[-2],
                           self.viewRegressionEndpoints[0, 0]-1,
                           self.viewRegressionEndpoints[0, 1]-1,
                           self.viewRegressionEndpoints[0, 0]+1,
                           self.viewRegressionEndpoints[0, 1]+1)
        self.canvas.coords(self.objects[-1],
                           self.viewRegressionEndpoints[1, 0]-1,
                           self.viewRegressionEndpoints[1, 1]-1,
                           self.viewRegressionEndpoints[1, 0]+1,
                           self.viewRegressionEndpoints[1, 1]+1)
        self.canvas.coords(self.regressionLine,
                           self.viewRegressionEndpoints[0, 0],
                           self.viewRegressionEndpoints[0, 1],
                           self.viewRegressionEndpoints[1, 0],
                           self.viewRegressionEndpoints[1, 1])

    def printData(self, event=None):

        try:
            # Connect numRows to a slider to allow the user to choose from the GUI how many rows to print?
            self.currentData.printData(numRows=20)
        except:
            print("No data")

    def handleQuit(self, event=None):

        print('Terminating')
        self.root.destroy()

    def clearData(self, event=None):

        for obj in self.objects:
            self.canvas.delete(obj)
        if self.regressionLine is not None:
            self.canvas.delete(self.regressionLine)
        self.objects = []
        self.points = np.matrix([[]])
        self.viewPoints = np.matrix([[]])
        self.regressionEndpoints = None
        self.viewRegressionEndpoints = None
        self.regressionLine = None
        if self.legend is not None:
            self.canvas.delete(self.legend)
        if self.regressionInfo is not None:
            self.canvas.delete(self.regressionInfo)

    def resetView(self, event=None):

        self.view.reset()
        self.clearData()
        for axis in self.axes:
            self.canvas.delete(axis)
        self.buildAxes()
        self.viewExtent = self.view.extent
        self.view.translationX = 0
        self.view.translationY = 0
        self.PCAData = {}
        self.PCAAxes = {}
        self.PCAEntries.delete(0, tk.END)

    def hotKeyXY(self, event=None):

        self.view.reset(extent=self.viewExtent)
        for axis in self.axes:
            self.canvas.delete(axis)
        self.buildAxes()
        self.view.rotateVRC(0, 0, 0)
        self.updateAxes()
        self.updatePoints()
        self.updateFits()

    def hotKeyXZ(self, event=None):

        self.view.reset(extent=self.viewExtent)
        for axis in self.axes:
            self.canvas.delete(axis)
        self.buildAxes()
        self.view.rotateVRC(3*math.pi/2, 0, 0)
        self.updateAxes()
        self.updatePoints()
        self.updateFits()

    def hotKeyYZ(self, event=None):

        self.view.reset(extent=self.viewExtent)
        for axis in self.axes:
            self.canvas.delete(axis)
        self.buildAxes()
        self.view.rotateVRC(0, 3*math.pi/2, 0)
        self.updateAxes()
        self.updatePoints()
        self.updateFits()

    def handleMouseButton1(self, event):

        self.baseClick1 = (event.x, event.y)

        # give the other base clicks values if they don't already have any
        if self.baseClick2 is None:
            self.baseClick2 = (event.x, event.y)
        if self.baseClick3 is None:
            self.baseClick3 = (event.x, event.y)
        if self.baseClick4 is None:
            self.baseClick4 = (event.x, event.y)

    def handleMouseButton2(self, event):

        self.baseClick2 = (event.x, event.y)

        # save a copy of the current view
        self.clone = self.view.clone()

        # give the other base clicks values if they don't already have any
        if self.baseClick1 is None:
            self.baseClick1 = (event.x, event.y)
        if self.baseClick3 is None:
            self.baseClick3 = (event.x, event.y)
        if self.baseClick4 is None:
            self.baseClick4 = (event.x, event.y)

    def handleMouseButton3(self, event):

        self.baseClick3 = (event.x, event.y)

        # save a copy of the current view
        clone = self.view.clone()
        self.viewExtent = clone.extent

        # give the other base clicks values if they don't already have any
        if self.baseClick1 is None:
            self.baseClick1 = (event.x, event.y)
        if self.baseClick2 is None:
            self.baseClick2 = (event.x, event.y)
        if self.baseClick4 is None:
            self.baseClick4 = (event.x, event.y)

    def handleMouseButton4(self, event):

        # place in that spot a randomly colored circle with radius dx
        self.baseClick4 = (event.x, event.y)

        # save a copy of the current view
        self.clone = self.view.clone()

        # give the other base clicks values if they don't already have any
        if self.baseClick1 is None:
            self.baseClick1 = (event.x, event.y)
        if self.baseClick2 is None:
            self.baseClick2 = (event.x, event.y)
        if self.baseClick3 is None:
            self.baseClick3 = (event.x, event.y)

    # A point is deleted when the user hits shift-command-click on top of one
    def handleShiftCommandMouseButton1(self, event):

        self.baseClick1 = (event.x, event.y)
        # print("Shift-Command-Button-1 pressed")
        # This may be computationally inefficient - recode if slow
        for obj in self.objects:
            loc = self.canvas.coords(obj)
            if loc[0] <= self.baseClick1[0]\
                    and loc[1] <= self.baseClick1[1]\
                    and self.baseClick1[0] <= loc[2]\
                    and self.baseClick1[1] <= loc[3]:
                self.canvas.delete(obj)
                self.objects.remove(obj)
                print("data point removed")

    # This is called if the first mouse button is being moved
    def handleMouseButton1Motion(self, event):

        # calculate the difference
        diff = (event.x - self.baseClick1[0], event.y - self.baseClick1[1])
        self.view.translationX += diff[0]
        self.view.translationY += diff[1]

        # divide the differential motion (dx, dy) by the screen size (view X, view Y)
        motion = (float(diff[0]) / self.view.screen[0], float(diff[1]) / self.view.screen[1])

        # multiply the horizontal and vertical motion by the horizontal and vertical extents
        translationMultiplierX = 1
        translationMultiplierY = 1
        delta0 = motion[0] * self.view.extent[0] * translationMultiplierX
        delta1 = motion[1] * self.view.extent[1] * translationMultiplierY

        # update VRP
        self.view.vrp = self.view.vrp + (delta0 * self.view.u) + (delta1 * self.view.vup)
        self.updateAxes()
        self.updatePoints()
        self.updateFits()

        # update base click
        self.baseClick1 = (event.x, event.y)

    # This is called if the second mouse button is being moved
    # Extension: find a way to use another button to implement rotation about the z axis
    def handleMouseButton2Motion(self, event):

        # calculate the difference
        diff = (event.x - self.baseClick2[0], event.y - self.baseClick2[1])

        # divide the differential motion (dx, dy) by the screen size (view X, view Y)
        motion = (diff[0] / self.view.screen[0], diff[1] / self.view.screen[1])

        # translate the horizontal and vertical motion into angular adjustments
        rotationMultiplierX = 1
        rotationMultiplierY = 1
        deltaX = float(motion[0] * math.pi * rotationMultiplierX) / 2
        deltaY = float(-motion[1] * math.pi * rotationMultiplierY) / 2
        deltaZ = 0

        # clone the view from when button 2 was clicked, run the rotation pipeline, and update the axes
        self.view = self.clone.clone()
        self.view.rotateVRC(deltaY, deltaX, deltaZ)
        self.updateAxes()
        self.updatePoints()
        self.updateFits()

    # This is called if the first mouse button is being moved while the command key is held down
    # Possible extension: build scaling such that the point of zoom is the location of button 3 click
    def handleMouseButton3Motion(self, event):

        # calculate the difference
        diff = (event.x - self.baseClick3[0], event.y - self.baseClick3[1])

        # capture a scale factor to multiply the extent attribute by
        scaleFactor = -diff[1]/100 + 1
        if scaleFactor < 0.1: scaleFactor = 0.1
        if scaleFactor > 3.0: scaleFactor = 3.0

        # adjust the extent and update the axes
        self.view.extent = self.viewExtent / scaleFactor
        self.updateAxes()
        self.updatePoints()
        self.updateFits()

    # This is called if the second mouse button is being moved while the command key is held down
    def handleMouseButton4Motion(self, event):

        # calculate the difference
        diff = (event.x - self.baseClick4[0], event.y - self.baseClick4[1])

        # divide the differential motion (dx, dy) by the screen size (view X, view Y)
        motion = diff[1] / self.view.screen[1]

        # translate the horizontal and vertical motion into angular adjustments
        rotationMultiplierZ = 1
        deltaX = 0
        deltaY = 0
        deltaZ = float(-motion * math.pi * rotationMultiplierZ) / 2

        # clone the view from when button 2 was clicked, run the rotation pipeline, and update the axes
        self.view = self.clone.clone()
        self.view.rotateVRC(deltaX, deltaY, deltaZ)
        self.updateAxes()
        self.updatePoints()
        self.updateFits()

    def main(self):

        # print('Entering main loop')
        self.root.mainloop()



class Dialog(tk.Toplevel):

    def __init__(self, parent, headers, title=None):

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)
        self.headers = headers

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):

        # create dialog body. Return widget that should have
        # initial focus. This method should be overridden
        pass

    def buttonbox(self):

        # add standard button box. Override if you don't want the
        # standard buttons
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):
        pass

    def apply(self):
        pass



class PlotDialog(Dialog):

    def __init__(self, parent, headers):

        Dialog.__init__(self, parent, headers)
        self.xChoice = None
        self.yChoice = None
        self.zChoice = None
        self.colorChoice = None
        self.sizeChoice = None

    def body(self, master):

        xLab = tk.Label(master, text='X axis')
        xLab.pack(side=tk.LEFT)
        self.selectX = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
        self.selectX.pack(side=tk.LEFT)
        yLab = tk.Label(master, text='Y axis')
        yLab.pack(side=tk.LEFT)
        self.selectY = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
        self.selectY.pack(side=tk.LEFT)
        zLab = tk.Label(master, text='Z axis\n(optional)')
        zLab.pack(side=tk.LEFT)
        self.selectZ = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
        self.selectZ.pack(side=tk.LEFT)
        colorLab = tk.Label(master, text='Color\n(optional)')
        colorLab.pack(side=tk.LEFT)
        self.selectColor = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
        self.selectColor.pack(side=tk.LEFT)
        sizeLab = tk.Label(master, text='Size\n(optional)')
        sizeLab.pack(side=tk.LEFT)
        self.selectSize = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
        self.selectSize.pack(side=tk.LEFT)
        for i in range(len(self.headers)):
            self.selectX.insert(tk.END, self.headers[i])
            self.selectY.insert(tk.END, self.headers[i])
            self.selectZ.insert(tk.END, self.headers[i])
            self.selectColor.insert(tk.END, self.headers[i])
            self.selectSize.insert(tk.END, self.headers[i])

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        # grab last values selected
        try:
            self.xChoice = self.headers[self.selectX.curselection()[0]]
        except:
            self.xChoice = None

        try:
            self.yChoice = self.headers[self.selectY.curselection()[0]]
        except:
            self.yChoice = None

        try:
            self.zChoice = self.headers[self.selectZ.curselection()[0]]
        except:
            self.zChoice = None

        try:
            self.colorChoice = self.headers[self.selectColor.curselection()[0]]
        except:
            self.colorChoice = None

        try:
            self.sizeChoice = self.headers[self.selectSize.curselection()[0]]
        except:
            self.sizeChoice = None

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def validate(self):
        # change?
        return True

    def apply(self):

        self.choices = [self.xChoice, self.yChoice, self.zChoice, self.colorChoice, self.sizeChoice]
        return self.choices  # overridden



class RegressionDialog(Dialog):

    def __init__(self, parent, headers):

        Dialog.__init__(self, parent, headers)
        self.indepChoice = None
        self.depChoice = None

    def body(self, master):

        xLab = tk.Label(master, text='Independent variable')
        xLab.pack(side=tk.TOP)
        self.selectIndep = tk.Listbox(master, selectmode=tk.MULTIPLE, exportselection=0)
        self.selectIndep.pack(side=tk.TOP)
        yLab = tk.Label(master, text='Dependent variable')
        yLab.pack(side=tk.TOP)
        self.selectDep = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
        self.selectDep.pack(side=tk.TOP)
        for i in range(len(self.headers)):
            self.selectIndep.insert(tk.END, self.headers[i])
            self.selectDep.insert(tk.END, self.headers[i])

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        # grab last values selected
        try:
            self.indepChoice = []
            for i in range(len(self.selectIndep.curselection())):
                choice = self.selectIndep.curselection()[i]
                self.indepChoice.append(self.headers[choice])
        except:
            self.indepChoice = None

        try:
            self.depChoice = self.headers[self.selectDep.curselection()[0]]
        except:
            self.depChoice = None

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def validate(self):
        # change?
        return True

    def apply(self):

        self.choices = [self.indepChoice, self.depChoice]
        return self.choices  # overridden



class PCADialog(Dialog):

    def __init__(self, parent, headers):

        Dialog.__init__(self, parent, headers)
        self.axesChoice = None

    def body(self, master):

        axisLabel = tk.Label(master, text='Select axes')
        axisLabel.pack(side=tk.TOP)
        self.selectAxes = tk.Listbox(master, selectmode=tk.MULTIPLE, exportselection=0)
        self.selectAxes.pack(side=tk.TOP)
        for i in range(len(self.headers)):
            self.selectAxes.insert(tk.END, self.headers[i])
        entryLabel = tk.Label(master, text='Save as:')
        entryLabel.pack(side=tk.LEFT)
        self.title = tk.Entry(master)
        self.title.pack(side=tk.LEFT)

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        # grab last values selected
        try:
            self.axesChoice = []
            for i in range(len(self.selectAxes.curselection())):
                choice = self.selectAxes.curselection()[i]
                self.axesChoice.append(self.headers[choice])
            self.titleChoice = self.title.get()
        except:
            self.axesChoice = None
            self.titleChoice = None

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def validate(self):
        # change?
        return True

    def apply(self):

        self.choices = self.axesChoice
        return self.choices, self.titleChoice  # overridden



class ClusterDialog(Dialog):

    def __init__(self, parent, headers, PCAChoices):

        Dialog.__init__(self, parent, headers)
        self.axesChoice = None
        self.PCAChoices = PCAChoices

    def body(self, master):

        axisLabel = tk.Label(master, text='Select axes')
        axisLabel.pack(side=tk.TOP)
        self.selectAxes = tk.Listbox(master, selectmode=tk.MULTIPLE, exportselection=0)
        self.selectAxes.pack(side=tk.TOP)
        for i in range(len(self.headers)):
            self.selectAxes.insert(tk.END, self.headers[i])
        entryLabel = tk.Label(master, text='Number of clusters:')
        entryLabel.pack(side=tk.TOP)
        self.k = tk.Entry(master)
        self.k.pack(side=tk.TOP)
        PCALabel = tk.Label(master, text='Choose PCA data to cluster. No selection defaults to current data.')
        PCALabel.pack(side=tk.TOP)
        self.selectPCAData = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
        self.selectPCAData.pack(side=tk.TOP)
        # for i in range(len(self.PCAChoices)):
        #     self.selectPCAData.insert(tk.END, self.PCAChoices[i])

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        # grab last values selected
        try:
            self.axesChoice = []
            for i in range(len(self.selectAxes.curselection())):
                choice = self.selectAxes.curselection()[i]
                self.axesChoice.append(self.headers[choice])
            try:
                self.PCADataChoice = self.PCAChoices[self.selectPCAData.curselection()[0]]
            except:
                self.PCADataChoice = []
            self.kChoice = self.k.get()
        except:
            self.axesChoice = None
            self.PCADataChoice = None
            self.kChoice = None

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def validate(self):
        # change?
        return True

    def apply(self):

        self.choices = self.axesChoice
        return self.choices, self.PCADataChoice, self.kChoice  # overridden



if __name__ == "__main__":
    dapp = DisplayApp(800, 600)
    dapp.main()