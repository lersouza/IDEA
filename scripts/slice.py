import argparse
import datetime
import logging
import os

logging.basicConfig(level=logging.INFO)


logger = logging.getLogger("slicer")


def main(args):
    path, _ = os.path.split(args.source)
    destination_path = os.path.join(path, f"sliced-{'-'.join(args.years)}.txt")

    slice_size = 0
    years_in_slice = list(map(int, args.years))

    logger.info(
        f"Slicing file {args.source} for years {years_in_slice}."
        f"Destination will be {destination_path}"
    )

    with open(destination_path, "w+") as target_file:
        with open(args.source, "r") as source_file:
            for line in source_file:
                review_date = line.split("******")[args.date_field]

                review_date = datetime.datetime.strptime(review_date, args.date_format)

                if review_date.year in years_in_slice:
                    target_file.write(line)
                    slice_size += 1

    logger.info(f"Done slicing. Slice size is {slice_size}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("source", type=str, help="The file to slice")
    parser.add_argument(
        "years", nargs="+", help="A list of years to consider in the slice"
    )

    parser.add_argument("--date_field", type=int, default=2, help="The date file index")
    parser.add_argument("--date_format", type=str, default="%Y-%m-%d %H:%M:%S", help="The date format in reviews")

    args = parser.parse_args()

    main(args)
