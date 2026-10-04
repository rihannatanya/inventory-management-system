# Simple in-memory store for inventory items
items_store = [
    {
        "id": 1,
        "barcode": "0737628001158",
        "name": "Thai Peanut Sauce",
        "brand": "San-J",
        "quantity": 25,
        "price": 3.99
    }
]

def fetch_all_items():
    return items_store

def find_item_by_id(item_id):
    for item in items_store:
        if item["id"] == item_id:
            return item
    return None

def create_item(payload):
    # Auto-increment ID based on existing items
    next_id = max([item["id"] for item in items_store], default=0) + 1
    
    new_entry = {
        "id": next_id,
        "barcode": payload.get("barcode", ""),
        "name": payload.get("name", "Unnamed Item"),
        "brand": payload.get("brand", "Generic"),
        "quantity": int(payload.get("quantity", 0)),
        "price": float(payload.get("price", 0.0))
    }
    items_store.append(new_entry)
    return new_entry

def modify_item(item_id, updates):
    target = find_item_by_id(item_id)
    if not target:
        return None
    
    # Update fields provided in payload
    for key, val in updates.items():
        if key in target and key != "id":
            if key == "quantity":
                target[key] = int(val)
            elif key == "price":
                target[key] = float(val)
            else:
                target[key] = val
    return target

def remove_item(item_id):
    global items_store
    existing = find_item_by_id(item_id)
    if existing:
        items_store = [item for item in items_store if item["id"] != item_id]
        return True
    return False