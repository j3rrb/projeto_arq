from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.urls import (
    product_urls,
    sale_urls,
    dashboard_urls,
    group_urls,
    manufacturer_urls,
)
from core.views import index

urlpatterns = [
    path("", index, name="Index"),
    path("dashboard/", include(dashboard_urls)),
    path("admin/", admin.site.urls),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path(
        "accounts/logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"
    ),
    path("product/", include(product_urls)),
    path("group/", include(group_urls)),
    path("manufacturer/", include(manufacturer_urls)),
    path("sale/", include(sale_urls)),
]
