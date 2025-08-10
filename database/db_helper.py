import json
import os
from typing import Dict, List, Any
from pathlib import Path

class DatabaseHelper:
    def __init__(self, db_file: str = "database/data.json"):
        self.db_file = db_file
        self.data = self.load_data()
    
    def load_data(self) -> Dict[str, Any]:
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Default data structure
        default_data = {
            "store": {  # Fixed: Added missing "store" wrapper
                "Dresses": [  # Fixed: Changed "Dresses1" to "Dresses"
                    {
                        "id": 1,  
                        "name": "Floral flowy linen",
                        "price": 15.00,
                        "description": "Lightweight summery buttery texture casual midi dress print lowcut sweet temperament dress",  # Fixed: lowercase 'description'
                        "sizes": ["S(US-4)", "M(US-6)", "L(US-08/10)"],
                        "colors": ["Butter yellow", "Sage green"]
                    },
                    {
                        "id": 2,  
                        "name": "Silky satin",
                        "price": 35.00,
                        "description": "women summer stain V neck sling dress elegant sleeveless loose maxi robes",  # Fixed: lowercase 'description'
                        "sizes": ["S(US-4)", "M(US-6)", "L(US-08/10)"],
                        "colors": ["Butter yellow", "Sage green", "Coral pink", "Misty brown"]
                    },
                ],
                "Pants": [
                    {
                        "id": 3,  
                        "name": "Classic linen wash",
                        "price": 25.00,
                        "description": "Slim fit, stretch denim.",
                        "sizes": ["28", "30", "32", "34"],
                        "colors": ["Blue", "Black","white"]
                    },
                    {
                        "id": 4,  
                        "name": "Baggy Jeans",
                        "price": 25.00,
                        "description": "Slim fit, stretch denim.",
                        "sizes": ["28", "30", "32", "34"],
                        "colors": ["Blue", "Black", "Sage"]
                    }
                ],
                "Shoes": [
                    {
                        "id": 5, 
                        "name": "Louboutons",
                        "price": 300.00,
                        "description": "Red bottom heels",
                        "sizes": ["7", "8", "9", "10"],
                        "colors": ["White", "Black","red"]
                    },
                    {
                        "id": 6,  
                        "name": "YSL",
                        "price": 120.00,
                        "description": "YSL imprented heels",
                        "sizes": ["7", "8", "9", "10"],
                        "colors": ["White", "Black", "gold"]
                    }
                ]
            },  
            "orders": {},
            "settings": {
                "shipping_fee": 5.00,
                "min_order": 20.00
            }
        }
        
        # Save default data
        self.save_data_dict(default_data)
        return default_data
    
    def save_data(self):
        self.save_data_dict(self.data)
    
    def save_data_dict(self, data: Dict[str, Any]):
        # Create directory if it doesn't exist
        Path(self.db_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_store_category(self, category: str) -> List[Dict]:
        return self.data.get("store", {}).get(category, [])
    
    def get_item_by_id(self, item_id: int) -> Dict:
        for category in self.data.get("store", {}).values():
            for item in category:
                if item.get("id") == item_id:  # Added .get() for safety
                    return item
        return {}
    
    def add_to_cart(self, user_id: int, item_id: int, quantity: int = 1):
        user_str = str(user_id)
        if user_str not in self.data["orders"]:
            self.data["orders"][user_str] = {"items": {}, "subtotal": 0, "shipping": 0, "total": 0}
        
        if str(item_id) in self.data["orders"][user_str]["items"]:
            self.data["orders"][user_str]["items"][str(item_id)] += quantity
        else:
            self.data["orders"][user_str]["items"][str(item_id)] = quantity
        
        self.update_cart_totals(user_id)
        self.save_data()
    
    def update_cart_totals(self, user_id: int):
        """Calculate subtotal, shipping, and total for a user's cart"""
        user_str = str(user_id)
        subtotal = 0
        
        if user_str in self.data["orders"]:
            for item_id, quantity in self.data["orders"][user_str]["items"].items():
                item = self.get_item_by_id(int(item_id))
                if item:
                    subtotal += item["price"] * quantity
            
            # Calculate shipping
            min_order = self.data["settings"]["min_order"]
            shipping_fee = self.data["settings"]["shipping_fee"]
            
            # Free shipping if order meets minimum, otherwise add shipping fee
            shipping = 0 if subtotal >= min_order else shipping_fee
            total = subtotal + shipping
            
            # Update the order
            self.data["orders"][user_str]["subtotal"] = subtotal
            self.data["orders"][user_str]["shipping"] = shipping
            self.data["orders"][user_str]["total"] = total
    
    def get_cart(self, user_id: int) -> Dict:
        """Get cart with detailed breakdown"""
        cart = self.data["orders"].get(str(user_id), {"items": {}, "subtotal": 0, "shipping": 0, "total": 0})
        
        # Add item details for easy display
        cart_with_details = cart.copy()
        cart_with_details["item_details"] = []
        
        for item_id, quantity in cart["items"].items():
            item = self.get_item_by_id(int(item_id))
            if item:
                cart_with_details["item_details"].append({
                    "item": item,
                    "quantity": quantity,
                    "line_total": item["price"] * quantity
                })
        
        return cart_with_details
    
    def clear_cart(self, user_id: int):
        user_str = str(user_id)
        if user_str in self.data["orders"]:
            self.data["orders"][user_str] = {"items": {}, "subtotal": 0, "shipping": 0, "total": 0}
            self.save_data()
    
    def remove_from_cart(self, user_id: int, item_id: int, quantity: int = 1):
        """Remove specific quantity of an item from cart"""
        user_str = str(user_id)
        item_str = str(item_id)
        
        if user_str in self.data["orders"] and item_str in self.data["orders"][user_str]["items"]:
            current_qty = self.data["orders"][user_str]["items"][item_str]
            
            if current_qty <= quantity:
                # Remove item completely
                del self.data["orders"][user_str]["items"][item_str]
            else:
                # Reduce quantity
                self.data["orders"][user_str]["items"][item_str] -= quantity
            
            self.update_cart_totals(user_id)
            self.save_data()
    
    def get_shipping_info(self, user_id: int) -> Dict:
        """Get shipping information for a user's cart"""
        cart = self.get_cart(user_id)
        min_order = self.data["settings"]["min_order"]
        shipping_fee = self.data["settings"]["shipping_fee"]
        
        free_shipping_eligible = cart["subtotal"] >= min_order
        amount_for_free_shipping = max(0, min_order - cart["subtotal"])
        
        return {
            "subtotal": cart["subtotal"],
            "shipping_fee": cart["shipping"],
            "total": cart["total"],
            "free_shipping_eligible": free_shipping_eligible,
            "amount_needed_for_free_shipping": amount_for_free_shipping,
            "min_order_for_free_shipping": min_order
        }

# Global database instance
db = DatabaseHelper()