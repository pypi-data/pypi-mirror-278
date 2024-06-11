"""
Download multiple days for MyWaveWAM product.
"""

import argparse
import datetime
import logging

import nwp_dl_utils.metno.mywavewam as mywavewam
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
        "-s", "--start", default="2019-01-01", help="First Day to Download."
    )
    parser.add_argument(
        "-r", "--region", default="midtnorge", help="Region to Download."
    )
    parser.add_argument(
        "-e", "--end", default="2019-01-02", help="Last Day to Download."
    )
    parser.add_argument("-b", "--basedir", default=".", help="Base Directory for Files")
    parser.add_argument("-f", "--force", action="store_true", default=False)
    parser.add_argument("-q", "--quiet", action="store_true", default=False)
    args = parser.parse_args()
    logging.info("CLI Arguments: %s" % args)

    # Build Date Range
    dates = pd.date_range(start=args.start, end=args.end)

    # Loop Dates
    for date in dates:
        date = date.strftime("%Y-%m-%d")
        logging.info("Downloading MyWaveWAM Product for %s." % date)
        _ = mywavewam.download_hourly_for_single_day(
            date, args.region, args.basedir, args.force, args.quiet
        )


if __name__ == "__main__":
    main()
