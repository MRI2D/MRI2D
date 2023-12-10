import numpy as np
import matplotlib.pyplot as plt

# Show plot at end of program to help in finding reso frequency

class Plotter():
    '''
    Handles everything necessary to create graphs after the simulation is done,
    to allow proper analysis.
    Tracks and later displays B0 magnitude, B1 freq, and theta through time.
    B1 magnitude isn't tracked, since its only requirement for finding the
    resonance frequency is being strong enough, not a specific value.
    '''
    def __init__(self,tsim,dtplot):
        # Store starting time for plotting timer
        self.dtplot = dtplot
        self.tplot = tsim

        # Tabular data for plotting and timing
        self.thetatab = []
        self.b0tab = []
        self.f1tab = []
        self.timetab = []
        self.devtab = []
        self.treset = []

    def tableupdate(self,tsim,b0mag,theta,b1freq):
        '''
        Adds a new data point in each plot if the time since last update is
        longer than dtplot, the time steps of the plots. Saving data on every
        tick would be a waste of storage.
        '''
        # Check whether it is time to store an update values to tables for plotting
        if tsim - self.tplot > self.dtplot:
            # Plotting timer
            self.tplot = tsim

            # Plot data
            self.timetab.append(tsim)
            self.b0tab.append(b0mag)

            # reshape theta into one long 1D array for plotting
            m,n = theta.shape
            allthetas = theta.reshape(m * n)

            self.thetatab.append(np.mod(allthetas,360))
            self.devtab.append(np.std(allthetas))
            self.f1tab.append(b1freq)

    def tabletreset(self,tsim):
        '''Tracks RESET button usage'''
        # Save the times of resetting arrows for red lines in the plot
        self.treset.append(tsim)

    def plotdata(self):
        '''
        Draws the saved data (B0 magnitude, B1 frequency and theta) in 3 plots.
        '''

        # Three or four rows with a plot, increase this number to add a plot
        nrows = 3

        # Plot data
        plt.subplot(nrows*100+11)
        plt.title("B0 field")
        plt.plot(self.timetab, self.b0tab)
        
        plt.subplot(nrows*100+12)
        plt.title("B1 freq [Hz]")
        plt.plot(self.timetab, self.f1tab)
        
        plt.subplot(nrows*100+13)
        plt.title("Theta")
        plt.vlines(self.treset, np.min(self.thetatab), np.max(self.thetatab), "r")
        plt.plot(self.timetab, self.thetatab)
        
#        plt.subplot(nrows*100+14)
#        plt.title("Std Dev Theta")
#        plt.plot(self.timetab, self.devtab)

        plt.show()
