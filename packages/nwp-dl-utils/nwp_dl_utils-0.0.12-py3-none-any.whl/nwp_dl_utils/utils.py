import logging
from typing import List, Tuple, Union

import numpy as np
import numpy.typing as npt
import pandas as pd
import pyresample
import xarray as xr


def get_indices_at_coordinates(
    ds: xr.Dataset,
    lats_req: Union[List[pd.Timestamp], npt.NDArray],
    lons_req: Union[List[pd.Timestamp], npt.NDArray],
    fields: str = "latlon",
) -> Tuple[npt.NDArray, npt.NDArray]:
    """
    use a kdtree to find the nearest neighbours to the requested coordinates
    (lats_req,lon_req) on the (lat,lon) grid included in the nwp product. works for
    multiples (lat,lon). see also https://stackoverflow.com/a/40044540.

    for example, if you pass lats_req = [60,60] and lons_req = [10,10], you get
    back [387,387] and [328,328]

    if `fields` = "latlon", we will look into the latitude and longitude matrices. we
    usually use this when working with the MEPS products from MetNo

    if `fields` = "latlon_short", we will look into the lat and long matrices. we usually use
    this when working with the NorKyst800m products from MetNo

    if `fields` = "rlatrlon", we will look into the rlat and rlon arrays. we usually
    use this when working with the MyWaveWAM products from MetNo

    :param ds: xarray NWP product dataset
    :param lats_req: ndarray/list of requested latitudes
    :param lons_req: ndarray/list of requested longitudes
    :param fields: string of either `latlon` or `rlatrlon`
    :returns: list of x and y indices into NWP array
    :rtype: tuple
    """

    # load grids
    if fields == "latlon":
        lon_grid = ds["longitude"][:].data  # 2D array
        lat_grid = ds["latitude"][:].data  # 2D array
    if fields == "latlon_short":
        lon_grid = ds["lon"][:].data  # 2D array
        lat_grid = ds["lat"][:].data  # 2D array
    elif fields == "rlatrlon":
        rlon = ds["rlon"][:].data  # 1D array
        rlat = ds["rlat"][:].data  # 1D array
        lon_grid, lat_grid = np.meshgrid(rlon, rlat)
    else:
        raise Exception("Invalid Coordinate Fields.")

    grid = pyresample.geometry.GridDefinition(lons=lon_grid, lats=lat_grid)
    swath = pyresample.geometry.SwathDefinition(lons=lons_req, lats=lats_req)

    # nearest neighbours (wrt great circle distance) in the grid
    _, _, index_array, distance_array = pyresample.kd_tree.get_neighbour_info(
        source_geo_def=grid,
        target_geo_def=swath,
        radius_of_influence=50000,
        neighbours=1,
    )

    # unflatten the indices
    index_array_2d = np.unravel_index(index_array, grid.shape)
    # print(index_array_2d)
    # print(index_array_2d[0][0])
    # print(index_array_2d[1][0])
    # print(lon_grid[387, 328]) # correct
    # print(lon_grid[328, 387]) # wrong
    # print(lat_grid[387, 328]) # correct
    # print(lat_grid[328, 387]) # wrong
    # sys.exit()

    # return
    xindices = index_array_2d[0]
    yindices = index_array_2d[1]
    return xindices, yindices


def get_indices_at_time(
    ds: xr.Dataset, ts_req: Union[List[pd.Timestamp], npt.NDArray]
) -> List[int]:
    """
    :param ds: xarray dataset
    :param ts_req: ndarray/list of requested timestamps
    :return indices: ndarray/list of indices for timestamps
    :rtype: list
    """
    ts = pd.to_datetime(ds["time"].data, origin="unix", unit="s", utc=True)
    tindices = []
    for kk in range(len(ts_req)):
        try:
            tidx = np.argwhere(ts_req[kk] == ts)[0][0]
        except IndexError:
            logging.warning("Requested Timestamp Not Found. Using Nearest Available.")
            tidx = np.argmin(np.abs(ts - pd.to_datetime(ts_req[kk])))
            logging.warning(
                "Requested: %s / Nearest Available: %s"
                % (pd.to_datetime(ts_req[kk]), ts[tidx])
            )
        tindices.append(tidx)
    return tindices
