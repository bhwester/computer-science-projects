# __Author__: 'Brian Westerman'
# __Date__: 2/15/16
# __File__: Display.py

import tkinter as tk
import tkinter.font as tkf
import numpy as np
import math
import random

# Create a class to build and manage the display
class DisplayApp:

    def __init__(self, width, height):

        # create a tk object, which is the root window
        self.root = tk.Tk()

        # width and height of the window
        self.initDx = width
        self.initDy = height

        # set up the geometry for the window
        self.root.geometry("%dx%d+50+30" % (self.initDx, self.initDy))

        # set the title of the window
        self.root.title("Data analysis and visualization")

        # set the maximum size of the window for resizing
        self.root.maxsize(1600, 900)

        # set up some constants for configuring the window


        # setup the menus
        self.buildMenus()

        # build the controls
        self.buildControls()

        # build the Canvas
        self.buildCanvas()

        # bring the window to the front
        self.root.lift()

        # - do idle events here to get actual canvas size
        self.root.update_idletasks()

        # now we can ask the size of the canvas
        print(self.canvas.winfo_geometry())

        # set up the key bindings
        self.setBindings()

        # set up the application state
        self.objects = [] # list of data objects that will be drawn in the canvas
        self.data = None # will hold the raw data someday.
        self.baseClick1 = None # used to keep track of mouse movement 1
        self.baseClick2 = None # used to keep track of mouse movement 2
        self.baseClick3 = None # used to keep track of mouse movement 3
        self.baseClick4 = None # used to keep track of mouse movement 4
        self.numDataPoints = 100
        self.origScale = 1
        # capture whether the x and y data distribution are uniform or gaussian
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
        menutext = [['-', '-', 'Quit  \xE2\x8C\x98-Q', 'Clear data  \xE2\x8C\x98-N'],
                     ['Command  1', '-', '-']]

        # menu callback functions (note that some are left blank,
        # so that you can add functions there if you want).
        # the first sublist is the set of callback functions for the file menu
        # the second sublist is the set of callback functions for the option menu
        menucmd = [[None, None, self.handleQuit, self.clearData],
                    [self.handleMenuCmd1, None, None]]

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
        rightControlFrame = tk.Frame(self.root)
        rightControlFrame.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

        # use a label to set the size of the right panel
        label = tk.Label(rightControlFrame, text="Control Panel", width=20)
        label.pack(side=tk.TOP, pady=10)

        # make a separator frame
        sep = tk.Frame(self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN)
        sep.pack(side=tk.RIGHT, padx = 2, pady = 2, fill=tk.Y)

        # make a menubutton
        self.colorOption = tk.StringVar(self.root)
        self.colorOption.set("black")
        colorMenu = tk.OptionMenu(rightControlFrame, self.colorOption,
                                        "black", "blue", "red", "green") # can add a command to the menu
        colorMenu.pack(side=tk.TOP, pady=5)

        # make a button in the frame
        # and tell it to call the handleButton method when it is pressed.
        colorUpdateButton = tk.Button(rightControlFrame, text="Update color",
                               command=self.handleColorUpdateButton)
        colorUpdateButton.pack(side=tk.TOP, pady=5)  # default side is top

        # make a button that allows the user to select the type of distribution
        selectDataDistributionButton = tk.Button(rightControlFrame, text="Select data distribution",
                                    command=self.selectDataDistribution)
        selectDataDistributionButton.pack(side=tk.TOP, pady=5)

        # make a button that generates random data points
        createRandomDataPointsButton = tk.Button(rightControlFrame, text="Create random data points",
                                                 command=self.createRandomDataPoints)
        createRandomDataPointsButton.pack(side=tk.TOP, pady=5)

        # make a button that clears the data
        clearDataButton = tk.Button(rightControlFrame, text="Clear data",
                                    command=self.clearData)
        clearDataButton.pack(side=tk.TOP, pady=5)

        # EXTENSION
        self.slider = tk.Scale(rightControlFrame, command=self.changeNumDataPoints, orient=tk.HORIZONTAL)
        self.slider.pack(side=tk.TOP, pady=5)

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
        self.canvas.bind('<Command-Button-1>', self.handleMouseButton3)
        self.canvas.bind('<Command-Button-2>', self.handleMouseButton3)
        self.canvas.bind('<Shift-Command-Button-1>', self.handleShiftCommandMouseButton1)
        self.canvas.bind('<B1-Motion>', self.handleMouseButton1Motion)
        self.canvas.bind('<B2-Motion>', self.handleMouseButton2Motion)
        self.canvas.bind('<Command-B1-Motion>', self.handleMouseButton2Motion)
        self.canvas.bind('<Command-B2-Motion>', self.handleMouseButton2Motion)

        # bind command sequences to the root window
        self.root.bind('<Command-q>', self.handleQuit)
        self.root.bind('<Command-n>', self.clearData)

    def selectDataDistribution(self, event=None):
        selections = self.dialogBox()
        self.xDistribution = selections[0]
        self.yDistribution = selections[1]

    def dialogBox(self):
        dialogBox = ListDialog(self.root)
        return dialogBox.apply()

    # EXTENSION
    def changeNumDataPoints(self, event=None):
        self.numDataPoints = self.slider.get()

    def createRandomDataPoints(self, event=None):
        # would be nice to be able to customize how big they appear
        dx = 3

        for i in range(self.numDataPoints):

            if self.xDistribution == 0:
                x = random.randint(0, self.initDx)
            elif self.xDistribution == 1:
                x = np.random.normal(loc=self.initDx/2, scale=int(self.initDy/3.5))
            else:
                x = random.randint(0, self.initDx)

            if self.yDistribution == 0:
                y = random.randint(0, self.initDy)
            elif self.yDistribution == 1:
                y = np.random.normal(loc=self.initDy/2, scale=int(self.initDy/3.5))
            else:
                y = random.randint(0, self.initDy)

            pt = self.canvas.create_oval(x-dx, y-dx, x+dx, y+dx, fill=self.colorOption.get(), outline='')
            self.objects.append(pt)

        print("Random data points created")

    def clearData(self, event=None):
        for obj in self.objects:
            self.canvas.delete(obj)
        self.objects = []
        print("All data points cleared")

    def handleQuit(self, event=None):
        print('Terminating')
        self.root.destroy()

    def handleColorUpdateButton(self):
        for obj in self.objects:
            self.canvas.itemconfig(obj, fill=self.colorOption.get())
        print('handling command button: ', self.colorOption.get())

    def handleMenuCmd1(self):
        print('handling menu command 1')

    def handleMouseButton1(self, event):
        self.baseClick1 = (event.x, event.y)
        print('handle mouse button 1: %d %d' % (event.x, event.y))

    def handleMouseButton2(self, event):
        self.baseClick2 = (event.x, event.y)
        loc = self.canvas.coords(self.objects[0])
        self.origScale = (loc[2] - loc[0]) / 2
        if self.origScale == 0:
            self.origScale = 1
        print("self.origScale: ", self.origScale)
        print('handle mouse button 2: %d %d' % (event.x, event.y))

    def handleMouseButton3(self, event):
        self.baseClick3 = (event.x, event.y)
        dx = 3
        rgb = "#%02x%02x%02x" % (random.randint(0, 255),
                                 random.randint(0, 255),
                                 random.randint(0, 255))
        oval = self.canvas.create_oval(event.x - dx,
                                       event.y - dx,
                                       event.x + dx,
                                       event.y + dx,
                                       fill = rgb,
                                       outline='')
        self.objects.append(oval)
        print('handle mouse button 3: %d %d' % (event.x, event.y))

    # EXTENSION
    def handleShiftCommandMouseButton1(self, event):
        self.baseClick4 = (event.x, event.y)
        print("Shift-Command-Button-1 pressed")
        # This may be computationally inefficient - recode if slow
        for obj in self.objects:
            loc = self.canvas.coords(obj)
            if loc[0] <= self.baseClick4[0]\
                    and loc[1] <= self.baseClick4[1]\
                    and self.baseClick4[0] <= loc[2]\
                    and self.baseClick4[1] <= loc[3]:
                self.canvas.delete(obj)
                self.objects.remove(obj)
                print("data point removed")

    # This is called if the first mouse button is being moved
    def handleMouseButton1Motion(self, event):
        # calculate the difference
        diff = (event.x - self.baseClick1[0], event.y - self.baseClick1[1])

        # update base click
        self.baseClick1 = (event.x, event.y)
        print('handle button 1 motion %d %d' % (diff[0], diff[1]))

        for obj in self.objects:
            loc = self.canvas.coords(obj)
            # only applies for objects with 4 coordinates - consider adjusting for objects with other than 4 coordinates
            self.canvas.coords(obj,
                               loc[0] + diff[0],
                               loc[1] + diff[1],
                               loc[2] + diff[0],
                               loc[3] + diff[1])

    # This is called if the second button of a real mouse has been pressed
    # and the mouse is moving. Or if the control key is held down while
    # a person moves their finger on the track pad.
    # EXTENSION
    def handleMouseButton2Motion(self, event):
        # calculate the difference
        diff = (event.x - self.baseClick2[0], event.y - self.baseClick2[1])

        # update base click
        #self.baseClick2 = (event.x, event.y)

        dx = -diff[1]/10 + 1
        print("dx: ", dx)
        for obj in self.objects:
            loc = self.canvas.coords(obj)
            midpoint = (((loc[0] + loc[2]) / 2), ((loc[1] + loc[3]) / 2))
            # only applies for objects with 4 coordinates - consider adjusting for objects with other than 4 coordinates
            self.canvas.coords(obj,
                               midpoint[0] - self.origScale * dx if dx > 0 else midpoint[0],
                               midpoint[1] - self.origScale * dx if dx > 0 else midpoint[1],
                               midpoint[0] + self.origScale * dx if dx > 0 else midpoint[0],
                               midpoint[1] + self.origScale * dx if dx > 0 else midpoint[1])

        print('handle button 2 motion')

    def main(self):
        print('Entering main loop')
        self.root.mainloop()



class Dialog(tk.Toplevel):

    def __init__(self, parent, title=None):

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

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
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
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



class ListDialog(Dialog):

    def __init__(self, parent):
        Dialog.__init__(self, parent)
        self.options = None

    def body(self, master):
        xLab = tk.Label(master, text='X choice')
        xLab.pack(side=tk.TOP)
        self.selectX = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
        self.selectX.pack(side=tk.TOP)
        yLab = tk.Label(master, text='Y choice')
        yLab.pack(side=tk.TOP)
        self.selectY = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
        self.selectY.pack(side=tk.TOP)
        self.options = ['Uniform', 'Gaussian']
        self.selectX.insert(tk.ACTIVE, self.options[0], self.options[1])
        self.selectY.insert(tk.ACTIVE, self.options[0], self.options[1])

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        # grab last values selected
        try:
            self.xChoice = self.selectX.curselection()[0]
        except:
            self.xChoice = None

        try:
            self.yChoice = self.selectY.curselection()[0]
        except:
            self.yChoice = None

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def validate(self):
        # change?
        return 1

    def apply(self):

        return [self.xChoice, self.yChoice] # overridden



if __name__ == "__main__":
    dapp = DisplayApp(800, 500)
    dapp.main()
