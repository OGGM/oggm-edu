#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oggm-edu - plots

Created on Thu Dec 27 10:16:48 2018

@author: zora
"""
import matplotlib.pyplot as plt
from oggm.core.flowline import FluxBasedModel, RectangularBedFlowline, TrapezoidalBedFlowline, ParabolicBedFlowline
# There are several solvers in OGGM core. We use the default one for this experiment
FlowlineModel = FluxBasedModel
import numpy as np


def plot_xz_bed(x, bed):
    """This function implements a glacier bed, prepared axes and a legend in 
    altitude vs. distance along glacier plot.
    
    Parameters
    ----------
    x : ndarray
        distance along glacier
    bed : ndarray
        bed rock     
    """
    
    plt.plot(x, bed, color='k', label='Bedrock', linestyle=':', linewidth=1.5)
    plt.xlabel('Distance along glacier (km)')
    plt.ylabel('Altitude (m)')
    plt.legend(loc='best')
    
def glacier(runtime, x, bed, model, mb_model, init_flowline):
    """"This function plots the glacier after a defined runtime"""
    model.run_until(runtime)
    # Plot the initial glacier first:
    plt.plot(x, init_flowline.surface_h, label='Initial glacier')
    # Get the modelled flowline (model.fls[-1]) and plot its new surface
    plt.plot(x, model.fls[-1].surface_h, label='Glacier after {} years'.format(model.yr))
    # Plot the equilibrium line altitude
    plt.axhline(mb_model.ela_h, linestyle='--', color='k', linewidth=0.8)
    # Add the bedrock and axes lables:
    #hf.plot_xz_bed(x=distance_along_glacier, bed = bed_h)
    plt.plot(x, bed, color='k', label='Bedrock', linestyle=':', linewidth=1.5)
    plt.xlabel('Distance along glacier (km)')
    plt.ylabel('Altitude (m)')
    plt.legend(loc='best')
    
def init_model(init_flowline, mb_model, years, glen_a):
    
    model = FlowlineModel(init_flowline, mb_model=mb_model, y0=0., glen_a=glen_a)
    # Year 0 to 600 in 5 years step
    yrs = np.arange(0, years + 1, 5) 
    # Array to fill with data
    nsteps = len(yrs)
    length = np.zeros(nsteps)
    vol = np.zeros(nsteps)
    # Loop
    for i, yr in enumerate(yrs):
        model.run_until(yr)
        length[i] = model.length_m
        vol[i] = model.volume_km3
    
    return model
        