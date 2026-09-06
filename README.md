# datafun-02-automation

Classifying penguin body mass with Python control flow.

[![Python 3.14](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](./pyproject.toml)
[![uv managed](https://img.shields.io/badge/uv-managed-DE5FE9)](https://docs.astral.sh/uv/)
[![MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](./LICENSE)

## The Problem

The Palmer Penguins dataset has 344 observations across three species.
Given a single body mass reading with no species label attached, can a
simple threshold rule tell you anything useful about the penguin?

This project answers that with loops, branching, and a classification
rule built from the sample mean.

## Why Body Mass

The example project classified bill length. Bill length is a single
broad distribution centered near 44 mm, so a threshold split just
carves an arbitrary line through one hump.

Body mass behaves differently. The species averages are:

| Species | Mean body mass (g) |
|---|---|
| Adelie | 3,700.7 |
| Chinstrap | 3,733.1 |
| Gentoo | 5,076.0 |

Adelie and Chinstrap are nearly identical. Gentoo is about 1,350 grams
heavier. That gap makes the overall distribution bimodal, so a
threshold rule lands on a real boundary rather than an arbitrary one.

![Distribution of body mass](docs/images/measurement-distribution.png)

The two humps in the chart are the light species cluster and the
Gentoo cluster.

## The Classification Rule

Thresholds are calculated from the sample mean of 4,201.8 g:

- **LIGHT** - below 0.85 x mean (3,571.5 g)
- **AVERAGE** - between the two thresholds
- **HEAVY** - above 1.15 x mean (4,832.0 g)

The example used 0.9 and 1.1. Those bands are too narrow for a
measurement with this spread and would push most of the sample into
the outer categories. Widening to 0.85 and 1.15 produces:

| Band | Count | Share |
|---|---|---|
| LIGHT | 89 | 26% |
| AVERAGE | 172 | 50% |
| HEAVY | 81 | 24% |

The heavy threshold at 4,832 g sits just under the Gentoo mean, so in
practice HEAVY is a Gentoo detector built from one number and two
comparisons.

## What the Code Does

1. Loads `data/penguins.csv` into a pandas DataFrame
2. Inspects shape, columns, and the first rows
3. Loops over species and logs the mean body mass for each
4. Transforms column names with a list comprehension
5. Calculates thresholds and classifies against them
6. Counts how many observations land in each band
7. Streams 15 records on a one second delay, classifying each
8. Saves a distribution chart to `docs/images/`

Every step writes to `project.log`.

## Handling Missing Data

Row 4 of the dataset has no measurements at all. The streaming loop
checks for it explicitly:

```python
if pd.isna(current_measurement):
    stream_class: str = "MISSING"
elif current_measurement < light_threshold:
    stream_class = "LIGHT"
```

Without that first branch a NaN falls through every comparison and
gets silently labeled AVERAGE, which would be wrong. Two of the 344
rows are affected.

## Run It

```shell
git clone https://github.com/jgdavis24/datafun-02-automation
cd datafun-02-automation
code .
```

Then in a VS Code terminal:

```shell
uv sync
uv run python -m datafun.app
```

A successful run ends with:

```shell
END main() - Executed successfully!
```

## Project Layout

- `data/` - the penguins CSV
- `docs/` - documentation and generated charts
- `src/datafun/` - application code
- `tests/` - pytest suite
- `pyproject.toml` - dependencies and tool config

## Techniques Used

pandas DataFrames, `for` loops, `while` loops, list comprehensions,
`if`/`elif`/`else` branching, boolean masking for counts, NaN
handling, matplotlib visualization, structured logging, type hints,
and `Final` constants.

## Data Source

Palmer Penguins, collected by Dr. Kristen Gorman at Palmer Station,
Antarctica. See [docs/data-card.md](docs/data-card.md).

## License

MIT. See [LICENSE](LICENSE).
