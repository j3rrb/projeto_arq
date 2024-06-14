from typing import Iterable
from django.db import models
from django.core.validators import MinLengthValidator
from cuid import cuid


class BaseModel(models.Model):
    id = models.CharField(max_length=25, default=cuid, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self._meta.fields}

    class Meta:
        abstract = True


class Location(BaseModel):
    address = models.CharField(max_length=50, null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=True)

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(
                f"'{self.__class__.__name__}' object has no attribute '{key}'"
            )

    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(
                f"'{self.__class__.__name__}' object has no attribute '{key}'"
            )


class Manufacturer(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False)
    social_name = models.CharField(max_length=50, null=False, blank=False)
    document = models.CharField(
        max_length=14,
        null=False,
        blank=False,
        unique=True,
        validators=[MinLengthValidator(14)],
    )
    email = models.EmailField(null=False, blank=True, unique=True)
    salesman = models.CharField(max_length=50, null=False, blank=False)

    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(
                f"'{self.__class__.__name__}' object has no attribute '{key}'"
            )

    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(
                f"'{self.__class__.__name__}' object has no attribute '{key}'"
            )


class Group(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    description = models.CharField(max_length=150, null=True, blank=True)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="parent_group",
    )
    sub_group = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="child_group",
    )

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(
                f"'{self.__class__.__name__}' object has no attribute '{key}'"
            )

    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(
                f"'{self.__class__.__name__}' object has no attribute '{key}'"
            )


class Product(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=150, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=16, null=False, decimal_places=2)
    sale_price = models.DecimalField(max_digits=16, null=False, decimal_places=2)
    weight = models.DecimalField(max_digits=4, null=False, decimal_places=2)
    bought_qty = models.IntegerField(null=False)
    sold_qty = models.IntegerField(null=False)

    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="products")
    sub_group = models.ForeignKey(
        Group,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="sub_products",
    )

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(
                f"'{self.__class__.__name__}' object has no attribute '{key}'"
            )

    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(
                f"'{self.__class__.__name__}' object has no attribute '{key}'"
            )


class Sale(BaseModel):
    timestamp = models.DateTimeField(auto_now_add=True)
    sold_price = models.DecimalField(max_digits=16, null=False, decimal_places=2)
    sold_qty = models.IntegerField(null=False, blank=False)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="sales")
    sub_group = models.ForeignKey(
        Group, null=True, blank=True, on_delete=models.CASCADE, related_name="sub_sales"
    )

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(
                f"'{self.__class__.__name__}' object has no attribute '{key}'"
            )

    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(
                f"'{self.__class__.__name__}' object has no attribute '{key}'"
            )
