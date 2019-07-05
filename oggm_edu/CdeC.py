## Helper functions to clean up Clubes de Ciencia notebooks
## 5 July 2019  EHU

def ice_to_freshwater(icevol, rho_ice=920, rho_water=1000):
    """Cleanly convert volume of glacial ice (km3) to equivalent volume fresh water (liter).
    Arguments:
        icevol = volume of ice to convert, in km3
        rho_ice = density of glacial ice (default 920 kg/m3)
        rho_water = density of freshwater (default 1000 kg/m3)
        """
    km3_to_ltr = 1E12
    water_vol_km3 = icevol * rho_ice / rho_water
    return water_vol_km3 * km3_to_ltr

