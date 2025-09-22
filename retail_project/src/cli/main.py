import argparse
import json
from src.services.product_service import ProductService
from src.services.customer_service import CustomerService
from src.services.order_service import OrderService

def serialize(obj):
    return json.dumps(obj, indent=2, default=str)

class RetailCLI:
    def __init__(self):
        self.product_service = ProductService
        self.customer_service = CustomerService
        self.order_service = OrderService

    # Product
    def cmd_product_add(self, args):
        print(serialize(self.product_service.add_product(args.name, args.sku, args.price, args.stock, args.category)))

    def cmd_product_list(self, args):
        print(serialize(self.product_service.list_products()))

    # Customer
    def cmd_customer_add(self, args):
        print(serialize(self.customer_service.add_customer(args.name, args.email, args.phone, args.city)))

    def cmd_customer_list(self, args):
        print(serialize(self.customer_service.list_customers()))

    # Order
    def cmd_order_create(self, args):
        items = [{"prod_id": int(i.split(":")[0]), "quantity": int(i.split(":")[1])} for i in args.item]
        print(serialize(self.order_service.create_order(args.customer, items)))

    def cmd_order_show(self, args):
        print(serialize(self.order_service.get_order_details(args.order)))

    def cmd_order_list(self, args):
        print(serialize(self.order_service.list_orders(args.customer)))

    def cmd_order_cancel(self, args):
        print(serialize(self.order_service.cancel_order(args.order)))

    # Parser
    def build_parser(self):
        parser = argparse.ArgumentParser(prog="retail-cli")
        sub = parser.add_subparsers(dest="cmd")

        # Product
        p_prod = sub.add_parser("product")
        ps = p_prod.add_subparsers(dest="action")
        addp = ps.add_parser("add")
        addp.add_argument("--name", required=True)
        addp.add_argument("--sku", required=True)
        addp.add_argument("--price", type=float, required=True)
        addp.add_argument("--stock", type=int, default=0)
        addp.add_argument("--category")
        addp.set_defaults(func=self.cmd_product_add)
        listp = ps.add_parser("list")
        listp.set_defaults(func=self.cmd_product_list)

        # Customer
        p_cust = sub.add_parser("customer")
        cs = p_cust.add_subparsers(dest="action")
        addc = cs.add_parser("add")
        addc.add_argument("--name", required=True)
        addc.add_argument("--email", required=True)
        addc.add_argument("--phone", required=True)
        addc.add_argument("--city")
        addc.set_defaults(func=self.cmd_customer_add)
        listc = cs.add_parser("list")
        listc.set_defaults(func=self.cmd_customer_list)

        # Order
        p_order = sub.add_parser("order")
        osub = p_order.add_subparsers(dest="action")
        createo = osub.add_parser("create")
        createo.add_argument("--customer", type=int, required=True)
        createo.add_argument("--item", nargs="+", required=True, help="prod_id:qty")
        createo.set_defaults(func=self.cmd_order_create)
        showo = osub.add_parser("show")
        showo.add_argument("--order", type=int, required=True)
        showo.set_defaults(func=self.cmd_order_show)
        listo = osub.add_parser("list")
        listo.add_argument("--customer", type=int, required=True)
        listo.set_defaults(func=self.cmd_order_list)
        cano = osub.add_parser("cancel")
        cano.add_argument("--order", type=int, required=True)
        cano.set_defaults(func=self.cmd_order_cancel)

        return parser

    def run(self):
        parser = self.build_parser()
        args = parser.parse_args()
        if hasattr(args, "func"):
            args.func(args)
        else:
            parser.print_help()

if __name__ == "__main__":
    RetailCLI().run()
