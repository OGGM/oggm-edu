#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oggm-edu - plots

@author: Zora
"""
import numpy as np
import matplotlib.pyplot as plt
from oggm.core.flowline import (FluxBasedModel,
                                RectangularBedFlowline)
from oggm.core.massbalance import LinearMassBalance
from oggm import cfg


def define_linear_bed(top, bottom, nx):
    """Creates a linear bedrock profile.

    Parameters
    ----------
    top : int, float
        top boundary of the domain
    bottom : int, float
        bottom boundary of the domain
    nx : int
        number of grid points

    Returns
    -------
    bed_h : ndarray
        bedrock profile
    surface_h : ndarray
        the glacier surface, i.e. the bedrock profile in case of no glacier
    """

    # linear bed profile
    bed_h = np.linspace(top, bottom, nx)

    # at the beginning, there is no glacier
    # the glacier surface is at the bed altitude
    surface_h = bed_h

    return bed_h, surface_h


def distance_along_glacier(nx, map_dx):
    """Calculates the distance along the glacier in km.

    Parameters
    ----------
    nx : int
        number of grid points
    map_dx : int
        grid point spacing

    Returns
    -------
    ndarray
        distance along the glacier in km.
    """
    return np.linspace(0, nx, nx) * map_dx * 1e-3


def plot_xz_bed(x, bed):
    """This function plot the glacier bed as a function of altitude.

    Parameters
    ----------
    x : ndarray
        distance along glacier
    bed : ndarray
        bedrock profile
    """

    plt.plot(x, bed, color='k', label='Bedrock', linestyle=':', linewidth=1.5)
    plt.xlabel('Distance along glacier [km]')
    plt.ylabel('Altitude [m]')
    plt.legend(loc='best', frameon=False)


def glacier_plot(x, bed, model, mb_model, init_flowline):
    """This function plots the glacier outline of a model. The bedrock, the
    equilibrium line altitude, labeled axes and a legend are added.

    Parameters
    ----------
    x : ndarray
        distance along glacier
    bed : ndarray
        bedrock profile
    model : oggm.core.flowline.FluxBasedModel
        OGGM model class
    mb_model : oggm.core.massbalance.LinearMassBalance
        the glacier mass balance model
    init_flowline : oggm.core.flowline.RectangularBedFlowline
        the glacier flowline

    Returns
    -------
        a labeled glacier plot (x,z)
    """

    # Plot the initial glacier:
    plt.plot(x, init_flowline.surface_h, label='Initial glacier')
    # Get the modelled flowline (model.fls[-1]) and plot its surface
    plt.plot(x, model.fls[-1].surface_h,
             label='Glacier after {} years'.format(model.yr))
    # Plot the equilibrium line altitude
    plt.axhline(mb_model.ela_h, linestyle='--', color='k', linewidth=0.8)
    # Add the bedrock and axes labels:
    plt.plot(x, bed, color='k', label='Bedrock', linestyle=':', linewidth=1.5)
    plt.xlabel('Distance along glacier [km]')
    plt.ylabel('Altitude [m]')
    plt.legend(loc='best')


def init_model(init_flowline, mb_model, years, glen_a=None, fs=None):
    """This function initializes a new model, therefore it uses FluxBasedModel.
    The outline of the glacier is calculated for a chosen amount of years.

    Parameters
    ----------
    init_flowline : oggm.core.flowline.RectangularBedFlowline
        the glacier flowline
    mb_model : oggm.core.massbalance.LinearMassBalance
        the glacier mass balance model
    years : int
        year until which glacier evolution is calculated
    glen_a : float
        Glen's parameter (default = 2.4e-24)
    fs : float
        sliding parameter (default = 0)

   Returns
   -------
   model : oggm.core.flowline.FluxBasedModel
       the initialized model

   TODO: return also length and volume steps (they are calculated for every
         time step)
   """
    if glen_a is None:
        glen_a = cfg.PARAMS['glen_a']

    if fs is None:
        fs = 0

    model = FluxBasedModel(init_flowline, mb_model=mb_model, y0=0.,
                           glen_a=glen_a, fs=fs)
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

    return model  # , length, vol


def surging_glacier(yrs, init_flowline, mb_model, bed, widths, map_dx, glen_a,
                    fs, fs_surge, model):
    """Function implements surging events in evolution of glacier. 2 different
    sliding parameters can be used.

    Parameters
    ----------
    yrs : int
        years in which glacier evolution should be calculated
    init_flowline : oggm.core.flowline.RectangularBedFlowline
        the glacier flowline
    mb_model : oggm.core.massbalance.LinearMassBalance
        the glacier mass balance model
    bed : ndarray
        bedrock profile
    widths : ndarray
        the glacier widths
    map_dx : int
        grid point spacing
    glen_a : float
        Glen's parameter
    fs : float
        sliding parameter for slow motion years
    fs_surge : float
        sliding parameter for the surging period
    model : oggm.core.flowline.FluxBasedModel
       OGGM model class

    Returns
    -------
    model : oggm.core.flowline.FluxBasedModel
        OGGM model class
    surging_glacier_h : list
        outline of glacier
    length_s3 : ndarray
        length after each time step
    vol_s3 : ndarray
        volume after each time step
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
            init_flowline = RectangularBedFlowline(
                    surface_h=surging_glacier_h_ts, bed_h=bed, widths=widths,
                    map_dx=map_dx)
            model = FluxBasedModel(init_flowline, mb_model=mb_model, y0=yr,
                                   glen_a=glen_a, fs=fs_surge)

        elif (yr-yrs[i-1]) == 1 and (yrs[i+1]-yr) == 10:
            # Save glacier geometry after the surge
            surging_glacier_h.append(model.fls[-1].surface_h)

            # Glacier evolution
            surging_glacier_h_ts = model.fls[-1].surface_h
            init_flowline = RectangularBedFlowline(
                    surface_h=surging_glacier_h_ts, bed_h=bed, widths=widths,
                    map_dx=map_dx)
            model = FluxBasedModel(init_flowline, mb_model=mb_model, y0=yr,
                                   glen_a=glen_a, fs=fs)

    return model, surging_glacier_h, length_s3, vol_s3


