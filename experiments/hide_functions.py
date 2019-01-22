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

def response_time_vol(model, perturbed_mb):
    """Calculation of the volume response time after Oerlemans(1997).
    Parameters
    ----------
    model : model in equilibrium state 
    perturbed_mb : new mb-model, which expresses the changes in climate"""
    # to be sure that the model state is in equilibrium (maybe not necessary)
    #model.run_until_equilibrium()
    try:
        model.run_until_equilibrium()
    except RunTimeError:
        model.run_until(model.yr + 1000)
        try:
            model.run_until_equilibrium()
        except RunTimeError:
            model.run_until(model.yr + 1000)
            try:
                model.run_until_equilibrium()
            except RunTimeError:
                model.run_until(model.yr + 1000)
                try:
                    model.run_until_equilibrium()
                except RunTimeError:
                    model.run_until(model.yr + 1000)
                    try:
                        model.run_until_equilibrium()
                    except RunTimeError:
                        raise RunTimeError('There is a problem with the function because it cannot handle the gradient. Probably it is too small to handle.')
    # set up new model, whith outlines of first model, but new mb_model
    pert_model = FlowlineModel(model.fls[-1], mb_model=perturbed_mb, y0=0.)
    try:
        pert_model.run_until_equilibrium()
    except RunTimeError:
        pert_model.run_until(pert_model.yr + 1000)
        try:
            pert_model.run_until_equilibrium()
        except RunTimeError:
            pert_model.run_until(pert_model.yr + 1000)
            try:
                pert_model.run_until_equilibrium()
            except RunTimeError:
                pert_model.run_until(pert_model.yr + 1000)
                try:
                    pert_model.run_until_equilibrium()
                except RunTimeError:
                    pert_model.run_until(pert_model.yr + 1000)
                    try:
                        pert_model.run_until_equilibrium()
                    except RunTimeError:
                        raise RunTimeError('There is a problem with the function because it cannot handle the gradient. Probably it is too small to handle.')
    #pert_model.run_until(2000)
    #pert_model.run_until_equilibrium()
    # save outline of model in equilibrium state
    eq_pert_model = pert_model.fls[-1].surface_h
    # recalculate the perturbed model to be able to save intermediate steps
    yrs = np.arange(0, pert_model.yr, 5)
    nsteps = len(yrs)
    length_w = np.zeros(nsteps)
    vol_w = np.zeros(nsteps)
    year = np.zeros(nsteps)
    recalc_pert_model = FlowlineModel(model.fls[-1], mb_model=perturbed_mb, y0=0.)
    for i, yer in enumerate(yrs):
        recalc_pert_model.run_until(yer)
        year[i] = recalc_pert_model.yr
        length_w[i] = recalc_pert_model.length_m
        vol_w[i] = recalc_pert_model.volume_km3
    # to get response time: calculate volume difference between model and pert. model in eq. state
    vol_dif = recalc_pert_model.volume_km3 - ((recalc_pert_model.volume_km3 - model.volume_km3) / np.e)
    # search for the appropriate time by determining the year with the closest volume to vol_dif:
        # difference between volumes of dif time steps and vol_dif
    all_dif_vol = abs(vol_w - vol_dif).tolist()
    # find index of smallest difference between
    index = all_dif_vol.index(min(all_dif_vol))
    response_time = year[index]
    
    return response_time, pert_model
    
     