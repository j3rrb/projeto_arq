from django.urls import path
from . import views

product_urls = [
    path("", views.list_product, name="List products"),
]

group_urls = [
    path("", views.list_groups, name="List groups"),
    path("get-subgroups/", views.get_subgroups, name="Get subgroups"),
]

manufacturer_urls = [path("", views.list_manufacturers, name="List manufacturers")]

sale_urls = [path("", views.list_sales, name="List sales")]
