# Vaccination Slot Tracker

Find and alert if a new vaccination slot has been found on Doctolib.

## Installation

Use the package manager [poetry](https://python-poetry.org/) to install vaccine_tracker.

```shell
poetry install
```

## Usage 

Change the Doctolib `URL` constant in `main.py` according to your location and your status (priority, age, etc.)

```shell
python main.py
```

OS notification have been tested on macos only. Please check regularly the script output to ensure that you do not miss
a vaccination slot.
