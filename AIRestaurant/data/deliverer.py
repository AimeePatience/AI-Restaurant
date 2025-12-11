

from django.db.models import *

from .users import Employee
from .chef import Product


class Order(Model):
    id = AutoField(primary_key=True)
    # Link to the Customer model in the same Django app
    customer = ForeignKey("Customer", CASCADE, null=True, blank=True)
    date = DateTimeField(auto_now_add=True)
    status = CharField(max_length=20, default="pending")
    # Classify orders so each one is either food or merch
    order_type = CharField(
        max_length=5,
        choices=[("food", "Food"), ("merch", "Merch")],
        default="food",
    )


class OrderedDish(Model):
    from_order_num = ForeignKey(Order, CASCADE, related_name="items")
    product = ForeignKey(Product, CASCADE)
    quantity = IntegerField()

    def total_cost(self) -> int:
        return self.product.price * self.quantity


class Deliverer(Employee):
    pass