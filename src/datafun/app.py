"""src/datafun/app.py - Project script.

Author: Josiah Davis
Date: 2026-09-06

HOW TO RUN THIS FILE:

Open a terminal in the root project folder and run:

uv run python -m datafun.app

DOMAIN:

Palmer Penguins. 344 observations of three penguin species across
three islands in the Palmer Archipelago, Antarctica.
See docs/data-card.md for details.

WHAT THIS DOES:

Loads the dataset, inspects its shape, then uses Python control flow
to classify penguins by body mass against thresholds calculated from
the sample mean. Every step is logged to project.log.

ORGANIZATION:

Execution begins in main(). Supporting functions live in
src/datafun/utils_data.py.
"""

# === IMPORTS ===

import logging
from pathlib import Path
import time
from typing import Final

from datafun_toolkit.logger import get_logger, log_header, log_path
from eda_vizkit import save_chart, show_numeric_distribution
import matplotlib.pyplot as plt
import pandas as pd

from datafun.utils_data import inspect

# === LOGGER ===

LOG: logging.Logger = get_logger("P02", level="DEBUG")

# === PATHS ===

DATA_FILE_PATH: Final[Path] = Path("data") / "penguins.csv"

# === WHAT ONE ROW REPRESENTS ===

GRAIN: Final[str] = "one penguin"

# === GROUPING COLUMN ===

GROUP_COLUMN: Final[str] = "species"

WHY_THIS_GROUP: Final[str] = r"""
Species has only three unique values, so a for loop can process each
one without the output becoming unreadable. Island would also work,
but species is the variable that actually drives the physical
measurements in this dataset.
"""

# === MEASUREMENT COLUMN ===

MEASUREMENT_COLUMN: Final[str] = "body_mass_g"

WHY_THIS_MEASUREMENT: Final[str] = r"""
Body mass separates the three species more cleanly than the bill
measurements do. Gentoo penguins are substantially heavier than
Adelie and Chinstrap, so the distribution is not one hump around a
single average. Classifying against the mean actually splits the data
into groups that correspond to something real.

Scale is the other reason. Bill length runs 32 to 60 mm, a range of
27 around a mean of 44. Body mass runs 2700 to 6300 grams, a range of
3600 around a mean near 4200. The wider relative spread means the
threshold bands land on meaningful differences instead of rounding
error.
"""

# === CLASSIFICATION THRESHOLDS ===

# Wider bands than the 0.9 / 1.1 used for bill length. Body mass has a
# larger spread, so a 10 percent window would classify most of the
# sample as LIGHT or HEAVY and leave the middle band nearly empty.
# 0.85 and 1.15 put the cutoffs near 3600 g and 4800 g, which lands
# roughly between the Adelie and Chinstrap cluster and the Gentoo one.

LIGHT_THRESHOLD_MULTIPLIER: Final[float] = 0.85
HEAVY_THRESHOLD_MULTIPLIER: Final[float] = 1.15


