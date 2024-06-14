from django.urls import path
from . import views

product_urls = [
    path("", views.list_product, name="List products"),
    path("create/", views.create_product, name="Create product"),
]

group_urls = [
    path("", views.list_groups, name="List groups"),
    path("create/", views.create_group, name="Create group"),
    path("get-subgroups/", views.get_subgroups, name="Get subgroups"),
]

manufacturer_urls = [
    path("", views.list_manufacturers, name="List manufacturers"),
    path("create/", views.create_manufacturer, name="Create a manufacturer"),
]

sale_urls = [
    path("", views.list_sales, name="List sales"),
    path("create/", views.create_sale, name="Create a sale"),
]
