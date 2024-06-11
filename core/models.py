from django.db import models
from django.contrib.auth.models import User
from cuid2 import cuid_wrapper

cuid_gen = cuid_wrapper()

class BaseModel(models.Model):
    id = models.CharField(max_length=24, default=cuid_gen, primary_key=True)

    class Meta:
        abstract = True

class Location(BaseModel):
    address = models.CharField(max_length=50, null=False, blank=True)
    phone = models.CharField(max_length=20, null=False, blank=True)


class Manufacturer(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False)
    social_name = models.CharField(max_length=50, null=False, blank=False)
    document = models.CharField(max_length=14)
    email = models.EmailField()

    salesman = models.ForeignKey(User, on_delete=models.CASCADE)


class Group(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=150, null=True)

    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name="parent_group")
    sub_group = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name="child_group")


class Product(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=150, null=True)
    cost_price = models.DecimalField(max_digits=16, null=False, decimal_places=2)
    sale_price = models.DecimalField(max_digits=16, null=False, decimal_places=2)
    weight = models.DecimalField(max_digits=4, null=False, decimal_places=2)
    bought_qty = models.IntegerField(null=False)
    sold_qty = models.IntegerField(null=False)

    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="products")
    sub_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="sub_products")


class Sale(BaseModel):
    timestamp = models.DateTimeField(auto_now_add=True)
    sold_price = models.DecimalField(max_digits=16, null=False, decimal_places=2)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="sales")
    sub_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="sub_sales")

