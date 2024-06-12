"""
Models for solar flux density at a given distance from the Sun.

This module provides access to various models of solar flux density. Models
currently supported are:

- Colina      (0.1195 to 2.5 micron)
- Kurucz      (0.15   to 300 micron)
- Rieke       (0.2    to 30  micron)
- STIS        (0.1195 to 2.7 micron)
- STIS_Rieke  (0.1195 to 30  micron)

The solar flux density can be returned directly in the form of a Tabulation
object (see the package `rms-tabulation <https://pypi.org/project/rms-tabulation>`_
or the mean flux density can be returned over a particular filter bandwith. In
each case you can specify the model to use, the units for wavelength and flux
density, the distance from the Sun, and whether or not to return just F instead
of flux density.
"""

# When a user does a wildcard import (from solar import *), don't import any
# solar models by default; but DO export the public interface functions and
# variables.
__all__ = ['flux_density', 'bandpass_flux_density', 'mean_flux_density',
           'bandpass_f', 'mean_f', 'AU', 'C', 'TO_CGS', 'TO_PER_ANGSTROM',
           'TO_PER_NM']

import functools
import importlib
import numpy as np
import tabulation as tab

try:
    from ._version import __version__
except ImportError:  # pragma no cover
    __version__ = 'Version unspecified'


# Class constants to be used externally as needed
AU = 149597870.7       # km
C = 299792.458         # km/sec
C_IN_UM_HZ = C * 1.e9  # um/sec

# Converts from W/m^2 to erg/s/cm^2
TO_CGS = 1.e7 / 1.e4

# Converts from flux per micron to flux per Angstrom
TO_PER_ANGSTROM = 1.e-4

# Converts from flux per micron to flux per nanometer
TO_PER_NM = 1.e-3

# First UNIT_DICT item is conversion factor from W/m^2/um or from W/m^2/Hz.
# Second item is True if the units are per wavelength, False if per frequency.
UNIT_DICT = {
    'W/m^2/um'     : (1.   , True),     # default units
    'W/m^2/nm'     : (1.e-3, True),
    'W/m^2/A'      : (1.e-4, True),
    'erg/s/cm^2/um': (1.e+3, True),
    'erg/s/cm^2/nm': (1.   , True),
    'erg/s/cm^2/A' : (1.e-1, True),

    'W/m^2/Hz'     : (1.   , False),
    'erg/s/cm^2/Hz': (1.e+3, False),
    'Jy'           : (1.e26, False),
    'uJy'          : (1.e32, False),
}

# First XUNIT_DICT item is conversion factor from um or from Hz.
# Second item is True if the units are wavelength, False if frequency.
XUNIT_DICT = {
    'um': (1.  , True),
    'nm': (1.e3, True),
    'A' : (1.e4, True),
    'Hz': (1.  , False),
}


