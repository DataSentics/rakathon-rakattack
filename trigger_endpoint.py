import os
import requests
import numpy as np
import pandas as pd
import json


def create_tf_serving_json(data):
    return {
        "inputs": (
            {name: data[name].tolist() for name in data.keys()}
            if isinstance(data, dict)
            else data.tolist()
        )
    }

def score_model(dataset):
    url = "https://adb-6675301098417980.0.azuredatabricks.net/serving-endpoints/5y_cancer_mortality_at_diagnosis/invocations"
    headers = {
        "Authorization": f"Bearer dapi9eeafe5d7ccaa279efba5b87bea42875-2",
        "Content-Type": "application/json",
    }
    ds_dict = (
        {"dataframe_split": dataset.to_dict(orient="split")}
        if isinstance(dataset, pd.DataFrame)
        else create_tf_serving_json(dataset)
    )
    data_json = json.dumps(ds_dict, allow_nan=True)
    response = requests.request(method="POST", headers=headers, url=url, data=data_json)
    if response.status_code != 200:
        raise Exception(f"Request failed with status {response.status_code}, {response.text}")
    return response.json()


if __name__ == "__main__":
    dataset = pd.read_csv("test_data.csv")
    score_model(dataset)
