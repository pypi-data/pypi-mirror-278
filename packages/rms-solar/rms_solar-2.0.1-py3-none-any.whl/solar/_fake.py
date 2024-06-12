################################################################################
# solar/fake.py: Fake model for the solar flux density at 1 AU. Used for
# testing.
################################################################################

import numpy as np
import tabulation as tab

# Column 1 is wavelength in microns
# Column 2 is solar F (not flux density) at 1 AU in W/m^2/Hz

FAKE_ARRAY = np.array([
    0.16, 1,
    0.20, 1,
    0.2000000001, 1e-20,  # Tabulation does not like having 0 values in the
    0.5999999999, 1e-20,  # middle of the flux density array
    0.60, 2,
    0.66, 2
])

FAKE_ARRAY = FAKE_ARRAY.reshape(FAKE_ARRAY.size//2, 2)

FAKE_WAVELENGTH_MICRON = FAKE_ARRAY[:, 0]
FAKE_FLUX_PER_HZ = FAKE_ARRAY[:, 1] * np.pi  # Column is F, not pi*F

FLUX_DENSITY = tab.Tabulation(FAKE_WAVELENGTH_MICRON, FAKE_FLUX_PER_HZ)
UNITS = 'W/m^2/um'
XUNITS = 'um'

################################################################################
