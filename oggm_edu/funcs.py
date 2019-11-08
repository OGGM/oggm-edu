#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oggm-edu - plots

@author: Zora
"""
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from oggm.core.flowline import (FluxBasedModel,
                                RectangularBedFlowline)
from oggm.core.massbalance import LinearMassBalance
from oggm import cfg, utils


def define_linear_bed(top, bottom, nx):
    """Creates a linear glacier bed.

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
        the glacier bed
    surface_h : ndarray
        the glacier surface, i.e. the glacier bed in case of no glacier
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
    """This function plots the glacier bed as a function of altitude.

    Parameters
    ----------
    x : ndarray
        distance along glacier
    bed : ndarray
        the glacier bed
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
        the glacier bed
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
    glen_a : float, optional
        Glen's parameter, (default: 2.4e-24 s^-1 Pa^-3)
    fs : float, optional
        sliding parameter, (default: 0)

   Returns
   -------
   model : oggm.core.flowline.FluxBasedModel
       the initialized model

   TODO: return also length and volume steps (they are calculated for every
         time step)
   """
    if not glen_a:
        glen_a = cfg.PARAMS['glen_a']

    if not fs:
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
        the glacier bed
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
    elev : int, optional
        elevation viewing angle for 3D plot, (default: 30)
    azim : int, optional
        azimuth viewing angle for 3D plot, (default: 40)

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
                          idx=None, advance=None, retreat=None, plot=True):
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
    idx : int, optional
        number of vertical grid points to shift ELA down/upglacier
    advance : bool, optional
        move the ELA downglacier by idx grid points to simulate
        a glacier advance
    retreat : bool, optional
        move the ELA upglacier by idx grid points to simulate
        a glacier retreat
    plot : bool, optional
        show a pseudo-3d plot of the glacier (default: True)

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

    # in case of an advance scenario, move the ELA downglacier by a number of
    # vertical grid points idx
    if advance and idx:
        ela = bed[np.where(widths == elaw)[0][idx]]

    # in case of a retreat scenario, move the ELA upglacier by a number of
    # vertical grid points idx
    elif retreat and idx:
        ela = bed[np.where(widths == acc_width[-idx])[0][0]]

    # in case of no scenario, the ela is the height where the width of the ela
    # is first reached
    else:
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


def linear_accumulation(mb_grad, ela, gsurface, bed, widths, acc_0=None):
    """Creates accumulation as a linear function of elevation.

    Parameters
    ----------
    mb_grad : int, float
        the mass balance altitude gradient in mm w.e. m^-1 yr^-1
    ela : int, float
        the equilibrium line altitude
    gsurface : ndarray
        the glacier elevation surface
    bed : ndarray
        the glacier bed
    widhts : ndarray
        the glacier widths
    acc_0 : int, float, optional
        the accumulation at the ELA in m w.e. yr^-1, (the default is None,
        which implies it is calculated so that the accumulation at the glacier
        terminus is exactly 0)

    Returns
    -------
    acc_d : ndarray
        the linear accumulation profile
    acc_0 : int, float
        the accumulation at the ELA in m w.e. yr^-1
    """

    # glacier terminus
    terminus = gsurface[gsurface <= bed][0]

    # get the closest value to the ELA in the glacier surface array
    ela_closest = gsurface[np.abs(gsurface - ela).argmin()]

    # check if the accumulation at the ELA, acc_0, is specified
    if not acc_0:
        # if not specified, the accumulation at the ELA is calculated to
        # produce an accumulation of exactly 0 at the glacier terminus
        acc_0 = (- mb_grad * (terminus - ela_closest) *
                 widths[gsurface == terminus] * 1e-3)

    # accumulation as a function of altitude in one year: m w.e. yr^-1
    # scaled by the model glacier widths
    acc = (acc_0 + mb_grad * (gsurface[gsurface >= terminus] - ela_closest) *
           1e-3 * widths[gsurface >= terminus])

    # append 0 accumulation downstream of glacier terminus
    acc_d = np.hstack([acc, np.zeros(len(gsurface[gsurface < terminus]))])

    return acc_d, acc_0


