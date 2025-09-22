from src.config import get_supabase

class CustomerDAO:
    def __init__(self):
        self.supabase = get_supabase()

    def add_customer(self, data):
        res = self.supabase.table("customers").insert(data).execute()
        return res.data[0]

    def list_customers(self):
        res = self.supabase.table("customers").select("*").execute()
        return res.data

    def get_customer_by_id(self, customer_id):
        res = self.supabase.table("customers").select("*").eq("customer_id", customer_id).execute()
        return res.data[0] if res.data else None
