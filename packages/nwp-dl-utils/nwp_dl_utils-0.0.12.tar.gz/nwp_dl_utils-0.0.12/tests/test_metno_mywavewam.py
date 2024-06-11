import numpy as np
import nwp_dl_utils.metno.mywavewam as mywavewam
import pandas as pd


def test_load_to_sequences():
    ts = [
        pd.to_datetime("2017-12-21T00:00:00Z"),
        pd.to_datetime("2017-12-23T00:00:00Z"),
    ]
    lats = [58.8806, 58.12]
    lons = [10.2103, 10.01]
    data = mywavewam.load_to_sequences([ts, ts], [lats, lats], [lons, lons])
    # print(data)

    # {
    #     "wind_speed": [4.611094951629639, 14.10683536529541],
    #     "wind_to_direction": [125.25358581542969, 61.2672004699707],
    #     "sea_surface_wave_significant_height": [0.6463204622268677, 2.772052526473999],
    #     "sea_surface_wave_to_direction": [39.521060943603516, 56.39546203613281],
    #     "sea_surface_wave_peak_period_from_variance_spectral_density": [
    #         5.209823131561279,
    #         6.934274196624756,
    #     ],
    # }

    wind_speed = np.array([4.611094951629639, 14.10683536529541])
    wind_to_direction = np.array([125.25358581542969, 61.2672004699707])
    sea_surface_wave_significant_height = np.array(
        [0.6463204622268677, 2.772052526473999]
    )
    sea_surface_wave_to_direction = np.array([39.521060943603516, 56.39546203613281])
    sea_surface_wave_peak_period_from_variance_spectral_density = np.array(
        [
            5.209823131561279,
            6.934274196624756,
        ]
    )

    np.testing.assert_almost_equal(data[0]["wind_speed"], wind_speed)
    np.testing.assert_almost_equal(data[0]["wind_to_direction"], wind_to_direction)
    np.testing.assert_almost_equal(
        data[0]["sea_surface_wave_significant_height"],
        sea_surface_wave_significant_height,
    )
    np.testing.assert_almost_equal(
        data[0]["sea_surface_wave_to_direction"], sea_surface_wave_to_direction
    )
    np.testing.assert_almost_equal(
        data[0]["sea_surface_wave_peak_period_from_variance_spectral_density"],
        sea_surface_wave_peak_period_from_variance_spectral_density,
    )
