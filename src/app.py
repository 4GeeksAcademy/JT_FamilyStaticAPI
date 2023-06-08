"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }

    return jsonify(response_body), 200

@app.route('/members', methods=['POST'])
def new_member():
    data = request.json

    if not data:
        return jsonify({"Message": "Datos incorrectos"}), 400

    response = jackson_family.add_member(data)

    return jsonify(response), 200


@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):

    response = jackson_family.delete_member(id)

    if response == {"Message": "No se encontró ningún miembro con ese id"}:
        return jsonify(response), 404

    return jsonify(response), 200


@app.route('/members/<int:id>', methods=['GET'])
def info_familymember(id):

    info_family_member = jackson_family.get_member(id)

    if info_family_member is None:
        return jsonify({"Message": "No se encontró ningún miembro con ese id"}), 404

    return jsonify(info_family_member), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
