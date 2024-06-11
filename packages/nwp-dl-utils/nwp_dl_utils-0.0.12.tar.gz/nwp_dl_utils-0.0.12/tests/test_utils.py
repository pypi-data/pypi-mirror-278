import numpy as np
import nwp_dl_utils.utils as utils
import xarray as xr


def test_get_indices_at_coordinates_latlon():
    # test with meps
    url = "https://thredds.met.no/thredds/dodsC/mepslatest/meps_lagged_6_h_latest_2_5km_latest.nc"  # noqa: E501
    with xr.open_dataset(url) as ds:
        xindices, yindices = utils.get_indices_at_coordinates(
            ds, [60.0, 61.0], [10.0, 9.0]
        )
        np.testing.assert_array_equal(xindices, np.array([390, 437]))
        np.testing.assert_array_equal(yindices, np.array([313, 295]))


def test_get_indices_at_coordinates_rlatrlon():
    # test with mywavewam
    url = "https://thredds.met.no/thredds/dodsC/fou-hi/mywavewam800mhf/mywavewam800_midtnorge.an.2023020518.nc"  # noqa: E501
    with xr.open_dataset(url) as ds:
        xindices, yindices = utils.get_indices_at_coordinates(
            ds, [1.9, 1.8], [12.5, 12.4], fields="rlatrlon"
        )
        np.testing.assert_array_equal(xindices, np.array([538, 525]))
        np.testing.assert_array_equal(yindices, np.array([71, 59]))
