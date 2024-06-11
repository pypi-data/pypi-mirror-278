import argparse
import csv
from datetime import date
from datetime import timedelta
from io import StringIO
from requests import get
from time import sleep

MAX_TRIP_COUNT_PER_REQUEST = 100_000

DEFAULT_DOCK_FIELD_NAMES = [
    "Dock Id",
    "Status",
    "Bus Position",
    "Holds Defective Bike",
    "Idle",
    "Last Activity",
    "Need Checkup",
    "Last Checkup Date",
    "Total Use Since Last Checkup",
    "Number of failed bike lock attempts",
    "Charging",
    "Station Id",
]

# excludes "Created By" and "Last Modified By"
DEFAULT_STATION_FIELD_NAMES = [
    "Station Id",
    # "Public Identifier (OBCN)",
    "Name",
    "Status",
    "Expected Station Size",
    "Latitude",
    "Longitude",
    "Altitude",
    "Landmark",
    "Address",
    "Address 2",
    "City",
    "Zip Code",
    "Street Intersection",
    "Creation Date",
    "Modification Date",
    "Nearby Station Distance",
    # "Test Station",
    "Blocked Status",
    # "Deleted",
    "Total Usage",
    "Type",
    "No Connection",
    "Voltage",
    "Battery Level",
    "Reorder Needed",
    # "Planned Date",
    # "Partner Station Id",
    # "Group Station Id",
    # "Cluster Id",
    # "Crown Id",
    # dynamically added
    "Location",
]


def get_first_day_of_month(dt):
    return dt.replace(day=1)


def get_last_day_of_previous_month(dt):
    return get_first_day_of_month(dt) - timedelta(days=1)


def get_first_day_of_previous_month(dt):
    return get_first_day_of_month(get_last_day_of_previous_month(dt))


