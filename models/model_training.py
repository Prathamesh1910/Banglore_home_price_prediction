import os
import sys
import warnings
from urllib.parse import urlparse

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import pickle
import mlflow
from mlflow.models import infer_signature
import mlflow.sklearn

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

def eval_metrics(true, pred):
    return np.sqrt(mean_squared_error(true, pred)), mean_absolute_error(true, pred), r2_score(true, pred)


if __name__ == '__main__':
    warnings.filterwarnings("ignore")

    try:
        df = pd.read_csv('../data/bhp_data.csv')
    except Exception as e:
        logger.exception(
            "Unable to download training & test CSV, check your internet connection. Error: %s", e
        )

    df.drop(columns=['Unnamed: 0'], inplace = True)

    inputs = df.drop('price_per_sqft', axis = 'columns')
    target = df['price_per_sqft']

    x_train, x_test, y_train, y_test = train_test_split(inputs.values, target, test_size = 0.2)

    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0001
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.01


    with mlflow.start_run():
        model_en = ElasticNet(alpha = alpha, l1_ratio = l1_ratio)
        model_en.fit(x_train, y_train)

        y_pred1 = model_en.predict(x_train)
        y_pred2 = model_en.predict(x_test)

        (rmse_train, mae_train, r2_train) = eval_metrics(y_train, y_pred1)
        (rmse_test, mae_test, r2_test) = eval_metrics(y_test, y_pred2)

        print(f"with alpha = {alpha} and l1_ratio = {l1_ratio}")
        print(f"rmse_train = {rmse_train}, mae_train = {mae_train}, r2_train = {r2_train}")
        print(f"rmse_test = {rmse_test}, mae_test = {mae_test}, r2_test = {r2_test}")

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse_train", rmse_train)
        mlflow.log_metric("mae_train", mae_train)
        mlflow.log_metric("r2_train", r2_train)
        mlflow.log_metric("rmse_test", rmse_test)
        mlflow.log_metric("mae_test", mae_test)
        mlflow.log_metric("r2_test", r2_test)

        signature = infer_signature(x_train, y_pred1)

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        # Model registry does not work with file store
        if tracking_url_type_store != "file":
            # Register the model
            # There are other ways to use the Model Registry, which depends on the use case,
            # please refer to the doc for more information:
            # https://mlflow.org/docs/latest/model-registry.html#api-workflow
            mlflow.sklearn.log_model(
                model_en, "model", registered_model_name="ElasticnetWineModel"
            )
        else:
            mlflow.sklearn.log_model(model_en, "model")


    # with open('./artifacts/bhp_model_en.pickle', 'wb') as f:
    #     pickle.dump(model_en, f)