#===============================================================================
@functools.lru_cache(maxsize=4)
def flux_density(model='STIS_Rieke', *, units='W/m^2/um', xunits='um',
                 sun_range=1., solar_f=False):
    """
    Compute the flux density of a solar model in the specified units.

    Args:
        model (str, optional): Name of the model.
        units (str, optional): Units for the flux.
            Options are: "W/m^2/um", "W/m^2/nm", "W/m^2/A", "erg/s/cm^2/um",
            "erg/s/cm^2/nm", "erg/s/cm^2/A", "W/m^2/Hz", "erg/s/cm^2/Hz", "Jy",
            or "uJy". "u" represents "mu" meaning micro.
        xunits (str, optional): Units for the x-axis.
            Options are: "um", "nm", "A", or "Hz". "u" represents "mu"
            meaning micro.
        sun_range (float, optional): Distance from Sun to target in AU.
        solar_f (bool, optional): True to divide by pi, providing solar F
            instead of solar flux density.

    Returns:
        Tabulation: The model solar flux density in the specified units.
    """

    # Each reference to a named model triggers the import of its associated
    # Python file hosts/solar/<name>.py, referenced as "solar.<name>"
    # here. Note that modules are imported only if requested, not by default.
    try:
        module = importlib.import_module(f'solar.{model.lower()}')
    except ImportError:
        raise ValueError(f'undefined solar model: {model} (valid models are: '
                         'colina, kurucz, rieke, stis_rieke, stis)')

    # Check units
    if units not in UNIT_DICT:
        valid_units = ', '.join(UNIT_DICT.keys())
        raise ValueError(f'invalid units: {units} (valid units are: '
                         f'{valid_units})')

    if xunits not in XUNIT_DICT:
        valid_xunits = ', '.join(XUNIT_DICT.keys())
        raise ValueError(f'invalid units: {xunits} (valid units are: '
                         f'{valid_xunits})')

    # Get the tabulation
    tabulation = module.FLUX_DENSITY

    # If we have the desired units, return
    if units == module.UNITS and xunits == module.XUNITS:
        return tabulation * ((1./np.pi if solar_f else 1.) / sun_range**2)

    # Gather unit info
    (scale, per_wavelength) = UNIT_DICT[units]
    (xscale, x_is_wavelength) = XUNIT_DICT[xunits]

    (model_scale, model_per_wavelength) = UNIT_DICT[module.UNITS]
    (model_xscale, model_x_is_wavelength) = XUNIT_DICT[module.XUNITS]

    # Create the new x-values
    if x_is_wavelength == model_x_is_wavelength:
        new_x = (xscale / model_xscale) * tabulation.x
    else:
        new_x = (xscale * model_xscale * C_IN_UM_HZ) / tabulation.x

    # Create the new y-values
    factor = scale/model_scale * (1./np.pi if solar_f else 1.) / sun_range**2

    if per_wavelength == model_per_wavelength:
        new_y = factor * tabulation.y

    else:
        # w = wavelength in microns
        # f = frequency in Hz
        #
        # We must satisfy:
        #   flux_w dw = flux_f df
        # so
        #   flux_w = flux_f |df/dw|
        # or
        #   flux_f = flux_w |dw/df|
        #
        # We have
        #   f = C/w
        # so
        #   |df/dw| = C/w^2 = f^2/C
        # or
        #   |dw/df| = C/f^2 = w^2/C

        if per_wavelength:  # we need df/dw
            if model_x_is_wavelength:  # pragma: no cover
                new_y = ((factor * C_IN_UM_HZ * model_xscale**2) *
                         tabulation.y / tabulation.x**2)
            else:  # pragma: no cover - There are currently no models in Hz
                new_y = ((factor / C_IN_UM_HZ / model_xscale**2) *
                         tabulation.y * tabulation.x**2)

        else:               # we need dw/df
            if model_x_is_wavelength:  # pragma: no cover
                new_y = ((factor / C_IN_UM_HZ / model_xscale**2) *
                         tabulation.y * tabulation.x**2)
            else:  # pragma: no cover - There are currently no models in Hz
                new_y = ((factor * C_IN_UM_HZ * model_xscale**2) *
                         tabulation.y / tabulation.x**2)

    return tab.Tabulation(new_x, new_y)

#===============================================================================
def bandpass_flux_density(bandpass, model='STIS_Rieke', *, units='W/m^2/um',
                          xunits='um', sun_range=1., solar_f=False):
    """
    Compute the average solar flux density over a filter bandpass.

    Args:
        bandpass (Tabulation or tuple): The Tabulation of the filter bandpass,
            with wavelength in units specified by `xunits` (if `model` is a
            string) or in the same units as `model` (if `model` is a
            Tabulation). Alternatively, a tuple of two arrays (wavelength,
            fraction), each of the same size.
        model (str or Tabulation, optional): Name of the model. Alternatively, a
            Tabulation of the solar flux density, already in the desired units.
        units (str, optional): Units for the flux.
            Options are: "W/m^2/um", "W/m^2/nm", "W/m^2/A", "erg/s/cm^2/um",
            "erg/s/cm^2/nm", "erg/s/cm^2/A", "W/m^2/Hz", "erg/s/cm^2/Hz", "Jy",
            or "uJy". "u" represents "mu" meaning micro. Ignored if `model` is a
            Tabulation.
        xunits (str, optional): Units for the x-axis.
            Options are: "um", "nm", "A", or "Hz". "u" represents "mu" meaning
            micro. Ignored if `model` is a Tabulation.
        sun_range (float, optional): Distance from Sun to target in AU.
        solar_f (bool, optional): True to divide by pi, providing solar F
            instead of solar flux density.

    Returns:
        float: The mean solar flux density or solar F within the filter
        bandpass.

    Note:
        If the bandpass of the filter is wider than the wavelength coverage of
        the selected solar model, the computation will be restricted to the
        wavelength range that is in common between the filter and the model.
    """

    if not isinstance(bandpass, tab.Tabulation):
        bandpass = tab.Tabulation(*bandpass)

    if isinstance(model, tab.Tabulation):
        flux = model * (1./np.pi if solar_f else 1.) / sun_range**2
    else:
        flux = flux_density(model, units=units, xunits=xunits,
                            sun_range=sun_range, solar_f=solar_f)

    # Multiply together the bandpass and the solar spectrum Tabulations
    product = bandpass * flux

    # Resample the bandpass at the same wavelengths for a more reliable
    # normalization
    bandpass = bandpass.resample(product.x)

    # Return the ratio of integrals
    return product.integral() / bandpass.integral()

