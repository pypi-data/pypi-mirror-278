import datetime
import logging

import numpy as np
import pandas as pd
import xarray as xr

from ..utils import get_indices_at_coordinates


def _construct_url(ts):
    # https://thredds.met.no/thredds/dodsC/meps25epsarchive/2022/08/01/meps_det_2_5km_20220801T06Z.nc
    baseurl = "https://thredds.met.no/thredds/dodsC/meps25epsarchive"
    basefile = "meps_det_2_5km"
    url = "%s/%04d/%02d/%02d/%s_%04d%02d%02dT%02dZ.nc" % (
        baseurl,
        ts.year,
        ts.month,
        ts.day,
        basefile,
        ts.year,
        ts.month,
        ts.day,
        ts.hour,
    )
    return url


def _load_diff_and_backfill(ds, ts, variable, xidx, yidx):
    """
    deals with variables that are accumulated

    these are bit annoying to deal with because the first value will be "no data" (as
    there's nothing accumulated from the hour before)

    so we
    1/ change the first to zero
    2/ take the diff (because it's accumulated)
    3/ put back the initial zero (np.diff shortens the array by one)
    4/ backfill the first value from the previous forecast file
    """

    accumulated = ds[variable][:6, 0, yidx, xidx].data
    accumulated[0] = 0.0
    differenced = np.diff(accumulated)
    differenced = np.concatenate([[0.0], differenced])
    # now do the backfill
    ts_minus_6hours = ts - datetime.timedelta(hours=6)
    url_minus_6hours = _construct_url(ts_minus_6hours)
    try:
        with xr.open_dataset(url_minus_6hours) as ds2:
            logging.debug("Backfilling `%s` from %s" % (variable, url_minus_6hours))
            accumulated2 = ds2[variable][:7, 0, yidx, xidx].data
            accumulated2[0] = 0.0
            differenced2 = np.diff(accumulated2)
            differenced2 = np.concatenate([[0.0], differenced2])
            differenced[0] = differenced2[-1]
    except IOError as e:
        logging.error(
            "IOError During Backfill. Setting Value for '%s' to NaN." % variable
        )
        logging.error(e)
        differenced[0] = np.nan

    return differenced


def load_to_records_single_forecast(
    url, ts, latitude, longitude, variables_direct, variables_diff_and_backfill
):
    # intermedita data structures
    data_direct = {}
    data_diff_and_backfill = {}

    # setup some lists that we return anyway
    records = []
    columns = []
    for variable in variables_direct:
        columns.append(variable)
    for variable in variables_diff_and_backfill:
        columns.append(variable)

    # load data and do processing
    try:
        with xr.open_dataset(url) as ds:
            # find indices of target coordinates
            xindices, yindices = get_indices_at_coordinates(ds, [latitude], [longitude])
            xidx = xindices[0]
            yidx = yindices[0]
            logging.debug(
                "Nearest Neighbour NWP Cell: (lat,lon) = (%.2f,%.2f)"
                % (
                    ds["latitude"][yidx, xidx].data,
                    ds["longitude"][yidx, xidx].data,
                ),
            )

            # process variables that do not need any post-processing
            logging.debug("Loading Variables (Direct)")
            for variable in variables_direct:
                if variable == "time":
                    data = ds[variable][:6].data
                else:
                    data = ds[variable][:6, 0, yidx, xidx].data
                data_direct[variable] = data

            # process variables that need differencing and backfilling
            logging.debug("Loading Variables (Differencing/Backfilling)")
            for variable in variables_diff_and_backfill:
                data = _load_diff_and_backfill(
                    ds,
                    ts,
                    variable,
                    xidx,
                    yidx,
                )
                data_diff_and_backfill[variable] = data

            # append to list of records
            logging.debug("Appending to List of Records for Bulk Insert")
            for kk in range(len(data_direct["time"])):
                record = ()
                for variable, data in data_direct.items():
                    if variable == "time":
                        record += (pd.Timestamp(data[kk]),)
                    else:
                        record += (data[kk],)
                for variable, data in data_diff_and_backfill.items():
                    record += (data[kk],)
                records.append(record)
    except IOError as e:
        logging.error("IOErrror during Direct Ingestion. Skipping Product.")
        logging.error(e)

    # return stuff
    return records, columns


def load_to_records_multiple_forecasts(timestamps, latitude, longitude):
    # define the variables from the NWP product we care about
    # first those that we can just load
    variables_direct = [
        "time",
        "air_temperature_0m",
        "air_temperature_2m",
        "cloud_area_fraction",
        "cloud_base_altitude",
        "cloud_top_altitude",
        "fog_area_fraction",
        "rainfall_amount",
        "relative_humidity_2m",
        "precipitation_type",
        "surface_downwelling_shortwave_flux_in_air",
        "surface_downwelling_longwave_flux_in_air",
        "wind_speed",
        "wind_direction",
        "wind_speed_of_gust",
    ]
    # now those that are accumulated during the run (and thus need to be differenced)
    variables_diff_and_backfill = [
        "integral_of_surface_direct_normal_irradiance_wrt_time",
        "integral_of_surface_downwelling_shortwave_flux_in_air_wrt_time",
        "integral_of_surface_downwelling_longwave_flux_in_air_wrt_time",
        "integral_of_toa_downwelling_shortwave_flux_wrt_time",
        "precipitation_amount_acc",
    ]
    records = []
    for ts in timestamps:
        url = _construct_url(ts)
        logging.info("Processing %s" % ts)
        logging.debug("Loading %s" % url)
        records_loc, columns = load_to_records_single_forecast(
            url, ts, latitude, longitude, variables_direct, variables_diff_and_backfill
        )
        records.extend(records_loc)
    return records, columns
