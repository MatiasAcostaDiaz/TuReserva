from db_methods import DBManager
from models import ModelManager
from flasgger.utils import swag_from
from flask import Blueprint, jsonify, request

user = Blueprint('user', __name__)
manager = DBManager()


# User SignUp
@user.route('/users', methods=['POST'], strict_slashes=False)
def user_signup():
    """Create a user"""
    values = []
    user_values = ModelManager('Users').values
    user_values.pop(0)
    json_request = request.json
    json_request['cash'] = 0
    #Check for existence of all keys in a dict
    if all(k in json_request for k in user_values):
        for elem in user_values:
            values.append(json_request[elem])
        register = manager.insert_register('Users', values)
        return jsonify(register)
    else:
        return "Miss some value"

# Get user info
@user.route('/users/<user_id>', methods=['GET'])
def user_get(user_id):
    """Return Information about User"""
    user = manager.select_register_id('Users', user_id)
    if user is None:
        return jsonify({'fail':'fail'}), 402
    return jsonify(user)