from flask import Flask, request,jsonify
import csv
app = Flask(__name__)
@app.route('/user-info', methods=["POST"])
def returnUserinfo():
    data = request.get_json()
    if not(data.get("file")) or data.get("file")==None:
        response= {
                    "file": None, 
                    "error": "Invalid JSON input." 
                  } 
    else: 
         if data['key'] == 'temperature':
            latest_temperature = None
            filepath='./data/'+data.get("file")
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
                         latest_temperature =  int(row[3])
            response={
                        'file': data['file'],
                        'temperature': latest_temperature
                      }
    
    return jsonify(response)
    
if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5001)