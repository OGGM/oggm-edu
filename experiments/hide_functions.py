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
from oggm import cfg


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
    plt.xlabel('Distance along glacier [km]')
    plt.ylabel('Altitude [m]')
    plt.legend(loc='best')
    
def glacier(runtime, x, bed, model, mb_model, init_flowline):
    """"This function plots the glacier after a defined runtime with labeled 
    axes and a legend."""
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
    plt.xlabel('Distance along glacier [km]')
    plt.ylabel('Altitude [m]')
    plt.legend(loc='best')
    
def init_model(init_flowline, mb_model, years, glen_a=None, fs=None):
    """This function uses FlowlineModel and returns the model. 
    TODO: return also length and volume.
    Parameters
    ----------
    ..."""
    if glen_a is None:
        glen_a = cfg.PARAMS['glen_a']
        
    if fs is None:
        fs = 0
    
    model = FlowlineModel(init_flowline, mb_model=mb_model, y0=0., glen_a=glen_a, fs=fs)
    # Year 0 to 600 in 5 years step
    yrs = np.arange(0, years, 5) 
    # Array to fill with data
    nsteps = len(yrs)
    length = np.zeros(nsteps)
    vol = np.zeros(nsteps)
    # Loop
    for i, yr in enumerate(yrs):
        model.run_until(yr)
        length[i] = model.length_m
        vol[i] = model.volume_km3
    
    return model#, length, vol
        
    
def surging_glacier(yrs, init_flowline, mb_model, bed, widths, map_dx, glen_a, fs, fs_surge, model):
    """Function for surging experiments. 2 different sliding parameters can be 
    used.
    TODO: Parameters
    """    

    # Array to fill with data
    nsteps = len(yrs)
    length_s3 = np.zeros(nsteps)
    vol_s3 = np.zeros(nsteps)
    surging_glacier_h = []

    # Loop & glacier evolution
    for i, yr in enumerate(yrs):
        model.run_until(yr)
        length_s3[i] = model.length_m
        vol_s3[i] = model.volume_km3    
    
        if i == 0 or i == (nsteps-1):
            continue
    
        elif (yr-yrs[i-1]) == 10 and (yrs[i+1]-yr) == 1:
            # Save glacier geometry before the surge
            surging_glacier_h.append(model.fls[-1].surface_h)
        
            # Glacier evolution
            surging_glacier_h_ts = model.fls[-1].surface_h
            init_flowline = RectangularBedFlowline(surface_h=surging_glacier_h_ts, bed_h=bed, widths=widths, map_dx=map_dx)
            model = FlowlineModel(init_flowline, mb_model=mb_model, y0=yr, glen_a=glen_a, fs=fs_surge)
    
        elif (yr-yrs[i-1]) == 1 and (yrs[i+1]-yr) == 10:
            # Save glacier geometry after the surge
            surging_glacier_h.append(model.fls[-1].surface_h)
        
            # Glacier evolution        
            surging_glacier_h_ts = model.fls[-1].surface_h
            init_flowline = RectangularBedFlowline(surface_h=surging_glacier_h_ts, bed_h=bed, widths=widths, map_dx=map_dx)
            model = FlowlineModel(init_flowline, mb_model=mb_model, y0=yr, glen_a=glen_a, fs=fs)
        
    return model, surging_glacier_h, length_s3, vol_s3