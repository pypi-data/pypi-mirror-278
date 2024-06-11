"""
Load NWP Data and Dump to CSV.
"""

import argparse
import datetime
import logging

import nwp_dl_utils.metno.meps as meps
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
        "-o", "--output", default="nwp.csv", type=str, help="Output File"
    )
    parser.add_argument("--lat", default=53.546111, type=float, help="Latitude")
    parser.add_argument("--lon", default=9.966111, type=float, help="Longitude")
    parser.add_argument(
        "--start", default="2022-07-29", type=str, help="Start Date (Inclusive)"
    )
    parser.add_argument(
        "--end", default="2022-07-31", type=str, help="End Date (Exclusive)"
    )
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    logging.info("CLI Arguments: %s" % args)
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load and Ingest Timestamps
    timestamps = pd.date_range(start=args.start, end=args.end, freq="6H")
    timestamps = timestamps[:-1]
    records, columns = meps.load_to_records_multiple_forecasts(
        timestamps, args.lat, args.lon
    )

    logging.info("Loading into Dataframe")
    df = pd.DataFrame.from_records(records, columns=columns)
    logging.info("Writing to %s" % args.output)
    df.to_csv(args.output, index=False)

    logging.info("Done")


if __name__ == "__main__":
    main()
