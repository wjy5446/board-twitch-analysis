import requests
import pandas as pd
import numpy as np

def get_viewship(id, name):
    url = "https://www.twitchmetrics.net/c/" + str(id) + "-" + str(name) + "/recent_viewership_values"
    response = requests.get(url)

    df_recent_viewer = pd.DataFrame(columns = ["time", "viewer", "game"])
    df_recent_viewer.time = np.array(response.json())[:, 0]
    df_recent_viewer.viewer = np.array(response.json())[:, 1]
    df_recent_viewer.game = np.array(response.json())[:, 2]

    df_recent_viewer.time = df_recent_viewer.time.apply(lambda x : pd.to_datetime(x))
    df_recent_viewer.viewer = df_recent_viewer.viewer.astype("int64")
    df_recent_viewer["hour"] = df_recent_viewer.time.apply(lambda x : x.hour).astype("str")

    return df_recent_viewer


def get_best_game_by_viewer(data, rank = 5):
    tmp =  data.groupby(["game"])["viewer"].agg("mean").sort_values(ascending = False)[:rank].astype("str")
    return list(zip(tmp.index, tmp))
    
def get_best_hour_by_viewer(data, rank = 5):
    tmp = data.groupby(["hour"])["viewer"].agg("mean").sort_values(ascending = False)[:rank].astype("str")
    return list(zip(tmp.index, tmp))