def linear_ablation(mb_grad, ela, gsurface, bed, widths, abl_0=None):
    """Creates ablation as a linear function of elevation.

    Parameters
    ----------
    mb_grad : int, float
        the mass balance altitude gradient in mm w.e. m^-1 yr^-1
    ela : int, float
        the equilibrium line altitude
    gsurface : ndarray
        the glacier elevation surface
    bed : ndarray
        the glacier bed
    widhts : ndarray
        the glacier widths
    abl_0 : int, float, optional
        the ablation at the ELA in m w.e. yr^-1, (the default is None,
        which implies it is calculated so that the ablation at the glacier top
        goes to 0). To balance accumulation and ablation at the ELA, pass the
        keyword argument ``acc_0`` from the ``linear_accumulation`` function
        to the keyword argument ``abl_0``.

    Returns
    -------
    acc_d : ndarray
        the linear ablation profile
    abl_0 : int, float
        the ablation at the ELA in m w.e. yr^-1
    """
    # glacier terminus
    terminus = gsurface[gsurface <= bed][0]

    # get the closest value to the ELA in the glacier surface array
    ela_closest = gsurface[np.abs(gsurface - ela).argmin()]

    # glacier top
    top = gsurface[0]

    # check if the ablation at the ela, abl_0, is specified
    if not abl_0:
        # if not specified, the ablation at the ELA is calculated to
        # produce an ablation of exactly 0 at the glacier top
        abl_0 = (- mb_grad * (top - ela_closest) *
                 widths[gsurface == top] * 1e-3)

    # ablation as a function of altitude in one year: m w.e. yr^-1
    # scaled by the model glacier widths
    abl = (- abl_0 + mb_grad * (gsurface[gsurface >= terminus] - ela_closest) *
           1e-3 * widths[gsurface >= terminus])

    # append 0 ablation downstream of glacier terminus
    abl_d = np.hstack([abl, np.zeros(len(gsurface[gsurface < terminus]))])

    # correct ablation > 0 to 0
    abl_d[abl_d > 0] = 0

    return abl_d, abl_0


def intro_glacier_plot(ax, dis, bed_h, initial, ref_sfc, labels, ela=None,
                       plot_ela=False):
    """Plots the glacier bed together with the actual glacier surface and
    perturbed glacier surfaces, e.g. the glacier surface after accumulation or
    ablation.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        a matplotlib axes instance
    dis : ndarray
        the distance along the glacier
    bed_h : ndarray
        the glacier bed
    initial : ndarray
        the actual glacier surface
    ref_sfc : list
        a list of ndarrays containing the perturbed glacier surfaces
    labels: list
        a list of strings describing the perturbed glacier surfaces
    ela : list, optional
        list of equilibrium line altitudes, (default: None). If specified,
        the first element of this list should be the ELA of the unperturbed
        glacier surface.
    plot_ela : bool, optional
        flag to plot ela, (default: False)
    """

    # plot the glacier bed and the initial glacier surface
    ax.plot(dis, bed_h, '--k', label='bed')
    ax.plot(dis, initial, '--r', label='initial')

    # check which surface is passed to the function
    counter = 0
    for sfc, l in zip(ref_sfc, labels):

        # fill area between bed/initial surface or bed/reference surface
        if counter < 1:
            ax.fill_between(dis, bed_h, sfc, sfc <= initial,
                            color='grey', alpha=0.3)
            if any(sfc - initial > 0):
                ax.fill_between(dis, bed_h, initial,
                                sfc >= initial, color='grey', alpha=0.3)
            else:
                ax.fill_between(dis, bed_h, initial,
                                sfc > initial, color='grey', alpha=0.3)

        # accumulation surface
        if all(sfc - initial >= 0):
            ax.plot(dis, sfc, color='lightblue',
                    linewidth=2, label=l)
            ax.fill_between(dis, initial, sfc,
                            sfc >= initial, color='lightblue', alpha=0.5)

        # ablation surface
        elif not any(sfc - initial > 0):
            ax.plot(dis, sfc, '-r', linewidth=2, label=l)
            ax.fill_between(dis, initial, sfc,
                            sfc <= initial, color='red', alpha=0.3)

        # mass balance surface
        else:
            ax.plot(dis, sfc, '-k', linewidth=2, label=l)
            ax.fill_between(dis, initial, sfc,
                            sfc > initial, color='lightblue', alpha=0.5)
            ax.fill_between(dis, initial, sfc,
                            sfc <= initial, color='red', alpha=0.3)
        # advance counter
        counter += 1

    # check if ELA's should be plotted or not
    if plot_ela and ela:

        # add a label for the initial ELA to the labels list
        labels.insert(0, 'Initial')

        # plot the ela's
        for e, l in zip(ela, labels):

            # check which ELA it is
            if e > ela[0]:
                color = 'red'
            elif e < ela[0]:
                color = 'lightblue'
            else:
                color = 'grey'

            # add horizontal line at the current ELA
            ax.hlines(e, dis[0], dis[-1],
                      linestyle='--', color=color)
            ax.text(dis[-1], e + 10,
                    'ELA: {}'.format(l), horizontalalignment='right',
                    verticalalignment='bottom', color=color)

    # axes labels and legend
    ax.legend(frameon=False)
    ax.set_xlabel('Distance along flowline / (km)')
    ax.set_ylabel('Elevation / (m)')


