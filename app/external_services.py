import requests

def get_product_from_openfoodfacts(barcode):
    endpoint = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    headers = {"User-Agent": "RihannaInventoryManager/1.0"}
    
    try:
        res = requests.get(endpoint, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if data.get("status") == 1:
                details = data.get("product", {})
                return {
                    "barcode": barcode,
                    "name": details.get("product_name", "Unknown Product"),
                    "brand": details.get("brands", "Unknown Brand")
                }
    except requests.RequestException:
        pass
        
    return None