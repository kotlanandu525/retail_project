from src.dao.order_dao import OrderDAO
from src.services.product_service import ProductService
from src.services.customer_service import CustomerService

class OrderService:
    dao = OrderDAO()

    @classmethod
    def create_order(cls, customer_id, items):
        customer = CustomerService.get_customer(customer_id)
        if not customer:
            raise Exception("Customer not found")

        total_amount = 0
        order_items = []

        # check products and stock
        for i in items:
            product = ProductService.get_product(i["prod_id"])
            if not product:
                raise Exception(f"Product {i['prod_id']} not found")
            if product["stock"] < i["quantity"]:
                raise Exception(f"Insufficient stock for product {product['name']}")
            total_amount += product["price"] * i["quantity"]
            order_items.append({"prod_id": i["prod_id"], "quantity": i["quantity"], "price": product["price"]})

        # deduct stock
        for i in order_items:
            product = ProductService.get_product(i["prod_id"])
            ProductService.update_stock(i["prod_id"], product["stock"] - i["quantity"])

        # create order
        order = cls.dao.create_order({"customer_id": customer_id, "status": "PLACED", "total_amount": total_amount})
        cls.dao.add_order_items(order["order_id"], order_items)
        return order

    @classmethod
    def get_order_details(cls, order_id):
        return cls.dao.get_order(order_id)

    @classmethod
    def list_orders(cls, customer_id):
        return cls.dao.list_orders_by_customer(customer_id)

    @classmethod
    def cancel_order(cls, order_id):
        order = cls.dao.get_order(order_id)
        if not order:
            raise Exception("Order not found")
        if order["status"] != "PLACED":
            raise Exception("Only PLACED orders can be cancelled")

        # restore stock
        from src.config import get_supabase
        supabase = get_supabase()
        items_res = supabase.table("order_items").select("*").eq("order_id", order_id).execute()
        for item in items_res.data:
            product = ProductService.get_product(item["prod_id"])
            ProductService.update_stock(item["prod_id"], product["stock"] + item["quantity"])

        cls.dao.cancel_order(order_id)
        order = cls.dao.get_order(order_id)
        return order
