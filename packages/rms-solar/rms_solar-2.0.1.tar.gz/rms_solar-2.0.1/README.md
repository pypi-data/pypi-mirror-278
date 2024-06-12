[![GitHub release; latest by date](https://img.shields.io/github/v/release/SETI/rms-solar)](https://github.com/SETI/rms-solar/releases)
[![GitHub Release Date](https://img.shields.io/github/release-date/SETI/rms-solar)](https://github.com/SETI/rms-solar/releases)
[![Test Status](https://img.shields.io/github/actions/workflow/status/SETI/rms-solar/run-tests.yml?branch=main)](https://github.com/SETI/rms-solar/actions)
[![Documentation Status](https://readthedocs.org/projects/rms-solar/badge/?version=latest)](https://rms-solar.readthedocs.io/en/latest/?badge=latest)
[![Code coverage](https://img.shields.io/codecov/c/github/SETI/rms-solar/main?logo=codecov)](https://codecov.io/gh/SETI/rms-solar)
<br />
[![PyPI - Version](https://img.shields.io/pypi/v/rms-solar)](https://pypi.org/project/rms-solar)
[![PyPI - Format](https://img.shields.io/pypi/format/rms-solar)](https://pypi.org/project/rms-solar)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/rms-solar)](https://pypi.org/project/rms-solar)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rms-solar)](https://pypi.org/project/rms-solar)
<br />
[![GitHub commits since latest release](https://img.shields.io/github/commits-since/SETI/rms-solar/latest)](https://github.com/SETI/rms-solar/commits/main/)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/SETI/rms-solar)](https://github.com/SETI/rms-solar/commits/main/)
[![GitHub last commit](https://img.shields.io/github/last-commit/SETI/rms-solar)](https://github.com/SETI/rms-solar/commits/main/)
<br />
[![Number of GitHub open issues](https://img.shields.io/github/issues-raw/SETI/rms-solar)](https://github.com/SETI/rms-solar/issues)
[![Number of GitHub closed issues](https://img.shields.io/github/issues-closed-raw/SETI/rms-solar)](https://github.com/SETI/rms-solar/issues)
[![Number of GitHub open pull requests](https://img.shields.io/github/issues-pr-raw/SETI/rms-solar)](https://github.com/SETI/rms-solar/pulls)
[![Number of GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed-raw/SETI/rms-solar)](https://github.com/SETI/rms-solar/pulls)
<br />
![GitHub License](https://img.shields.io/github/license/SETI/rms-solar)
[![Number of GitHub stars](https://img.shields.io/github/stars/SETI/rms-solar)](https://github.com/SETI/rms-solar/stargazers)
![GitHub forks](https://img.shields.io/github/forks/SETI/rms-solar)

# Introduction

`solar` is a Python module that provides solar flux density from a variety of
models. These models are currently supported:

| Name       | Wavelength range (microns) |
| ---------- | -------------------------- |
| Colina     | 0.1195 to 2.5              |
| Kurucz     | 0.15 to 300                |
| Rieke      | 0.2 to 30                  |
| STIS       | 0.1195 to 2.7              |
| STIS_Rieke | 0.1195 to 30               |

`solar` is a product of the [PDS Ring-Moon Systems Node](https://pds-rings.seti.org).

# Installation

The `solar` module is available via the `rms-solar` package on PyPI and can be
installed with:

    pip install rms-solar

# Getting Started

The `solar` module provides five functions:

- `flux_density`: Compute the flux density of a solar model in the specified units.
- `bandpass_flux_density`: Compute the average solar flux density over a filter bandpass.
- `mean_flux_density`: Compute average solar flux density over the bandpass of a "boxcar" filter.
- `bandpass_f`: Compute the solar F averaged over a filter bandpass.
- `mean_f`: Compute average solar F over the bandpass of a "boxcar" filter.

These functions take or return `Tabulation` objects. For more information on `Tabulation`
objects see the [`rms-tabulation`](https://github.com/SETI/rms-tabulation) package.

Details of each function are available in the [module documentation](https://rms-solar.readthedocs.io/en/latest/module.html).

Here is an example that plots the solar flux density for the visual range of 400
to 700 nm using the Rieke model at 2 AU in units of nm for wavelength and
W/m^2/nm for flux:

```python
import matplotlib.pyplot as plt
import solar

flux = solar.flux_density(model='rieke', xunits='nm', units='W/m^2/nm', solar_range=2)
flux = flux.clip(400, 700)
plt.plot(flux.x, flux.y)
plt.show()
```

# Contributing

Information on contributing to this package can be found in the
[Contributing Guide](https://github.com/SETI/rms-solar/blob/main/CONTRIBUTING.md).

# Links

- [Documentation](https://rms-solar.readthedocs.io)
- [Repository](https://github.com/SETI/rms-solar)
- [Issue tracker](https://github.com/SETI/rms-solar/issues)
- [PyPi](https://pypi.org/project/rms-solar)

# Licensing

This code is licensed under the [Apache License v2.0](https://github.com/SETI/rms-solar/blob/main/LICENSE).