def correct_to_bed(bed, ref_sfc):
    """Corrects a reference surface to the glacier bed in case of negative
    ice thickness.

    Parameters
    ----------
    bed : ndarray
        the glacier bed
    ref_sfc : ndarray
        the (perturbed) glacier surface

    Returns
    -------
    ref_sfc : ndarray
        the corrected glacier surface
    """

    # check where the ice thickness is negative
    no_ice = np.where(ref_sfc < bed)

    # correct the reference surface to the bed surface where there is no ice
    ref_sfc[no_ice] = bed[no_ice]

    return ref_sfc


def read_run_results(gdir, window=36, filesuffix=None):
    """Reads the output diagnostics of a simulation
    and puts the data in a pandas dataframe.
    
    Parameters
    ----------
    gdir : oggm.GlacierDirectory
        the glacier directory defined by oggm
    window : int
        size of the moving window: number of observations used
        to smooth the glacier length timeseries
    filesuffix : str
        the file identifier
    
    Returns
    -------
    odf : pd.DataFrame
        dataframe containing glacier length, volume and water storage
    """
    
    # read model output
    with xr.open_dataset(gdir.get_filepath('model_diagnostics',
                                           filesuffix=filesuffix)) as ds:
        ds = ds.load()

    # length needs filtering
    ts = ds.length_m.to_series()
    ts = ts.rolling(window).min()
    ts.iloc[0:window] = ts.iloc[window]
    
    # volume change
    delta_vol = np.append(ds.volume_m3.data[1:] - ds.volume_m3.data[0:-1], [0])
    
    if ds.calendar_month[0] == 10 and gdir.cenlat < 0:
        # this is to cover up a bug in OGGM
        _, m = utils.hydrodate_to_calendardate(ds.hydro_year.data, ds.hydro_month.data, start_month=4)
        ds.calendar_month[:] = m
    
    odf = pd.DataFrame()
    odf['length_m'] = ts
    odf['volume_m3'] = ds.volume_m3
    odf['delta_water_m3'] = delta_vol * 0.9
    odf['month'] = ds.calendar_month
    
    return odf


def compute_climate_statistics(gdir, tmin='1985', tmax='2015', lapse_rate=0.0065):
    """Computes monthly average temperature and precipitation
    during the climate period defined by tmin and tmax.
    
    Temperatures are reduced to the terminus elevation assuming
    a constant lapse rate.
    
    Parameters
    ----------
    gdir : oggm.GlacierDirectory
        the glacier directory defined by oggm
    tmin : int
        the beginning of the period of interest
    tmax : int
        the end of the period of interest
    
    Returns
    -------
    odf : pd.DataFrame
        dataframe containing monthly average temperature and precipitation
        during tmin-tmax
    """
    
    with xr.open_dataset(gdir.get_filepath('climate_monthly')) as ds:
        ds = ds.load()
        
    ds = ds.sel(time=slice(str(tmin), str(tmax)))
        
    dsm = ds.groupby('time.month').mean(dim='time')
    odf = pd.DataFrame()
    odf['temp_celcius'] = dsm.temp.to_series()
    odf['prcp_mm_mth'] = dsm.prcp.to_series()
    
    # We correct for altitude difference
    d = utils.glacier_statistics(gdir)
    odf['temp_celcius'] += (ds.ref_hgt - d['flowline_min_elev']) * lapse_rate
    
    return odf
