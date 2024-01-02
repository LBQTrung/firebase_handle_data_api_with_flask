from flask import Flask
from flask import jsonify

app = Flask(__name__)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Config firebase admin
cred = credentials.Certificate("firestore.json")
firebase_app = firebase_admin.initialize_app(cred)
db = firestore.client()

# import numpy for calc statistic index
import numpy as np


# Use for check all data
@app.route("/")
def index():
    esp32_ref = db.collection("testco")
    docs = esp32_ref.get()

    # doc_ref = users_ref.document("test30")
    data = [doc.to_dict() for doc in docs]

    return jsonify(data)


#  Use for update time data
@app.route("/update")
def update():
    esp32_ref = db.collection("testco")
    docs = esp32_ref.get()

    esp32_ref.document(f"testdo0").update({"create_at": 1703425857})

    time = 1703425857

    for i in range(len(docs)):
        if i > 0:
            time += 2700
            esp32_ref.document(f"testdo{i}").update({"create_at": time})

    return {"Status": "Cập nhật thành công"}


# ======== API for realtime temparature =======
@app.route("/mean-temperature")
def calc_mean_temperature():
    esp32_ref = db.collection("testco")
    docs = esp32_ref.get()
    data = [doc.to_dict()["temperature"] for doc in docs]

    return {"mean-temperature": round(np.mean(data), 2)}


@app.route("/sd-temperature")
def calc_sd_temperature():
    esp32_ref = db.collection("testco")
    docs = esp32_ref.get()
    data = [doc.to_dict()["temperature"] for doc in docs]

    return {"mean-temperature": round(np.std(data), 2)}


@app.route("/min-temperature")
def calc_min_temperature():
    esp32_ref = db.collection("testco")
    docs = esp32_ref.get()
    data = [doc.to_dict()["temperature"] for doc in docs]

    return {"mean-temperature": float(np.min(data))}


@app.route("/max-temperature")
def calc_max_temperature():
    esp32_ref = db.collection("testco")
    docs = esp32_ref.get()
    data = [doc.to_dict()["temperature"] for doc in docs]

    return {"mean-temperature": float(np.max(data))}


# ======== API for realtime humidity =======

if __name__ == "__main__":
    app.run(debug=True)
