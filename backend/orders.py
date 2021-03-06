from db_methods import DBManager
from models import ModelManager
from flasgger.utils import swag_from
from flask import Blueprint, jsonify, request

order = Blueprint('order', __name__)
manager = DBManager()


# Create an Order
@order.route('/orders', methods=['POST'],
           strict_slashes=False)
@swag_from('documentation/orders/post_order.yml')
def order_create():
    """Create a Review"""
    values = []
    user_values = ModelManager('Orders').values
    user_values.pop(0)
    # DateTime format is YYYY-MM-DD HH-MM-SS
    json_request = request.json
    print(json_request)
    #Check for existence of all keys in a dict
    if all(k in json_request for k in user_values):
        for elem in user_values:
            values.append(json_request[elem])
        register = manager.insert_register('Orders', values)
        if register is None:
            return jsonify({'msg':'Error'}), 403
        res = manager.create_orders_services(
            register['id'], json_request['services'])
        if res == False:
            return "Something wrong"
        return jsonify({'msg':'OK'}), 201
    else:
        return jsonify({"msg":"Miss some value"}), 400

# Get an Order
@order.route('/orders/<order_id>', methods=['GET'])
@swag_from('documentation/orders/get_order.yml')
def orders_get(order_id):
    """Return Information about an Order"""
    order = manager.select_register_id('Orders', order_id)
    if order is None:
        return jsonify({'msg':'Not found'}), 404
    return jsonify(order), 200

# Delete an order
@order.route('/orders/<order_id>', methods=['DELETE'],
           strict_slashes=False)
@swag_from('documentation/orders/delete_order.yml')
def order_delete(order_id):
    """This function delete an order <order_id>"""
    res = manager.delete_register('Orders', order_id)
    if res == False:
        return ("Something wrong\n"), 400
    else:
        return ("OK"), 200
