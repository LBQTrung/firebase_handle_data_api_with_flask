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


@app.route("/")
def index():
    users_ref = db.collection("testco")
    docs = users_ref.stream()
    doc_ref = users_ref.document("test30")
    data = [doc.to_dict() for doc in docs]

    return {"số data": len(data)}


if __name__ == "__main__":
    app.run(debug=True)
