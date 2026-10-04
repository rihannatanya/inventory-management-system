import sys
import requests

BASE_URL = "http://127.0.0.1:5000/api"

def print_menu():
    print("\n" + "="*45)
    print(" INVENTORY MANAGEMENT ADMIN PORTAL ")
    print("="*45)
    print("1. View All Inventory Items")
    print("2. Search Item by ID")
    print("3. Add New Item Manually")
    print("4. Import Product via Barcode (External API)")
    print("5. Update Item (PATCH)")
    print("6. Delete Item")
    print("7. Exit")
    print("="*45)

def main():
    while True:
        print_menu()
        choice = input("Enter choice (1-7): ").strip()
        
        try:
            if choice == '1':
                res = requests.get(f"{BASE_URL}/inventory")
                items = res.json().get("data", [])
                print("\n--- Current Inventory ---")
                for item in items:
                    print(f"ID: {item['id']} | Name: {item['name']} | Brand: {item['brand']} | Qty: {item['quantity']} | Price: ${item['price']}")
            
            elif choice == '2':
                item_id = input("Enter Item ID: ")
                res = requests.get(f"{BASE_URL}/inventory/{item_id}")
                if res.status_code == 200:
                    item = res.json()["data"]
                    print(f"\nItem Found: {item}")
                else:
                    print("\nError:", res.json().get("message"))
                    
            elif choice == '3':
                name = input("Product Name: ")
                brand = input("Brand: ")
                quantity = int(input("Quantity: ") or 0)
                price = float(input("Price: ") or 0.0)
                barcode = input("Barcode (optional): ")
                
                payload = {"name": name, "brand": brand, "quantity": quantity, "price": price, "barcode": barcode}
                res = requests.post(f"{BASE_URL}/inventory", json=payload)
                print("\nAdded:", res.json())
                
            elif choice == '4':
                barcode = input("Enter Barcode (e.g., 0737628001158): ").strip()
                quantity = int(input("Initial Quantity: ") or 1)
                price = float(input("Initial Price: ") or 0.0)
                
                res = requests.post(f"{BASE_URL}/external/import/{barcode}", json={"quantity": quantity, "price": price})
                if res.status_code == 201:
                    print("\nSuccessfully imported from OpenFoodFacts!")
                    print("Imported Data:", res.json()["data"])
                else:
                    print("\nImport Failed:", res.json().get("message"))

            elif choice == '5':
                item_id = input("Enter Item ID to update: ")
                print("Leave blank if you don't want to change a field.")
                name = input("New Name: ")
                quantity = input("New Quantity: ")
                price = input("New Price: ")
                
                updates = {}
                if name: updates["name"] = name
                if quantity: updates["quantity"] = int(quantity)
                if price: updates["price"] = float(price)
                
                res = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=updates)
                print("\nResult:", res.json())

            elif choice == '6':
                item_id = input("Enter Item ID to delete: ")
                res = requests.delete(f"{BASE_URL}/inventory/{item_id}")
                print("\nResult:", res.json())

            elif choice == '7':
                print("Exiting CLI...")
                sys.exit(0)
            else:
                print("Invalid choice, please select 1-7.")
        except requests.exceptions.ConnectionError:
            print("\n[Error] Unable to connect to Flask API. Make sure the server is running on http://127.0.0.1:5000.")

if __name__ == "__main__":
    main()