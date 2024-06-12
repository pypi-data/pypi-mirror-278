################################################################################
# tests/test_solar.py
################################################################################

import numpy as np
import unittest
import solar
import tabulation as tab


NAMES = ['STIS_Rieke', 'stis', 'RIEKE', 'Kurucz', 'Colina']
UNITS = list(solar.UNIT_DICT.keys())
XUNITS = list(solar.XUNIT_DICT.keys())


class TestSolar(unittest.TestCase):
    def test_flux_density(self):
        # We test that all models agree with each other, but don't actually test
        # that any of the models are "correct".
        # Testing every possible combination of units doesn't seem strictly
        # necessary, but it doesn't take too long.
        for unit in UNITS:
            for xunit in XUNITS:
                model0 = solar.flux_density(NAMES[0], units=unit, xunits=xunit,
                                            sun_range=1., solar_f=False)
                for name in NAMES[1:]:
                    model1 = solar.flux_density(name, units=unit, xunits=xunit,
                                                sun_range=1., solar_f=False)
                    model0a = model0.subsample(model1.x)
                    model1a = model1.subsample(model0a.x)

                    model0a = model0a.trim()
                    model1a = model1a.trim()

                    (min0, max0) = model0a.domain()
                    (min1, max1) = model1a.domain()

                    test_min = max(min0, min1)
                    test_max = min(max0, max1)

                    self.assertTrue(test_min < test_max)

                    model0a = model0a.clip(test_min, test_max)
                    model1a = model1a.clip(test_min, test_max)

                    diffs = 2 * np.abs(model1a.y - model0a.y) / (model0a.y + model1a.y)
                    median_diff = np.median(diffs)

                    self.assertTrue(median_diff < 0.02)

        for name in NAMES:
            model0 = solar.flux_density(name, sun_range=1., solar_f=False)
            model1 = solar.flux_density(name, sun_range=9., solar_f=False) * 81.
            model2 = solar.flux_density(name, sun_range=1., solar_f=True) * np.pi

            self.assertTrue(np.allclose(model0.y, model1.y, rtol=1e-15, atol=1e-15))
            self.assertTrue(np.allclose(model0.y, model2.y, rtol=1e-15, atol=1e-15))

            model0 = solar.flux_density(name, units='W/m^2/um')
            model1 = solar.flux_density(name, units='W/m^2/nm') * 1.e3
            model2 = solar.flux_density(name, units='W/m^2/A') * 1.e4

            with self.assertRaises(ValueError):
                solar.flux_density(name, units='Fred')
            with self.assertRaises(ValueError):
                solar.flux_density(name, xunits='Fred')

            self.assertTrue(np.allclose(model0.y, model1.y, rtol=1e-15, atol=1e-15))
            self.assertTrue(np.allclose(model0.y, model2.y, rtol=1e-15, atol=1e-15))

            model1 = solar.flux_density(name, units='erg/s/cm^2/um') * 1.e-7 * 1.e4
            self.assertTrue(np.allclose(model0.y, model1.y, rtol=1e-15, atol=1e-15))

            model0 = solar.flux_density(name, units='W/m^2/Hz')
            model1 = solar.flux_density(name, units='erg/s/cm^2/Hz') * 1.e-7 * 1.e4
            model2 = solar.flux_density(name, units='Jy') / 1.e26
            model3 = solar.flux_density(name, units='uJy') / 1.e32

            self.assertTrue(np.allclose(model0.y, model1.y, rtol=1e-15, atol=1e-15))
            self.assertTrue(np.allclose(model0.y, model2.y, rtol=1e-15, atol=1e-15))
            self.assertTrue(np.allclose(model0.y, model3.y, rtol=1e-15, atol=1e-15))

        with self.assertRaises(ValueError):
            solar.flux_density('Fred')

    def test_bandpass_flux_density(self):
        bandpass = tab.Tabulation((0, 1000), (1, 1))
        # Integral of full fake model is 0.16,
        # mean is 0.16 / 0.5 = 0.32
        bfd = solar.bandpass_flux_density(bandpass, model='_fake', solar_f=True)
        self.assertAlmostEqual(bfd, 0.32)

        # Integral of fake model over [0.18, 0.19] is 0.01,
        # mean is 0.01 / 0.01 = 1
        bandpass = tab.Tabulation((0.18, 0.19), (1, 1))
        bfd = solar.bandpass_flux_density(bandpass, model='_fake', solar_f=True)
        self.assertAlmostEqual(bfd, 1)

        bfd = solar.bandpass_flux_density(((0.18, 0.19), (1, 1)), model='_fake',
                                          solar_f=True)
        self.assertAlmostEqual(bfd, 1)

        bfd = solar.bandpass_flux_density(bandpass, model='_fake', solar_f=True,
                                          units='W/m^2/nm')
        self.assertAlmostEqual(bfd, 1/1000)

        bfd = solar.bandpass_flux_density(bandpass, model='_fake', solar_f=True,
                                          sun_range=2)
        self.assertAlmostEqual(bfd, 1/4)

        bfd = solar.bandpass_flux_density(((180, 190), (1, 1)), model='_fake',
                                          xunits='nm', solar_f=True)
        self.assertAlmostEqual(bfd, 1)

        # Integral of fake model over [0.58, 0.62] is 0.04,
        # mean is 0.04 / 0.04 = 1
        # The smaller bandpass doesn't change the answer, because the
        # BFD is normalized to the bandpass integral
        bandpass = tab.Tabulation((0.58, 0.62), (.5, .5))
        bfd = solar.bandpass_flux_density(bandpass, model='_fake', solar_f=True)
        self.assertAlmostEqual(bfd, 1)

        bandpass = tab.Tabulation((0.17, 0.19), (1., 1.))
        model = tab.Tabulation(np.array([0.15, 0.16, 0.17, 0.18, 0.19, 0.20]),
                               np.array([1., 2., 3., 4., 5., 6.]))
        bfd = solar.bandpass_flux_density(bandpass, model=model, solar_f=False)
        self.assertAlmostEqual(bfd, 4)

    def test_mean_flux_density(self):
        # Integral of full fake model is 0.16,
        # mean is 0.16 / 0.5 = 0.32
        mfd = solar.mean_flux_density(500, 1000, model='_fake', solar_f=True)
        self.assertAlmostEqual(mfd, 0.32)

        # Integral of fake model over [0.18, 0.19] is 0.01,
        # mean is 0.01 / 0.01 = 1
        mfd = solar.mean_flux_density(0.185, 0.01, model='_fake', solar_f=True)
        self.assertAlmostEqual(mfd, 1)

        mfd = solar.mean_flux_density(0.185, 0.01, model='_fake', solar_f=True,
                                      units='W/m^2/nm')
        self.assertAlmostEqual(mfd, 1/1000)

        mfd = solar.mean_flux_density(0.185, 0.01, model='_fake', solar_f=True,
                                      sun_range=2)
        self.assertAlmostEqual(mfd, 1/4)

        mfd = solar.mean_flux_density(185, 10, model='_fake',
                                      xunits='nm', solar_f=True)
        self.assertAlmostEqual(mfd, 1)

        # Integral of fake model over [0.58, 0.62] is 0.04,
        # mean is 0.04 / 0.04 = 1
        mfd = solar.mean_flux_density(0.6, 0.04, model='_fake', solar_f=True)
        self.assertAlmostEqual(mfd, 1)
        mfd = solar.mean_flux_density(0.6, 0.04, model='_fake')
        self.assertAlmostEqual(mfd, np.pi)

        model = tab.Tabulation(np.array([0.15, 0.16, 0.17, 0.18, 0.19, 0.20]),
                               np.array([1., 2., 3., 4., 5., 6.]))
        mfd = solar.mean_flux_density(0.18, 0.02, model=model, solar_f=False)
        self.assertAlmostEqual(mfd, 4)

    def test_bandpass_f(self):
        bandpass = tab.Tabulation((0, 1000), (1, 1))
        # Integral of full fake model is 0.16,
        # mean is 0.16 / 0.5 = 0.32
        bf = solar.bandpass_f(bandpass, model='_fake')
        self.assertAlmostEqual(bf, 0.32)

        # Integral of fake model over [0.18, 0.19] is 0.01,
        # mean is 0.01 / 0.01 = 1
        bandpass = tab.Tabulation((0.18, 0.19), (1, 1))
        bf = solar.bandpass_f(bandpass, model='_fake')
        self.assertAlmostEqual(bf, 1)

        bf = solar.bandpass_f(((0.18, 0.19), (1, 1)), model='_fake')
        self.assertAlmostEqual(bf, 1)

        bf = solar.bandpass_f(bandpass, model='_fake', units='W/m^2/nm')
        self.assertAlmostEqual(bf, 1/1000)

        bf = solar.bandpass_f(bandpass, model='_fake', sun_range=2)
        self.assertAlmostEqual(bf, 1/4)

        bf = solar.bandpass_f(((180, 190), (1, 1)), model='_fake', xunits='nm')
        self.assertAlmostEqual(bf, 1)

        # Integral of fake model over [0.58, 0.62] is 0.04,
        # mean is 0.04 / 0.04 = 1
        # The smaller bandpass doesn't change the answer, because the
        # bf is normalized to the bandpass integral
        bandpass = tab.Tabulation((0.58, 0.62), (.5, .5))
        bf = solar.bandpass_f(bandpass, model='_fake')
        self.assertAlmostEqual(bf, 1)

        bandpass = tab.Tabulation((0.17, 0.19), (1., 1.))
        model = tab.Tabulation(np.array([0.15, 0.16, 0.17, 0.18, 0.19, 0.20]),
                               np.array([1., 2., 3., 4., 5., 6.]))
        bf = solar.bandpass_f(bandpass, model=model)
        self.assertAlmostEqual(bf, 4/np.pi)

    def test_mean_f(self):
        # Integral of full fake model is 0.16,
        # mean is 0.16 / 0.5 = 0.32
        mf = solar.mean_f(500, 1000, model='_fake')
        self.assertAlmostEqual(mf, 0.32)

        # Integral of fake model over [0.18, 0.19] is 0.01,
        # mean is 0.01 / 0.01 = 1
        mf = solar.mean_f(0.185, 0.01, model='_fake')
        self.assertAlmostEqual(mf, 1)

        mf = solar.mean_f(0.185, 0.01, model='_fake', units='W/m^2/nm')
        self.assertAlmostEqual(mf, 1/1000)

        mf = solar.mean_f(0.185, 0.01, model='_fake', sun_range=2)
        self.assertAlmostEqual(mf, 1/4)

        mf = solar.mean_f(185, 10, model='_fake', xunits='nm')
        self.assertAlmostEqual(mf, 1)

        # Integral of fake model over [0.58, 0.62] is 0.04,
        # mean is 0.04 / 0.04 = 1
        mf = solar.mean_f(0.6, 0.04, model='_fake')
        self.assertAlmostEqual(mf, 1)

        model = tab.Tabulation(np.array([0.15, 0.16, 0.17, 0.18, 0.19, 0.20]),
                               np.array([1., 2., 3., 4., 5., 6.]))
        mf = solar.mean_f(0.18, 0.02, model=model)
        self.assertAlmostEqual(mf, 4/np.pi)


########################################

if __name__ == '__main__':  # pragma: no cover
    unittest.main(verbosity=2)

################################################################################
