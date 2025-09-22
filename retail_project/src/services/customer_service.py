from src.dao.customer_dao import CustomerDAO

class CustomerService:
    dao = CustomerDAO()

    @classmethod
    def add_customer(cls, name, email, phone, city):
        data = {"name": name, "email": email, "phone": phone, "city": city}
        return cls.dao.add_customer(data)

    @classmethod
    def list_customers(cls):
        return cls.dao.list_customers()

    @classmethod
    def get_customer(cls, customer_id):
        return cls.dao.get_customer_by_id(customer_id)
