"""
Get Bulk Data from Norkyst800m.

Call Signature
$ python ./get_norkyst800m_bulk.py \
    --locations locations.csv \
    --timestamps timestamps.csv \
    --output norkyst800m_sequences.csv

Where
$ cat locations.csv
location_id,latitude,longitude
98.59.371235,5.216333
99,69.70953,18.363983

$ cat timestamps.csv
timestamp
2023-10-21T00:00:00Z
2023-12-23T00:00:00Z
2024-01-02T00:00:00Z

$ cat norkyst800m_bulk.csv
timestamp,latitude,longitude,temperature,salinity
2023-10-21 00:00:00+00:00,59.371235,5.216333,12.00999927520752,33.13999938964844
2023-10-21 00:00:00+00:00,69.70953,18.363983,8.460000038146973,33.72100067138672
2023-12-23 00:00:00+00:00,59.371235,5.216333,8.359999656677246,34.04199981689453
2023-12-23 00:00:00+00:00,69.70953,18.363983,5.059999942779541,33.946998596191406
2024-01-02 00:00:00+00:00,59.371235,5.216333,7.199999809265137,33.073001861572266
2024-01-02 00:00:00+00:00,69.70953,18.363983,4.460000038146973,33.970001220703125
"""

import argparse
import datetime
import logging

import nwp_dl_utils.metno.norkyst800m as norkyst800m
import pandas as pd


def main():
    # Logging
    logging.basicConfig(
        level=logging.INFO,
        format=f"%(asctime)s - %(levelname)s - %(name)s - %(threadName)s - %(message)s",
    )
    logging.Formatter.formatTime = (
        lambda self, record, datefmt=None: datetime.datetime.fromtimestamp(
            record.created, datetime.timezone.utc
        )
        .astimezone()
        .isoformat(sep=" ", timespec="seconds")
    )
    logger = logging.getLogger()

    # Parse Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--output",
        default="norkyst800m_bulk.csv",
        type=str,
        help="Output file.",
    )
    parser.add_argument(
        "-l",
        "--locations",
        default="locations.csv",
        type=str,
        help="Locations for which to load data.",
    )
    parser.add_argument(
        "-t",
        "--timestamps",
        default="timestamps.csv",
        type=str,
        help="Timestamps for which to load data.",
    )
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    logging.info("CLI Arguments: %s" % args)
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load and Format Locations
    logging.info("Reading Locations from %s" % args.locations)
    df_locations = pd.read_csv(args.locations)
    latitudes = df_locations.latitude.values
    longitudes = df_locations.longitude.values
    location_id = df_locations.location_id

    # Load and Format Timestamps
    logging.info("Reading Timestamps from %s" % args.timestamps)
    df_timestamps = pd.read_csv(args.timestamps, parse_dates=["timestamp"])
    timestamps = [
        pd.to_datetime(ts, utc=True) for ts in list(df_timestamps.timestamp.values)
    ]

    # Some Info
    logging.info(
        "Read %i Locations and %i Timestamps." % (len(df_locations), len(df_timestamps))
    )
    logging.info(
        "Retrieving %i Total Datapoints." % (len(df_timestamps) * len(df_locations))
    )

    # logging.info("Done")
    # timestamps = [
    #     pd.to_datetime("2023-12-01T00:00:00Z"),
    #     pd.to_datetime("2023-12-23T00:00:00Z"),
    #     pd.to_datetime("2024-03-23T00:00:00Z"),
    # ]
    # lats = [59.371235, 69.70953]
    # lons = [5.216333, 18.363983]
    logging.info("Querying Data and Loading to Dataframe")
    df_output = norkyst800m.load_to_dataframe(
        timestamps, latitudes, longitudes, location_id
    )
    logging.info("Writing to %s" % args.output)
    df_output.to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
