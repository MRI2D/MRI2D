"""
MRI 2D by Alex Hoekstra
Python 3.9.13
"""
import time
import numpy as np
from graphics import GUI, clock
from model import Model
from plotter import Plotter


def main(b0set = 4000, b1set = 1000, f1set = 1, tissuefile=""):
    '''Main function containing simulation loop'''

    # Dimensions of compass arrow grid (m,n)
    m, n = 5, 4

    # Initialize GUI window with a caption, xmax,ymax
    xmax,ymax = 1000,800

    # Create model and gui
    #model = Model(xmax,ymax,m,n)
    gui = GUI("MRI (Magnetic Resonance Imaging) 2D simulation",xmax,ymax)

    # Not starting from 0 as then the unaffected arrows are quite boring
    model = Model(b0set, b1set, f1set, m,n,xmax,ymax,tissuefile,gui)

    # factor for speed of control by keys and mouse
    adjustfactor =  np.sqrt(2) # Doubling in 2 seconds. factor per second, >1 for logical behaviour
    
    # Set up timer for loop
    print("Starting simulation")
    tstart = clock()
    t0 = tstart
    tsim = 0     # simulated time for harmonic oscillation of B1
    maxdt = 0.1 # time step max so slow PCs won't have big time steps
    running = True

    # Create a plotter
    dtplot = 0.1 #delta time for tables with plot data
    plotter = Plotter(tsim,dtplot)

    # Main simulation loop
    while running:
        # Time control in loop
        t = clock()
        dt = min(t-t0,maxdt) # set maximum limit to dt
        t0 = t

        # Plot data to be added
        plotter.tableupdate(tsim, model.b0on*model.b0mag,
                            model.theta, model.b1on*model.b1freq)

        # Simulated time, also protected for time steps larger than maxdt
        tsim = tsim + dt
        
        # If a real timestep has been made, we calculate and draw
        if dt>0:

            # Update compass arrows model
            model.update(tsim,dt)

            # Update GUI
            gui.clearscreen()
            gui.textpanel(model.b0mag, model.b1mag, model.b1freq, model.b0on, model.b1on)
            gui.drawarrows(model.arrowlist,m,n)
            gui.updatescreen()
    
        # Key inputs
        # B_0 magnitude with right/left
        keyspressed = gui.getkeys()

        if 'RIGHT' in keyspressed:
            model.b0mag *= adjustfactor**dt
        if 'LEFT' in keyspressed:
            model.b0mag /= adjustfactor**dt
        
        # B_1 magnitude with up/down
        if 'UP' in keyspressed:
            model.b1mag *= adjustfactor**dt
        if 'DOWN' in keyspressed:
            model.b1mag /= adjustfactor**dt

        # Frequency (B_1) with +/-
        if 'PLUS' in keyspressed:
            model.b1freq *= adjustfactor**(dt*0.7)
        if 'MINUS' in keyspressed:
            model.b1freq /= adjustfactor**(dt*0.7)

        # B_0 on/off switch
        if "B0" in keyspressed:
            model.b0on = not model.b0on

        # B_1 on/off switch
        if "B1" in keyspressed:
            model.b1on = not model.b1on

        # Angular velocity reset
        if "V" in keyspressed:
                model.v = model.v * 0#

        # Total reset: angular velocity & position
        if "RESET" in keyspressed:
            model.v = model.v*0
            model.theta = 140+0*model.theta
            plotter.tabletreset(tsim) # Keep track of reset times for plots

        # Magnetic fields details
        # Debug messages
        if "B" in keyspressed and t%.2>.18:
            #time requirement so the message isn't printed too often
            print("____________________\n",
                "B0 magnitude | ", round(b0mag,5), "\n",
                "B1 magnitude | ", round(b1mag,5), "\n",
                "B1 frequency | ", round(b1freq,5),
                "\n____________________")
        
        # Quit with Esc
        if "ESC" in keyspressed:
            running = False
        
        # Runtime limit
        if t>300:
            running = False

    # Exit when loop is ended
    # close screen
    print("Simulation ran",t-tstart,"seconds")
    del gui


    # Plot store tables with data
    plotter.plotdata()
    print("Ready.")

# "If this program is run, run main."
# Checking this makes it easier to keep this .py file in folders for importing
if __name__ == "__main__":
        main()
    
