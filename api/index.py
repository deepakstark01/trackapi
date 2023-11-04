from flask import Flask, jsonify, request
from pymongo import MongoClient
app = Flask(__name__)

# Replace '<password>' with your actual password and ensure the rest of your connection string is correct.
CONNECTION_STRING = "mongodb+srv://deepakstark01:deepak01@data.lp7ftel.mongodb.net/"

client = MongoClient(CONNECTION_STRING)

# Assuming you have already created the 'tracker' database and 'devices' collection
db = client.tracker
devices_collection = db.devices

@app.route('/devices', methods=['POST'])
def create_device():
    # Get data from URL parameters or JSON
    device = request.args.get('Device') or request.json.get('Device')
    phone = request.args.get('Phone') or request.json.get('Phone')
    timeval = request.args.get('Time') or request.json.get('Time')
    
    # Create or update the document with the new call
    call_data = {
        "Phone": phone,
        "Time": timeval,
    }
    
    # Check if the device already exists
    device_document = devices_collection.find_one({"Device": device})
    
    if device_document:
        # If it exists, append the new call to the 'Calls' array
        devices_collection.update_one(
            {"_id": device_document['_id']},
            {"$push": {"Calls": call_data}}
        )
        return jsonify({"result": "Call added to existing device"}), 200
    else:
        # If it doesn't exist, create a new document with the device and the call
        data = {
            "Device": device,
            "Calls": [call_data]
        }
        devices_collection.insert_one(data)
        # return jsonify({"_id": str(result.inserted_id), "result": "New device created with call"}), 201
        return jsonify({"result": "New device created with call"}), 201


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404

app.run(host='0.0.0.0', port=81)