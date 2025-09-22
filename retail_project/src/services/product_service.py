from src.dao.product_dao import ProductDAO

class ProductService:
    dao = ProductDAO()

    @classmethod
    def add_product(cls, name, sku, price, stock, category):
        data = {"name": name, "sku": sku, "price": price, "stock": stock, "category": category}
        return cls.dao.add_product(data)

    @classmethod
    def list_products(cls):
        return cls.dao.list_products()

    @classmethod
    def get_product(cls, prod_id):
        return cls.dao.get_product_by_id(prod_id)

    @classmethod
    def update_stock(cls, prod_id, new_stock):
        cls.dao.update_stock(prod_id, new_stock)
