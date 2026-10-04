from flask import Blueprint, jsonify, request
from .database import (
    fetch_all_items, find_item_by_id, create_item, modify_item, remove_item
)
from .external_services import get_product_from_openfoodfacts

api_bp = Blueprint('api', __name__)

@api_bp.route('/inventory', methods=['GET'])
def list_inventory():
    return jsonify({"success": True, "data": fetch_all_items()}), 200

@api_bp.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = find_item_by_id(item_id)
    if not item:
        return jsonify({"success": False, "message": "Item not found"}), 404
    return jsonify({"success": True, "data": item}), 200

@api_bp.route('/inventory', methods=['POST'])
def add_inventory_item():
    body = request.get_json()
    if not body or "name" not in body:
        return jsonify({"success": False, "message": "Product name is required"}), 400
    
    new_item = create_item(body)
    return jsonify({"success": True, "data": new_item}), 201

@api_bp.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_inventory_item(item_id):
    body = request.get_json()
    if not body:
        return jsonify({"success": False, "message": "No update fields sent"}), 400
    
    updated = modify_item(item_id, body)
    if not updated:
        return jsonify({"success": False, "message": "Item not found"}), 404
        
    return jsonify({"success": True, "data": updated}), 200

@api_bp.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    deleted = remove_item(item_id)
    if not deleted:
        return jsonify({"success": False, "message": "Item not found"}), 404
    return jsonify({"success": True, "message": f"Item {item_id} removed"}), 200

@api_bp.route('/external/import/<barcode>', methods=['POST'])
def import_barcode_product(barcode):
    external_data = get_product_from_openfoodfacts(barcode)
    if not external_data:
        return jsonify({"success": False, "message": "Product not found on OpenFoodFacts API"}), 404
    
    payload = request.get_json() or {}
    external_data["quantity"] = payload.get("quantity", 1)
    external_data["price"] = payload.get("price", 0.0)
    
    new_item = create_item(external_data)
    return jsonify({
        "success": True,
        "message": "Product imported successfully",
        "data": new_item
    }), 201