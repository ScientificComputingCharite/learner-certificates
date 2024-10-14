import pandas
from pathlib import Path
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "data", nargs="+", type=Path,
        help="semicolon separated file containing email "
        "address and name of attendees")
    parser.add_argument(
        "-o", "--output", type=Path,
        help="write out overall list of attendees")
    parser.add_argument(
        "-a", "--attendance", type=int, default=75,
        help="percentage attendance, default 75")
    args = parser.parse_args()

    if args.attendance < 0 or args.attendance > 100:
        parser.error("attendance must be in range 0 - 100")
    minSess = round(len(args.data) * args.attendance/100)

    data = []
    for p in args.data:
        data.append(pandas.read_csv(p, sep=";", names=["email", "name"]))
    data = pandas.concat(data).sort_values("email")
    # count the number of sessions
    nsess = data.groupby("email").count().rename(columns={"name": "nSession"})
    # associated names with email
    names = data.drop_duplicates("email").set_index("email")
    # put data together
    data = pandas.concat([nsess, names], axis=1).reset_index()
    # sort by attendance and name
    data = data.sort_values(["nSession", "email"])
    # drop rows where attendance is below minimum attendance
    data = data.drop(data[data.nSession < minSess].index)

    result = data.to_csv(columns=["nSession", "email", "name"], index=False)

    if args.output is not None:
        args.output.write_text(result)
    else:
        print(result)


if __name__ == "__main__":
    main()
