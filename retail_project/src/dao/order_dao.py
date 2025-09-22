from src.config import get_supabase
from datetime import datetime

class OrderDAO:
    def __init__(self):
        self.supabase = get_supabase()

    def create_order(self, data):
        data["created_at"] = datetime.utcnow().isoformat()
        data["updated_at"] = datetime.utcnow().isoformat()
        res = self.supabase.table("orders").insert(data).execute()
        return res.data[0]

    def add_order_items(self, order_id, items):
        for item in items:
            item["order_id"] = order_id
            item["price"] = item["price"]  # snapshot of product price
            item["created_at"] = datetime.utcnow().isoformat()
            item["updated_at"] = datetime.utcnow().isoformat()
        self.supabase.table("order_items").insert(items).execute()

    def get_order(self, order_id):
        res = self.supabase.table("orders").select("*").eq("order_id", order_id).execute()
        return res.data[0] if res.data else None

    def list_orders_by_customer(self, customer_id):
        res = self.supabase.table("orders").select("*").eq("customer_id", customer_id).execute()
        return res.data

    def cancel_order(self, order_id):
        self.supabase.table("orders").update({"status": "CANCELLED", "updated_at": datetime.utcnow().isoformat()}).eq("order_id", order_id).execute()
