import numpy as np
import logging
from pathlib import Path
import pickle
import json

__model = None
__data_columns = None
__least_locations = None
__locations = None
__area_type = None
__availability = None
path: Path = Path(__file__).parent.parent


def load_saved_artifacts():
    global __model
    global __data_columns
    global __least_locations
    global __locations
    global __area_type
    global __availability

    logging.info('Loading saved artifacts')

    with open(path.joinpath("models/artifacts/columns.json"), 'r') as f:
        __data_columns = json.load(f)['data_columns']

    with open(path.joinpath("models/artifacts/bhp_model_en.pickle"), 'rb') as f:
        __model = pickle.load(f)

    with open(path.joinpath("models/artifacts/least_locations1.json"), 'r') as f:
        __least_locations = json.load(f)['least_locations']

    with open(path.joinpath("models/artifacts/locations.json"), 'r') as f:
        __locations = json.load(f)['locations']

    with open(path.joinpath("models/artifacts/area_type.json"), 'r') as f:
        __area_type = json.load(f)["area_types"]

    with open(path.joinpath("models/artifacts/availability.json"), 'r') as f:
        __availability = json.load(f)['month_availability']

    logging.info('Artifacts loaded')


def get_locations():
    return __locations


def get_area_type():
    return __area_type


def get_availability():
    return __availability


def scale_params(size: int, total_sqft: float, bath: int, balcony: int) -> list:
    scaled_params = []

    min_size, max_size = 0.5, 9
    min_area, max_area = 296.0, 42000.0
    min_bath, max_bath = 1, 9
    min_balc, max_balc = 0, 3

    scaled_params.append(round((size - min_size) / (max_size - min_size), 4))
    scaled_params.append(round((total_sqft - min_area) / (max_area - min_area), 4))
    scaled_params.append(round((bath - min_bath) / (max_bath - min_bath), 4))
    scaled_params.append(round((balcony - min_balc) / (max_balc - min_balc), 4))

    return scaled_params


def predict_price(**kwargs) -> float:

    size, total_sqft, bath, balcony, area_type, location, month_availability = kwargs['size'], kwargs['total_sqft'], kwargs['bath'], kwargs['balcony'], \
                                                                               kwargs['area_type'], kwargs['location'], kwargs['month_availability']

    if location in __least_locations:
        location = 'Other'

    x = np.zeros(len(__data_columns))

    index1, index2, index3 = 0, 0, 0

    try:
        index1 = __data_columns.index(area_type.lower())
    except:
        None

    try:
        index2 = __data_columns.index(location.lower())
    except:
        None

    try:
        index3 = __data_columns.index(month_availability.lower())
    except:
        None

    scaled_params = scale_params(size, total_sqft, bath, balcony)

    x[0] = scaled_params[0]  # size
    x[1] = scaled_params[1]  # total_sqft (area)
    x[2] = scaled_params[2]  # bath
    x[3] = scaled_params[3]  # balcony

    if index1 > 0:
        x[index1] = 1
    if index2 > 0:
        x[index2] = 1
    if index3 > 0:
        x[index3] = 1

    return round(__model.predict([x])[0] * total_sqft / 100000, 2)


if __name__ == '__main__':
    load_saved_artifacts()
    print(predict_price(**{'size': 4, 'total_sqft': 1500.0, 'bath': 3, 'balcony': 4, 'area_type': 'Carpet Area', 'location': 'JP Nagar', 'month_availability': 'Jun'}))