from src.config import get_supabase

class ProductDAO:
    def __init__(self):
        self.supabase = get_supabase()

    def add_product(self, data):
        res = self.supabase.table("products").insert(data).execute()
        return res.data[0]

    def list_products(self):
        res = self.supabase.table("products").select("*").execute()
        return res.data

    def get_product_by_id(self, prod_id):
        res = self.supabase.table("products").select("*").eq("prod_id", prod_id).execute()
        return res.data[0] if res.data else None

    def update_stock(self, prod_id, new_stock):
        self.supabase.table("products").update({"stock": new_stock}).eq("prod_id", prod_id).execute()
