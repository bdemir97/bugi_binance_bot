from flask import Flask, jsonify, request
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.json_util import dumps
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("mongodb+srv://idemir:Bugra07.@cryptotradebot.w9yryxn.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client.configuration
collection = db.config

@app.route('/get-latest', methods=['GET'])
def get_latest():
    latest_entry = collection.find().sort([('_id', -1)]).limit(1)
    return dumps(latest_entry)

@app.route('/update', methods=['POST'])
def update_entry():
    data = request.json
    result = collection.update_one({"_id": data["_id"]}, {"$set": data})
    return jsonify({"success": result.modified_count > 0})

if __name__ == '__main__':
    app.run(debug=True)