def response_time_vol(model, perturbed_mb):
    """Calculation of the volume response time after Oerlemans (1997).

    Parameters
    ----------
    model : oggm.core.flowline.FluxBasedModel
        OGGM model class of the glacier in equilibrium
    perturbed_mb : oggm.core.massbalance.LinearMassBalance
        Perturbed mass balance model

    Returns
    -------
    response_time : numpy.float64
        the response time of the glacier
    pert_model : oggm.core.flowline.FluxBasedModel
        OGGM model class of the glacier in equilibrium adapted to the new ELA
    """
    # to be sure that the model state is in equilibrium (maybe not necessary)
    count = 0
    while True:
        try:
            model.run_until_equilibrium(rate=0.006)
            break
        except RuntimeError:
            count += 1
            # if equilibrium not reached yet, add 1000 years. Then try again.
            model.run_until(models[0].yr + 1000)
            if count == 6:
                raise RuntimeError('Because the gradient is be very small, '
                                   'the equilibrium will be reached only '
                                   'after many years. Run this cell '
                                   'again, then it should work.')

    # set up new model, whith outlines of first model, but new mb_model
    pert_model = FluxBasedModel(model.fls[-1], mb_model=perturbed_mb, y0=0.)
    # run it until in reaches equilibrium state
    count = 0
    while True:
        try:
            pert_model.run_until_equilibrium(rate=0.006)
            break
        except RuntimeError:
            count += 1
            # if equilibrium not reached yet, add 1000 years. Then try again.
            pert_model.run_until(models[0].yr + 1000)
            if count == 6:
                raise RuntimeError('Because the gradient is be very small, '
                                   'the equilibrium will be reached only '
                                   'after many years. Run this cell '
                                   'again, then it should work.')

    # save outline of model in equilibrium state
    eq_pert_model = pert_model.fls[-1].surface_h
    # recalculate the perturbed model to be able to save intermediate steps
    yrs = np.arange(0, pert_model.yr, 5)
    nsteps = len(yrs)
    length_w = np.zeros(nsteps)
    vol_w = np.zeros(nsteps)
    year = np.zeros(nsteps)
    recalc_pert_model = FluxBasedModel(model.fls[-1], mb_model=perturbed_mb,
                                       y0=0.)
    for i, yer in enumerate(yrs):
        recalc_pert_model.run_until(yer)
        year[i] = recalc_pert_model.yr
        length_w[i] = recalc_pert_model.length_m
        vol_w[i] = recalc_pert_model.volume_km3
    # to get response time: calculate volume difference between model and pert.
    # model in eq. state
    vol_dif = recalc_pert_model.volume_km3
    vol_dif -= (recalc_pert_model.volume_km3 - model.volume_km3) / np.e
    # search for the appropriate time by determining the year with the closest
    # volume to vol_dif:
    # difference between volumes of different time steps and vol_dif
    all_dif_vol = abs(vol_w - vol_dif).tolist()
    # find index of smallest difference between
    index = all_dif_vol.index(min(all_dif_vol))
    response_time = year[index]

    return response_time, pert_model


