import numpy as np
from graphics import Arrowimg
import os

class Model():
    '''
    This class contains all physics.
    It sets start values for physical quantities and contains calculations
    that are called upon every frame. It needs the time and timesteps as inputs,
    they are not regulated within this class. (See sim.py, the main program.)
    '''    
    def __init__(self, b0set, b1set, f1set, m, n, xmax, ymax, tissuefile, gui):
        # Array size
        self.m,self.n = m,n

        # Adjustable values
        self.b0mag, self.b1mag, self.b1freq = b0set, b1set, f1set
        self.kdamper = 0.6

        # Pixel distance between compass arrows
        xdist = xmax / (self.m + 1)
        ydist = ymax / (self.n + 2)

        # + 1 because the centers are half distance from borders on each side
        # Arrays with the x and y pixel positions of the compass arrows
        xposarr = np.arange(xdist, xmax, xdist)
        yposarr = np.arange(2.0 * ydist, ymax, ydist)

        # Setting up the arrows
        # Saving them in a 2D list so using the physics arrays will be easier
        self.arrowlist = []
        for i in range(m):
            self.arrowlist.append([])
            for j in range(n):
                self.arrowlist[i].append(Arrowimg(xposarr[i], yposarr[j], gui.imglist))

        # Simulating tissue in the grid
        self.readtissue(tissuefile)

        # Starting the magnetic field arrays
        # Optional x gradient and y gradient to build magnetic fields on
        self.b0gradient, self.b1gradient = np.zeros([m, n]), np.zeros([m, n])
        for i in range(m):
            self.b0gradient[i, :] = np.linspace(.1, 1, n)
        for j in range(n):
            self.b1gradient[:, j] = np.linspace(.1, 1, m)

        # For realism, not every compass arrow is exactly identical, so add noise
        # Use gradient factor for noise
        self.noise = 0.03
        self.b0gradient = 1 + self.noise * (np.random.rand(m, n) - 0.5)
        self.b1gradient = 1 + 0 * self.b1gradient

        # Start with B0 and B1 oon
        self.b0on = True
        self.b1on = True

        # Set up physics variables
        # Angles and angular velocities
        theta0 = 180.
        self.theta, self.v = np.ones([m, n]) * theta0, np.zeros([m, n])

    def readtissue(self,tissuefile):
        '''
        Imports the file containing the properties of compasses
        by their coordinates, to simulate different tissues, and "image" them.
        '''
        # Read tissue file or set to one
        if tissuefile == "":
            self.tissuemask = np.ones([self.m, self.n])
        else:
            # Check for .csv or .tis extension, if not add ".tis"
            filename = os.path.join("data",tissuefile)
            if not (".tis" in filename) and \
               not (".csv" in filename):
                filename += ".tis"

            # Read lines from tissuefile
            f = open(filename,"r")
            lines= f.readlines()
            f.close()
            print("Reading "+filename)
            
            # Read tissue data from lines from tissue CSV file
            # Use list for appending
            tissuelist = []
            for line in lines:
                if line.strip()[0]=="#":
                    continue # Comment line skip to next
                else:
                    row = []
                    columns = line.split(",")
                    for col in columns:
                        row.append(float(col))

                # Add row of data
                tissuelist.append(row)

            # Convert list to numpy array
            # Row,column  = x,y so transpose data from file
            self.tissuemask = np.array(tissuelist).T
        

        #if tissuesimulation:
        #    tissuemask[int(m / 3):2 * int(m / 3), int(n / 3):2 * int(n / 3)] = .1
        #    # This picks one or a few center arrows to experience a lot less force
        #    print("Simulated tissue:", tissuemask)


    def force(self, bx, by, theta):
        # Force function
        '''
        Takes in 3 arrays B0, B1 and the angles of the arrows.
        Returns the torque on each.
        '''
        # arctan2 is the inverse tangent that can automatically deal
        # with any quadrant
        forcerad = np.arctan2(by, bx)
        forcemag = np.sqrt(bx ** 2 + by ** 2)

        # theta was in degrees, we work with radians for numpy sine
        thetarad = theta / 360 * 2 * np.pi
        # angle between the spin (thetarad) and the force
        anglediff = thetarad - forcerad
        # doesn't have to be smallest angle, or any specific domain
        # since it will go into a sine function

        # possible to add extra factors here
        force = forcemag * np.sin(anglediff)
        return force

    def update(self, tsim, dt):
        '''
        Time integration from acceleration, to velocity, to theta.
        '''
        # Model update function
        if dt > 0.:
            # Update magnetic field arrays, separate for x and y (B0 and B1)
            self.b0 = self.b0mag * self.b0gradient
            self.b1 = self.b1mag * np.cos(2 * np.pi * self.b1freq * tsim) * self.b1gradient
            a = self.tissuemask * self.force(self.b0on * self.b0, self.b1on * self.b1, self.theta)\
                   - self.kdamper * self.v

            # can add a factor here if necessary to simulate MoI

            self.v = self.v + a * dt
            self.theta = self.theta + self.v * dt

            # Now all array calculations are done
            # We have to switch to loops/lists for graphics

            # Set all arrows from arrowlist to their new angle
            for i in range(self.m):
                for j in range(self.n):
                    # Update the arrow for this iteration
                    # Slicing looks different because arrowlist a nested list
                    self.arrowlist[i][j].update(self.theta[i, j])



