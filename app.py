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


# Test bên Tân
@app.route("/")
def index():
    users_ref = db.collection("testco")
    docs = users_ref.get()

    # doc_ref = users_ref.document("test30")
    data = [doc.to_dict() for doc in docs]

    for doc in docs:
        print(doc.id, doc.to_dict())
    return jsonify(data)


# @app.route("/")
# def index():
#     esp32_ref = db.collection("esp32")

#     docs = esp32_ref.get()

#     # data = [doc.to_dict() for doc in docs]
#     for i in range(len(docs)):
#         print(esp32_ref.document(f"test{i+1}").get().to_dict())

#     # for i in len(docs):
#     #     print(docs[i].to_dict())
#     # for doc in docs:
#     #     doc.update({'create_at': 1703425857})

#     data = [doc.to_dict() for doc in docs]

#     return jsonify(data)


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


if __name__ == "__main__":
    app.run(debug=True)
