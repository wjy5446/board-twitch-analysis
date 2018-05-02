from util import db
from util import viewship

from flask import Flask, render_template, request, jsonify
import logging
import pickle
from twitch import TwitchClient

import numpy as np
import pandas as pd
import gensim
from gensim.models import Word2Vec
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

# template가 변경될 때마다 Reload
app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD = True,
)

# Load models
database = {}
models = {}

def init():
    with open("../model/stream2vec.p", "rb") as f:
        models["stream2vec"] = pickle.load(f)

    database["stream_info_db"] = db.load_db()

init()

##############################################################################
# index
@app.route("/")
def index():
    return render_template("index.html")

# api
@app.route("/info/", methods = ["POST"])
def recommand_streamer():
    model = models["stream2vec"]

    if request.method == "POST":
        stream_name_input = request.values.get("streamer_id")

        # id가 리스트에 있는 지 확인]
        if db.exist_by_name(database["stream_info_db"], stream_name_input):
            stream_id_input = db.get_id_by_name(database["stream_info_db"], stream_name_input)

            most_similar_streamers = model.most_similar(str(stream_id_input), topn=12)
            most_similar_streamers_info = []
            client = TwitchClient(client_id="jh0fr7g4isys0t2fmviygsvk7ez3l9")

            # get main streamer
            channel = client.channels.get_by_id(stream_id_input)
            streamer_info = {
                "mature": channel["mature"],
                "partner" : channel["partner"],
                "status": channel["status"],
                "display_name": channel["display_name"],
                "game": channel["game"],
                "language": channel["language"],
                "created_at": channel["created_at"],
                "updated_at": channel["updated_at"],
                "logo": channel["logo"],
                "url": channel["url"],
                "views": channel["views"],
                "followers": channel["followers"],
            }

            # get main streamer recent viewship
            df_viewship = viewship.get_viewship(stream_id_input, stream_name_input)
            best_game = viewship.get_best_game_by_viewer(df_viewship)
            best_hour = viewship.get_best_hour_by_viewer(df_viewship)

            viewer_value = list(df_viewship.viewer.astype("str").values)
            time_value = list(((df_viewship.time - pd.datetime(1970,1,1)).dt.total_seconds() * 1000).astype("str").values)

            data_viewship = {
                "viewer" : viewer_value,
                "time" : time_value,
                "best_game" : best_game,
                "best_hour" : best_hour,
            }


            # get similar_streamers
            for idx in range(len(most_similar_streamers)):
                try:
                    channel = client.channels.get_by_id(most_similar_streamers[idx][0])
                    smiliar_streamer_info = {
                            "similar_rate" : round(most_similar_streamers[idx][1] * 100, 0),
                            "display_name" : channel["display_name"],
                            "name" :  channel["name"],
                            "image" : channel["logo"],
                            "game" : channel["game"],
                            "followers" : channel["followers"],
                            "views" : channel["views"],
                            "link" : channel["url"],
                    }
                    most_similar_streamers_info.append(smiliar_streamer_info)
                except Exception as e:
                    pass

            result = {
                "status" : 200,
                "result_main" : streamer_info,
                "result_similar" : list(most_similar_streamers_info),
                "viewship" : data_viewship
            }

        else:
            result = {
                    "status" : 202,
            }
    else:
        result = {
            "status" : 201
        }

    return jsonify(result)

###############################################################################
# app run
if __name__ == "__main__":
    app.run(debug=True)