#===============================================================================
def mean_flux_density(center, width, model='STIS_Rieke', *, units='W/m^2/um',
                      xunits='um', sun_range=1., solar_f=False):
    """
    Compute average solar flux density over the bandpass of a "boxcar" filter.

    Args:
        center (float): The center of the bandpass (microns).
        width (float): The full width of the bandpass (microns).
        model (str or Tabulation, optional): Name of the model. Alternatively, a
            Tabulation of the solar flux density, already in the desired units.
        units (str, optional): Units for the flux.
            Options are: "W/m^2/um", "W/m^2/nm", "W/m^2/A", "erg/s/cm^2/um",
            "erg/s/cm^2/nm", "erg/s/cm^2/A", "W/m^2/Hz", "erg/s/cm^2/Hz", "Jy",
            or "uJy". "u" represents "mu" meaning micro. Ignored if `model` is a
            Tabulation.
        xunits (str, optional): Units for the x-axis.
            Options are: "um", "nm", "A", or "Hz". "u" represents "mu" meaning
            micro. Ignored if `model` is a Tabulation.
        sun_range (float, optional): Distance from Sun to target in AU.
        solar_f (bool, optional): True to divide by pi, providing solar F
            instead of solar flux density.

    Returns:
        float: The mean solar flux density or solar F within the filter bandpass.

    Note:
        If the bandpass of the filter is wider than the wavelength coverage
        of the selected solar model, the computation will be restricted to the
        wavelength range that is in common between the filter and the model.
    """

    # Create a boxcar filter Tabulation
    bandpass = tab.Tabulation((center - width/2., center + width/2.), (1., 1.))

    # Return the mean over the filter
    return bandpass_flux_density(bandpass, model=model, units=units,
                                 xunits=xunits, sun_range=sun_range,
                                 solar_f=solar_f)

#===============================================================================
def bandpass_f(bandpass, model='STIS_Rieke', *, units='W/m^2/um', xunits='um',
               sun_range=1.):
    """
    Compute the solar F averaged over a filter bandpass.

    Args:
        bandpass (Tabulation or tuple): The Tabulation of the filter bandpass,
            with wavelength in units specified by `xunits` (if `model` is a
            string) or in the same units as `model` (if `model` is a
            Tabulation). Alternatively, a tuple of two arrays (wavelength,
            fraction), each of the same size.
        model (str or Tabulation, optional): Name of the model. Alternatively, a
            Tabulation of the solar flux density, already in the desired units.
        units (str, optional): Units for the flux.
            Options are: "W/m^2/um", "W/m^2/nm", "W/m^2/A", "erg/s/cm^2/um",
            "erg/s/cm^2/nm", "erg/s/cm^2/A", "W/m^2/Hz", "erg/s/cm^2/Hz", "Jy",
            or "uJy". "u" represents "mu" meaning micro. Ignored if `model` is a
            Tabulation.
        xunits (str, optional): Units for the x-axis.
            Options are: "um", "nm", "A", or "Hz". "u" represents "mu" meaning
            micro. Ignored if `model` is a Tabulation.
        sun_range (float, optional): Distance from Sun to target in AU.

    Returns:
        float: The mean solar F within the filter bandpass.

    Note:
        If the bandpass of the filter is wider than the wavelength coverage
        of the selected solar model, the computation will be restricted to the
        wavelength range that is in common between the filter and the model.
    """

    return bandpass_flux_density(bandpass, model=model, units=units,
                                 xunits=xunits, sun_range=sun_range,
                                 solar_f=True)

#===============================================================================
def mean_f(center, width, model='STIS_Rieke', *, units='W/m^2/um', xunits='um',
           sun_range=1.):
    """
    Compute average solar F over the bandpass of a "boxcar" filter.

    Args:
        center (float): The center of the bandpass (microns).
        width (float): The full width of the bandpass (microns).
        model (str or Tabulation, optional): Name of the model. Alternatively, a
            Tabulation of the solar flux density, already in the desired units.
        units (str, optional): Units for the flux.
            Options are: "W/m^2/um", "W/m^2/nm", "W/m^2/A", "erg/s/cm^2/um",
            "erg/s/cm^2/nm", "erg/s/cm^2/A", "W/m^2/Hz", "erg/s/cm^2/Hz", "Jy",
            or "uJy". "u" represents "mu" meaning micro. Ignored if `model` is a
            Tabulation.
        xunits (str, optional): Units for the x-axis.
            Options are: "um", "nm", "A", or "Hz". "u" represents "mu" meaning
            micro. Ignored if `model` is a Tabulation.
        sun_range (float, optional): Distance from Sun to target in AU.

    Returns:
        float: The mean solar flux density or solar F within the filter
        bandpass.

    Note:
        If the bandpass of the filter is wider than the wavelength coverage
        of the selected solar model, the computation will be restricted to the
        wavelength range that is in common between the filter and the model.
    """

    return mean_flux_density(center, width, model=model, units=units,
                             xunits=xunits, sun_range=sun_range, solar_f=True)

################################################################################
