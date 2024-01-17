import pandas as pd
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import LabelEncoder
from model import  Recommender, mse_with_l2
from joblib import load
from flask import Flask, request

app = Flask(__name__)

game_data = pd.read_csv("game-data.csv", usecols=["id", "thumbnail", "primary", "average"])
game_data = game_data.sort_values(by='average', ascending=False)
NUM_ITEMS = 15

item_matrix = tf.keras.models.load_model("recommender.keras").X

item_encoder = LabelEncoder()
item_encoder.fit([])
temp_encoder = load("itemencoder.joblib")
item_encoder.classes_ = temp_encoder.classes_



keys = item_encoder.inverse_transform(range(item_matrix.shape[0]))
game_data = game_data[game_data['id'].isin(keys)]




ratings = {}

def genericRecommendations():
    top_items = game_data.head(NUM_ITEMS)
    return {
        'thumbnail': list(top_items['thumbnail']),
        'id': list(top_items['id']),
        'rating': [ratings[x] if x in ratings else 5 for x in list(top_items['id'])]
    }

@app.route('/getresults', methods=["POST"])
def GetResults():
    query = request.get_json(force=True)["query"].lower()
    result = game_data[game_data["primary"].str.lower().apply(lambda x : x.startswith(query))]

    top_items = result.head(NUM_ITEMS)
    return {
        'thumbnail': list(top_items['thumbnail']),
        'id': list(top_items['id']),
        'rating': [ratings[x] if x in ratings else 5 for x in list(top_items['id'])]
        }

@app.route('/updaterating', methods=["POST"])
def UpdateRating():
    global ratings
    data = request.get_json(force=True)
    ratings[data["id"]] = float(data["rating"])
    return {}

@app.route('/getrecommendations', methods=["GET"])
def GetRecommendations():
    global ratings
    if not ratings:
        return genericRecommendations()
    
    indices = []
    rating_array = []
    for key, item in ratings.items():
        indices.append(item_encoder.transform([key])[0])
        rating_array.append(item - game_data[game_data['id'] == key]['average'].iloc[0])

    b = tf.cast(tf.constant(rating_array, shape=(len(rating_array), 1)), dtype=tf.float32)
    A = tf.gather(item_matrix, indices)
    x = tf.linalg.lstsq(A, b, l2_regularizer=0.0001)

    predictions = tf.matmul(item_matrix, x).numpy().flatten()

    for i in range(len(predictions)):
        average = game_data[game_data['id'] == keys[i]]['average']
        if len(average) > 0:
            predictions[i] += average.iloc[0]
        else:
            predictions[i] = -100

    sorted_indices = np.flip(np.argsort(predictions))
    ids = item_encoder.inverse_transform(sorted_indices[:NUM_ITEMS])
    games = game_data[game_data['id'].isin(ids)]

    return {
        'thumbnail': list(games['thumbnail']),
        'id': list(games['id']),
        'rating': [ratings[x] if x in ratings else 5 for x in list(games['id'])]
    }
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