def main() -> None:
    """Entry point when running this file as a script.

    Arguments: None.
    Returns: None.
    """
    log_header(LOG, "P02")

    LOG.info("===================================")
    LOG.info("START main()")
    LOG.info("===================================")

    LOG.info("-------------------------------")
    LOG.info("01. LOAD the data.")
    LOG.info("-------------------------------")

    log_path(LOG, "data file", path=DATA_FILE_PATH)

    df: pd.DataFrame = pd.read_csv(DATA_FILE_PATH)

    LOG.info("Data loaded successfully.")

    LOG.info("-------------------------------")
    LOG.info("02. INSPECT the data.")
    LOG.info("-------------------------------")

    inspection_string: str = inspect(df=df, grain=GRAIN, log=LOG)

    LOG.info(inspection_string)

    LOG.info("-------------------------------")
    LOG.info("03. REPEAT logic using a for loop.")
    LOG.info("-------------------------------")

    column_names: list[str] = df.columns.tolist()

    for name in column_names:
        LOG.info(f"Column name: {name}")

    LOG.info(f"Selected group column: {GROUP_COLUMN}")
    LOG.info(f"Reason for choosing this group: {WHY_THIS_GROUP}")

    unique_list: list[str] = df[GROUP_COLUMN].unique().tolist()

    for item in unique_list:
        LOG.info(f"Item: {item}")

    # Log the mean measurement for each species so the threshold choices
    # below can be checked against the actual group averages.
    for species in unique_list:
        species_mean: float = df.loc[
            df[GROUP_COLUMN] == species, MEASUREMENT_COLUMN
        ].mean()
        LOG.info(f"Mean {MEASUREMENT_COLUMN} for {species}: {round(species_mean, 1)}")

    LOG.info("-------------------------------")
    LOG.info("04. TRANSFORM one list to another list.")
    LOG.info("-------------------------------")

    capitalized_column_names: list[str] = [name.upper() for name in column_names]
    LOG.info(f"Capitalized column names: {capitalized_column_names}")

    LOG.info("-------------------------------")
    LOG.info("05. BRANCH based on conditions.")
    LOG.info("-------------------------------")

    LOG.info(f"Selected measurement column: {MEASUREMENT_COLUMN}")
    LOG.info(f"Reason for choosing this measurement: {WHY_THIS_MEASUREMENT}")

    minimum: float = df[MEASUREMENT_COLUMN].min()
    maximum: float = df[MEASUREMENT_COLUMN].max()
    mean: float = df[MEASUREMENT_COLUMN].mean()
    LOG.info(f"{MEASUREMENT_COLUMN} - Minimum: {minimum}")
    LOG.info(f"{MEASUREMENT_COLUMN} - Maximum:  {maximum}")
    LOG.info(f"{MEASUREMENT_COLUMN} - Mean:     {round(mean, 1)}")
    LOG.info("-------------------------------")

    sample_index: int = 0
    sample_reading: float = df[MEASUREMENT_COLUMN].iloc[sample_index]
    LOG.info(f"Sample {MEASUREMENT_COLUMN}: {sample_reading}")

    LOG.info(f"Light threshold multiplier: {LIGHT_THRESHOLD_MULTIPLIER}")
    LOG.info(f"Heavy threshold multiplier: {HEAVY_THRESHOLD_MULTIPLIER}")

    light_threshold: float = LIGHT_THRESHOLD_MULTIPLIER * mean
    heavy_threshold: float = HEAVY_THRESHOLD_MULTIPLIER * mean

    LOG.info(f"Light threshold: {round(light_threshold, 1)}")
    LOG.info(f"Heavy threshold: {round(heavy_threshold, 1)}")

    if sample_reading < light_threshold:
        classification_string: str = "LIGHT"
    elif sample_reading > heavy_threshold:
        classification_string: str = "HEAVY"
    else:
        classification_string: str = "AVERAGE"

    LOG.info(f"First row {MEASUREMENT_COLUMN} classification: {classification_string}")

    # Count how many penguins fall in each band so the thresholds can be
    # judged on the whole sample instead of one row.
    light_count: int = int((df[MEASUREMENT_COLUMN] < light_threshold).sum())
    heavy_count: int = int((df[MEASUREMENT_COLUMN] > heavy_threshold).sum())
    average_count: int = (
        int(df[MEASUREMENT_COLUMN].notna().sum()) - light_count - heavy_count
    )

    LOG.info(f"LIGHT count:   {light_count}")
    LOG.info(f"AVERAGE count: {average_count}")
    LOG.info(f"HEAVY count:   {heavy_count}")

    LOG.info("-------------------------------")
    LOG.info("06. REPEAT while a condition is true.")
    LOG.info("-------------------------------")

    # Simulate a stream by reading one measurement at a time on a delay.
    # 15 records instead of 10 so the classification runs across more of
    # the opening rows and the LIGHT band shows up repeatedly.

    MAX_RECORDS: Final[int] = 15
    STREAM_WAIT_SECONDS: Final[int] = 1

    LOG.info("Starting to process measurements periodically...")
    LOG.info(f"Max records to process: {MAX_RECORDS}")
    LOG.info(f"Stream wait seconds: {STREAM_WAIT_SECONDS}")

    count: int = 0
    LOG.info(f"Current count: {count}")

    while count < MAX_RECORDS:
        current_measurement: float = df[MEASUREMENT_COLUMN].iloc[count]

        # Classify each streamed reading, not just the first row.
        if pd.isna(current_measurement):
            stream_class: str = "MISSING"
        elif current_measurement < light_threshold:
            stream_class = "LIGHT"
        elif current_measurement > heavy_threshold:
            stream_class = "HEAVY"
        else:
            stream_class = "AVERAGE"

        LOG.info(
            f"Current {MEASUREMENT_COLUMN}: {current_measurement} -> {stream_class}"
        )

        count += 1
        LOG.info(f"Updated count: {count}")

        time.sleep(STREAM_WAIT_SECONDS)

    LOG.info("-------------------------------")
    LOG.info("07. VISUALIZE the selected measurement.")
    LOG.info("-------------------------------")

    LOG.info("Creating a chart to visualize the selected measurement.")

    CHART_PATH = Path("docs/images/measurement-distribution.png")

    ax = show_numeric_distribution(
        df,
        column=MEASUREMENT_COLUMN,
    )

    save_chart(ax, CHART_PATH)
    LOG.info(f"Chart saved successfully at {CHART_PATH}.")

    LOG.info(
        "IMPORTANT: Close chart window to continue by clicking its X or close button."
    )
    plt.show()

    LOG.info("===================================")
    LOG.info("END main() - Executed successfully!")
    LOG.info("===================================")


if __name__ == "__main__":
    main()
