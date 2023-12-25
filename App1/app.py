from flask import Flask, request, jsonify
import csv
import requests
import json
import os
app = Flask(__name__)
@app.route('/store-file', methods=["POST"])
def store_file():
    data = request.get_json()
    
    if not data or "file" not in data or "data" not in data:
        response = {
            "file": None,
            "error": "Invalid JSON input."
        }
        return jsonify(response)

    file_name = data["file"]
    file_data = data["data"]

    try:
        if not os.path.exists('./data'):
            os.makedirs('./data')

        file_path = os.path.join('./data', file_name)

        with open(file_path, 'w') as file:
            file.write(file_data)

        response = {
            "file": file_name,
            "message": "Success."
        }
    except Exception as e:
        response = {
            "file": file_name,
            "error": "Error while storing the file to the storage."
        }
    
    return jsonify(response)

@app.route('/user-info', methods=["POST"])
def returnUserinfo():
    data = request.get_json()
    if not(data.get("file")) or data.get("file")==None:
        response= {
                    "file": None, 
                    "error": "Invalid JSON input." 
                  } 
        return jsonify(response)
    filepath='./data/'+data.get("file")
    if not os.path.exists(filepath):
            response = {
                "file": data["file"], 
                "error": "File not found." 
            }    
    else: 
         if data['key'] == 'location':
            latest_location = None
            with open(filepath,'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    if len(row) != 4:
                         response = {
                                        "file": data["file"], 
                                        "error": "Input file not in CSV format." 
                                    }  
                         return jsonify(response)
                    if row[0] == data.get("name"):
                         latest_location = {'latitude': float(row[1]), 'longitude': float(row[2])}
            response={
                        'file': data['file'],
                        'latitude': latest_location['latitude'],
                        'longitude': latest_location['longitude']
                      }
         elif data['key'] =='temperature':
             headers = {'Content-Type': 'application/json'}
             json_data = json.dumps(data)
             response = requests.post('http://app2:5001/user-info', data=json_data, headers=headers)
             return response.json()
    return jsonify(response)
    
if __name__ == '__main__':
    app.run(host = "0.0.0.0", port=6000)