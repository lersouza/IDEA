import argparse
import csv
import logging
import os

from collections import defaultdict

from google_play_scraper import Sort, reviews_all
from google_play_scraper.features.reviews import reviews


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("downloader")


def handle_review_field(field):
    field = str(field)
    field = field.replace("*", "")
    field = field.replace("\r", "")
    field = field.replace("\n", "")

    return field


def main(args):
    logger.info(f"About to get reviews for {args.app_id}.")

    result = reviews_all(
        args.app_id,
        lang="pt",
        country="br",
        sort=Sort.NEWEST,
        sleep_milliseconds=150,
    )

    if not result:
        logger.info(f"Could not retrieve any review for {args.app_id}.")
        return

    dataset_location = os.path.join(args.output_dir, args.app_id)
    dataset_file = os.path.join(dataset_location, "reviews.txt")

    logger.info(f"Found {len(result)}. Dumping to {dataset_file}.")

    os.makedirs(dataset_location, exist_ok=True)

    with open(dataset_file, "w+") as output_file:
        columns = ["score", "content", "at", "reviewCreatedVersion"]
        skipped = defaultdict(int)

        for r_id, review in enumerate(result):
            if (
                "reviewCreatedVersion" not in review
                or not review["reviewCreatedVersion"]
            ):
                skipped["no_version"] += 1
                continue  # We skip reviews without a version

            row = [review[c] for c in columns]

            if not all(row):
                skipped["empty_field"] += 1
                continue  # We skip any review with empty fields

            line = "******".join(map(handle_review_field, row))

            output_file.write(line)
            output_file.write("\n")

        logger.info(f"Skipped reviews: {skipped}")

    logger.info(f"Done writing.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("app_id")
    parser.add_argument("--output_dir", default="../dataset/")

    args = parser.parse_args()

    main(args)