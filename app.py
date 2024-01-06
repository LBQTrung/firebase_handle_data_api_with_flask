from flask import Flask
from flask import jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Config firebase admin
cred = credentials.Certificate("firestore2.json")
firebase_app = firebase_admin.initialize_app(cred)
db = firestore.client()

esp32_ref = db.collection("testco")
docs = esp32_ref.get()

# import numpy for calc statistic index
import numpy as np


# Use for check all data
@app.route("/")
def index():
    # doc_ref = users_ref.document("test30")
    data = [doc.to_dict() for doc in docs]

    return jsonify(data)


@app.route("/test")
def test():
    return "test cho biết"


#  Use for update time data
@app.route("/update")
def update():
    esp32_ref = db.collection("testco")
    docs = esp32_ref.get()
    esp32_ref.document(f"testdo0").update({"create_at": 1703430600})

    time = 1703430600

    for i in range(len(docs)):
        if i > 0:
            time += 1800
            esp32_ref.document(f"testdo{i}").update({"create_at": time})

    return {"Status": "Cập nhật thành công"}


# Fake data for development
@app.route("/fake-data")
def fake_data():
    time = 1703425857

    for i in range(323):
        if i > 0:
            time += 2700

            fake_data = {
                "temperature": random.randint(17, 25),
                "humidity": random.randint(89, 95),
                "create_at": time,
            }

            esp32_ref.document(f"test{i}").set(fake_data)
    return "Fake thành công"


# ======== API for realtime temparature =======
@app.route("/statistic-temp")
def calc_statistic_temperature():
    data = [doc.to_dict()["temperature"] for doc in docs]

    return {
        "mean": round(np.mean(data), 2),
        "std": round(np.std(data), 2),
        "min": float(np.min(data)),
        "max": float(np.max(data)),
    }


# ======== API for realtime humidity =======
@app.route("/statistic-humidity")
def calc_statistic_humidity():
    data = [doc.to_dict()["humidity"] for doc in docs]

    return {
        "mean": round(np.mean(data), 2),
        "std": round(np.std(data), 2),
        "min": float(np.min(data)),
        "max": float(np.max(data)),
    }


# ======== API for Line Graph =======
@app.route("/line-graph-temp")
def get_data_for_line_graph_temperature():
    dict_data = [doc.to_dict() for doc in docs]
    # Sort dictionary according to create_at
    dict_data.sort(key=lambda x: x["create_at"])

    labels = [data["create_at"] for data in dict_data]
    data = [data["temperature"] for data in dict_data]
    return {"labels": labels, "data": data}


@app.route("/line-graph-humidity")
def get_data_for_line_graph_humidity():
    dict_data = [doc.to_dict() for doc in docs]
    # Sort dictionary according to create_at
    dict_data.sort(key=lambda x: x["create_at"])

    labels = [data["create_at"] for data in dict_data]
    data = [data["humidity"] for data in dict_data]
    return {"labels": labels, "data": data}


# ======== API for Bar Chart =======
@app.route("/bar-chart-temp")
def get_data_for_bar_chart_temperature():
    dict_data = [doc.to_dict() for doc in docs]
    temperature_list = [data["temperature"] for data in dict_data]
    freq = {}
    for temperature in temperature_list:
        if temperature in freq:
            freq[temperature] += 1
        else:
            freq[temperature] = 1

    sorted_data = dict(sorted(freq.items(), key=lambda item: int(item[0])))
    return {"labels": list(sorted_data.keys()), "data": list(sorted_data.values())}


@app.route("/bar-chart-humidity")
def get_data_for_bar_chart_humidity():
    dict_data = [doc.to_dict() for doc in docs]
    humidity_list = [data["humidity"] for data in dict_data]
    freq = {}
    for humidity in humidity_list:
        if humidity in freq:
            freq[humidity] += 1
        else:
            freq[humidity] = 1

    sorted_data = dict(sorted(freq.items(), key=lambda item: int(item[0])))
    return {"labels": list(sorted_data.keys()), "data": list(sorted_data.values())}


if __name__ == "__main__":
    app.run(debug=True)
