from route_api.utils.csv_loader import get_fuel_dataframe

def get_stations_by_state(state):
    dataframe = get_fuel_dataframe()
    return dataframe[
        dataframe["State"] == state
    ]

def get_stations_by_city(city):
    dataframe = get_fuel_dataframe()
    return dataframe[
        dataframe["City"].str.upper() == city.upper()
    ]

def find_cheapest_station(city=None, state=None):
    dataframe = get_fuel_dataframe()
    dataframe["City"] = dataframe["City"].astype(str).str.strip()
    dataframe["State"] = dataframe["State"].astype(str).str.strip()
    if city:
        city_stations = dataframe[
            dataframe["City"].str.upper() == city.upper().strip()
        ]
        if not city_stations.empty:
            cheapest = city_stations.loc[
                city_stations["Retail Price"].idxmin()
            ]

            station = cheapest.to_dict()
            station["match_type"] = "city"

            return station
    if state:
        state_stations = dataframe[
            dataframe["State"].str.upper() == state.upper().strip()
        ]
        if not state_stations.empty:
            cheapest = state_stations.loc[
                state_stations["Retail Price"].idxmin()
            ]
            station = cheapest.to_dict()
            station["match_type"] = "state_fallback"

            return station

    return None