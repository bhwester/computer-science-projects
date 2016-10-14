# __Author__: 'Brian Westerman'
# __Date__: 2/15/16
# __File__: view.py

import numpy as np

class View:

    # constructor
    def __init__(self):

        # automatically resets the view
        self.reset()

    def reset(self,
              vrp=np.matrix([0.5, 0.5, 1]),
              vpn=np.matrix([0, 0, -1]),
              vup=np.matrix([0, 1, 0]),
              u=np.matrix([-1, 0, 0]),
              extent=np.array([1, 1, 1]),
              screen=np.array([400, 400]),
              offset=np.array([20, 20])):

        # initializes default values
        self.vrp = vrp
        self.vpn = vpn
        self.vup = vup
        self.u = u
        self.extent = extent
        self.screen = screen
        self.offset = offset
        self.translationX = 0
        self.translationY = 0

    def build(self):

        # Generate a 4x4 identity matrix, which will be the basis for the view matrix
        vtm = np.identity(4, dtype=float)

        # Generate a translation matrix to move the VRP to the origin and then premultiply the vtm by the translation matrix
        t1 = np.matrix([[1, 0, 0, -self.vrp[0, 0]],
                        [0, 1, 0, -self.vrp[0, 1]],
                        [0, 0, 1, -self.vrp[0, 2]],
                        [0, 0, 0, 1]])
        vtm = t1 * vtm

        # Calculate the view reference axes tu, tvup, tvpn
        # tu is the cross product (np.cross) of the vup and vpn vectors
        tu = np.cross(self.vup, self.vpn)
        # tvup is the cross product of the vpn and tu vectors
        tvup = np.cross(self.vpn, tu)
        # tvpn is a copy of the vpn vector
        tvpn = self.vpn

        # Normalize the view axes tu, tvup, and tvpn to unit length
        # du, dv, and dz are all a part of the normalization process, make explicit?
        # Bruce's edits: (didn't work, caused an error, and rotation/translation/scaling still work fine for axes and data)
        # tu /= np.linalg.norm(tu)
        # tvup /= np.linalg.norm(tvup)
        # tvpn /= np.linalg.norm(tvpn)
        np.linalg.norm(tu)
        np.linalg.norm(tvup)
        np.linalg.norm(tvpn)

        # Copy the orthonormal axes tu, tvup, and tvpn back to self.u, self.vup and self.vpn
        self.u = tu
        self.vup = tvup
        self.vpn = tvpn

        # align the axes
        r1 = np.matrix([[tu[0,0], tu[0, 1], tu[0, 2], 0.0],
                        [tvup[0, 0], tvup[0, 1], tvup[0, 2], 0.0],
                        [tvpn[0, 0], tvpn[0, 1], tvpn[0, 2], 0.0],
                        [0.0, 0.0, 0.0, 1.0]])
        vtm = r1 * vtm

        # Perspective view transformation goes here
        #p = np.matrix([[1, 0, 0, 0],
        #               [0, 1, 0, 0],
        #               [0, 0, 1, 0],
        #               [0, 0, 1/d, 0]])
        #p = p ####

        # Translate the lower left corner of the view space to the origin. Since the axes are aligned, this is just a
        # translation by half the extent of the view volume in the X and Y view axes
        t2 = np.matrix([[1, 0, 0, 0.5*self.extent[0]],
                        [0, 1, 0, 0.5*self.extent[1]],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])
        vtm = t2 * vtm

        # Use the extent and screen size values to scale to the screen
        s1 = np.matrix([[-self.screen[0]/self.extent[0], 0, 0, 0],
                       [0, -self.screen[1]/self.extent[1], 0, 0],
                       [0, 0, 1.0/self.extent[2], 0],
                       [0, 0, 0, 1]])
        vtm = s1 * vtm

        # Translate the lower left corner to the origin and add the view offset, which gives a little buffer around the
        # top and left edges of the window
        t3 = np.matrix([[1, 0, 0, self.screen[0]+self.offset[0]],
                        [0, 1, 0, self.screen[1]+self.offset[1]],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])
        vtm = t3 * vtm

        return vtm

    def clone(self):

        # make a new View object
        clone = View()

        # copy all fields of the current View object to the new View object
        clone.vrp = np.copy(self.vrp)
        clone.vpn = np.copy(self.vpn)
        clone.vup = np.copy(self.vup)
        clone.u = np.copy(self.u)
        clone.extent = np.copy(self.extent)
        clone.screen = np.copy(self.screen)
        clone.offset = np.copy(self.offset)
        clone.translationX = self.translationX
        clone.translationY = self.translationY

        return clone

    def rotateVRC(self, thetaU, thetaVUP, thetaVPN):

        # translate the center of rotation (the middle of the extent volume) to the origin, rotate around the Y axis,
        # rotate around the X axis, then translate back by the opposite of the first translation
        tvrc = np.matrix([[self.vrp[0, 0], self.vrp[0, 1], self.vrp[0, 2], 1],
                          [self.u[0, 0], self.u[0, 1], self.u[0, 2], 0],
                          [self.vup[0, 0], self.vup[0, 1], self.vup[0, 2], 0],
                          [self.vpn[0, 0], self.vpn[0, 1], self.vpn[0, 2], 0]])
        point = np.matrix(self.vrp + self.vpn * self.extent[2] * 0.5)

        t1 = np.matrix([[1, 0, 0, -point[0, 0]],
                        [0, 1, 0, -point[0, 1]],
                        [0, 0, 1, -point[0, 2]],
                        [0, 0, 0, 1]])
        Rxyz = np.matrix([[self.u[0,0], self.u[0, 1], self.u[0, 2], 0.0],
                        [self.vup[0, 0], self.vup[0, 1], self.vup[0, 2], 0.0],
                        [self.vpn[0, 0], self.vpn[0, 1], self.vpn[0, 2], 0.0],
                        [0.0, 0.0, 0.0, 1.0]])
        r1 = np.matrix([[1, 0, 0, 0],
                        [0, np.cos(thetaU), -np.sin(thetaU), 0],
                        [0, np.sin(thetaU), np.cos(thetaU), 0],
                        [0, 0, 0, 1]])
        r2 = np.matrix([[np.cos(thetaVUP), 0, np.sin(thetaVUP), 0],
                        [0, 1, 0, 0],
                        [-np.sin(thetaVUP), 0, np.cos(thetaVUP), 0],
                        [0, 0, 0, 1]])
        r3 = np.matrix([[np.cos(thetaVPN), -np.sin(thetaVPN), 0, 0],
                       [np.sin(thetaVPN), np.cos(thetaVPN), 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])
        t2 = np.matrix([[1, 0, 0, point[0, 0]],
                        [0, 1, 0, point[0, 1]],
                        [0, 0, 1, point[0, 2]],
                        [0, 0, 0, 1]])

        tvrc = (t2 * Rxyz.T * r3 * r2 * r1 * Rxyz * t1 * tvrc.T).T

        # Copy values from tvrc back into VRP, U, VUP, and VPN
        self.vrp = tvrc[0, 0:3]
        self.u = tvrc[1, 0:3]
        self.vup = tvrc[2, 0:3]
        self.vpn = tvrc[3, 0:3]

        # Normalize U, VUP, and VPN
        np.linalg.norm(self.u)
        np.linalg.norm(self.vup)
        np.linalg.norm(self.vpn)