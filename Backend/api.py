from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import base64
import teste

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app, support_credentials=True)


@app.route('/image', methods=['POST'])
@cross_origin(supports_credentials=True)
def home():
    content = request.get_json()
    try:
        carPlate = teste.carPlateString(content)
        return jsonify(carPlate)
    except:
        return jsonify("No plate detected")


app.run(host='0.0.0.0')