class PBSC:
    def __init__(self, base, username, password, api_key):
        self.base = base
        self.api_key = api_key
        self.auth = (username, password)
        self.default_count = 100_000

    def export_docks(self, filepath):
        url = self.base + "/v1/docks/export"
        params = {"count": self.default_count}

        res = get(
            url, auth=self.auth, headers={"X-API-KEY": self.api_key}, params=params
        )

        # test that res is actually a csv
        with StringIO(res.text) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if len(rows) == 0:
            raise Exception("[pbsc] parsed zero docks")

        # see https://stackoverflow.com/questions/3191528/csv-in-python-adding-an-extra-carriage-return-on-windows
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=DEFAULT_DOCK_FIELD_NAMES)
            writer.writeheader()
            writer.writerows(
                [
                    dict([(field, row[field]) for field in DEFAULT_DOCK_FIELD_NAMES])
                    for row in rows
                ]
            )

    def _get_stations(self):
        url = self.base + "/v1/stations/export"
        params = {
            "count": self.default_count,
            "portable": "false",
            "hideTestAssets": "true",
            "alerts": "false",
        }

        res = get(
            url, auth=self.auth, headers={"X-API-KEY": self.api_key}, params=params
        )

        # test that res is actually a csv
        with StringIO(res.text) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if len(rows) == 0:
            raise Exception("[pbsc] parsed zero stations")

        # filter rows
        rows = [
            row
            for row in rows
            if row["Test Station"] != "true" and row["Deleted"] != "true"
        ]

        # add location column, which helps with publishing to Socrata
        rows = [
            {**row, "Location": f"POINT({row['Longitude']} {row['Latitude']})"}
            for row in rows
        ]

        return rows

    def export_stations(self, filepath):
        rows = self._get_stations()

        # see https://stackoverflow.com/questions/3191528/csv-in-python-adding-an-extra-carriage-return-on-windows
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=DEFAULT_STATION_FIELD_NAMES)
            writer.writeheader()
            writer.writerows(
                [
                    dict([(field, row[field]) for field in DEFAULT_STATION_FIELD_NAMES])
                    for row in rows
                ]
            )

    def export_trips(self, filepath, end=None, buffer_period=0, wait=30):
        stations = self._get_stations()

        station_id_to_location = dict(
            [(station["Station Id"], station["Location"]) for station in stations]
        )

        if end is None:
            end = date.today() - timedelta(days=buffer_period)

        start = get_first_day_of_month(end)
        print(f"[pbsc] current period {start}:{end}")

        for i in range(1000):
            start = get_first_day_of_month(end)

            url = self.base + "/v1/trips/export"

            params = {
                "count": MAX_TRIP_COUNT_PER_REQUEST,
                # period applies to 'Start Time' field
                # period end date is inclusive
                "period": f"{date.strftime(start, '%Y-%m-%d')}:{date.strftime(end, '%Y-%m-%d')}",
            }
            print("[pbsc] params:", params)

            if i != 0:
                print(f"[pbsc] waiting {wait} seconds before next request")
                sleep(wait)

            res = get(
                url, auth=self.auth, headers={"X-API-KEY": self.api_key}, params=params
            )

            with StringIO(res.text) as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames + [
                    "Start Station Location",
                    "End Station Location",
                ]
                rows = list(reader)

            # to-do: make this more sophisticated in order to avoid breaking when there's a random month of data missing
            if len(rows) == 0:
                break

            # add locations
            rows = [
                {
                    **row,
                    "Start Station Location": station_id_to_location.get(
                        row["Start Station Id"], None
                    ),
                    "End Station Location": station_id_to_location.get(
                        row["End Station Id"], None
                    ),
                }
                for row in rows
            ]

            # flip rows, so going from latest to earliest
            rows.reverse()

            print(
                f"[pbsc] range of rows: {rows[0]['Start Time']} ... {rows[-1]['Start Time']}"
            )
            print(f"[pbsc] number of rows: {len(rows)}")

            if len(rows) == MAX_TRIP_COUNT_PER_REQUEST:
                raise Exception(
                    f"[pbsc] Uh Oh. Hit Max Trip Count per Request of {MAX_TRIP_COUNT_PER_REQUEST}"
                )

            if i == 0:
                print("[pbsc] writing the following csv header:", fieldnames)
                # see https://stackoverflow.com/questions/3191528/csv-in-python-adding-an-extra-carriage-return-on-windows
                with open(filepath, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()

            print("[pbsc] adding trips to csv")
            # see https://stackoverflow.com/questions/3191528/csv-in-python-adding-an-extra-carriage-return-on-windows
            with open(filepath, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerows(rows)

            start = get_first_day_of_previous_month(start)
            end = get_last_day_of_previous_month(end)
            print(f"[pbsc] changed period to {start}:{end}")


def main():
    parser = argparse.ArgumentParser(
        prog="pbsc",
        description="High-Level API Client for Public Bike System Company",
    )
    parser.add_argument(
        "method",
        help='method to run, can be "export-docks", "export-stations", or "export-trips"',
    )
    parser.add_argument(
        "outpath", help="output filepath of where to save downloaded CSV"
    )
    parser.add_argument(
        "--base",
        type=str,
        help='base url for the API, like "https://example.publicbikesystem.net/operation/data"',
    )
    parser.add_argument("--username", type=str, help="username")
    parser.add_argument("--password", type=str, help="password")
    parser.add_argument("--api-key", type=str, help="API key")
    args = parser.parse_args()
    print("args:", args)

    client = PBSC(
        base=args.base,
        username=args.username,
        password=args.password,
        api_key=args.api_key,
    )
    print("initialized client")

    if args.method in ["export-docks", "export_docks"]:
        client.export_docks(args.outpath)
    elif args.method in ["export-stations", "export_stations"]:
        client.export_stations(args.outpath)
    elif args.method in ["export-trips", "export_trips"]:
        client.export_trips(args.outpath)


if __name__ == "__main__":
    main()
