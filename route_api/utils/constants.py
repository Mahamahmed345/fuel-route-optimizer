from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

CSV_FILE = BASE_DIR / "data" / "fuel-prices.csv"

MAX_VEHICLE_RANGE_MILES = 500

VEHICLE_MPG = 10