def plot_glacier_3d(dis, bed, widths, nx, elev=30, azim=40):
    """Plots the glacier geometry in pseudo-3d.

    Parameters
    ----------
    dis : ndarray
        the distance along the flowline
    bed : ndarray
        the glacier bed
    widths: ndarray
        the glacier widths
    nx : int
        number of grid points
    elev : int
        elevation viewing angle for 3D plot
    azim : int
        azimuth viewing angle for 3D plot

    Returns
    -------
    fig : matplotlib.figure.Figure
        the 3D plot
    """

    # arrays for 3D plot
    X = np.tile(dis, (nx, 1)).T
    Z = np.tile(bed, (nx, 1)).T
    Y = []
    for w in widths:
        Y.append(np.linspace(-w/2, w/2, nx))
    Y = np.array(Y)

    # plot glacier geometry in 3D
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(elev, azim)
    ax.plot_surface(X, Y, Z)
    ax.set_xlabel('Distance along flowline / (km)')
    ax.set_ylabel('Glacier width across flowline / (m)')
    ax.set_zlabel('Elevation / (m)')

    return fig


def linear_mb_equilibrium(bed, surface, accw, elaw, nz, mb_grad, nx, map_dx,
                          plot=True):
    """Runs the OGGM FluxBasedModel with a linear mass balance
    gradient until the glacier reaches equilibrium.

    Parameters
    ----------
    bed : ndarray
        the glacier bed
    surface : ndarray
        the initial glacier surface
    accw : int
        the width of the glacier at the top of the accumulation area
    elaw : int
        the width of the glacier at the equilibrium line altitude
    nz : float
        fraction of vertical grid points occupied by accumulation area
    mb_grad : int, float
        the mass balance altitude gradient in mm w.e. m^-1 yr^-1
    nx : int
        number of grid points
    map_dx : int
        grid point spacing
    plot : bool
        show a pseudo-3d plot of the glacier geometry

    Returns
    -------
    model : oggm.core.flowline.FluxBasedModel
        OGGM model class of the glacier in equilibrium
    """

    # accumulation area occupies a fraction NZ of the total glacier extent
    acc_width = np.linspace(accw, elaw, int(nx * nz))

    # ablation area occupies a fraction 1 - NZ of the total glacier extent
    abl_width = np.tile(elaw, nx - len(acc_width))

    # glacier widths profile
    widths = np.hstack([acc_width, abl_width])

    # model widths
    mwidths = np.zeros(nx) + widths / map_dx

    # define the glacier bed
    init_flowline = RectangularBedFlowline(surface_h=surface, bed_h=bed,
                                           widths=mwidths, map_dx=map_dx)

    # equilibrium line altitude
    ela = bed[np.where(widths == elaw)[0][0]]

    # linear mass balance model
    mb_model = LinearMassBalance(ela, grad=mb_grad)

    # flowline model
    model = FluxBasedModel(init_flowline, mb_model=mb_model,
                           y0=0., min_dt=0, cfl_number=0.01)

    # run until the glacier reaches an equilibrium
    model.run_until_equilibrium()

    # show a pseudo-3d plot of the glacier geometry
    if plot:
        dis = distance_along_glacier(nx, map_dx)
        plot_glacier_3d(dis, bed, widths, nx)

    return model
