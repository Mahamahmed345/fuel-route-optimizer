import pandas as pd

from .constants import CSV_FILE

import pandas as pd

from .constants import CSV_FILE

fuel_price_dataframe = pd.read_csv(CSV_FILE)
fuel_price_dataframe["Retail Price"] = (
    fuel_price_dataframe["Retail Price"]
      .astype(str)
      .str.replace("$", "", regex=False)
      .astype(float)
)


def get_fuel_dataframe():
    return fuel_price_dataframe