from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Group, Sale, Product, Manufacturer, Location
from .forms import SaleForm, ManufacturerForm, ProductForm, GroupForm


def is_admin(user):
    return user.is_superuser


def dashboard(request):
    if request.method == "GET":
        return render(request, "dashboard.html")


@login_required
def index(request):
    if request.method == "GET":
        return render(request, "index.html")


@login_required
def list_product(request):
    if request.method == "GET":
        products = Product.objects.all().order_by("-updated_at")

        return render(request, "products.html", {"products": products})


@login_required
def list_groups(request):
    if request.method == "GET":

        def build_tree(nodes, parent_id=None):
            tree = []
            for node in nodes:
                if node["parent_id"] == parent_id:
                    tree_node = node.to_dict()
                    tree_node["children"] = build_tree(nodes, node["id"])
                    tree.append(tree_node)

            return tree

        groups = Group.objects.all().order_by("-updated_at")
        groups = build_tree(groups)

        return render(request, "groups.html", {"groups": groups})


@login_required
def list_manufacturers(request):
    if request.method == "GET":
        manufacturers = Manufacturer.objects.all().order_by("-updated_at")

        return render(request, "manufacturers.html", {"manufacturers": manufacturers})


@login_required
def list_sales(request):
    if request.method == "GET":
        sales = Sale.objects.all().order_by("-updated_at")

        return render(request, "sales.html", {"sales": sales})


@login_required
@user_passes_test(is_admin, "/")
def create_manufacturer(request):
    message = None
    errors = None

    if request.method == "POST":
        post_data = request.POST.copy()

        address = post_data["address"]
        phone = post_data["phone"]

        location = Location.objects.create(address=address, phone=phone)

        post_data["location"] = location

        form = ManufacturerForm(post_data)

        if form.is_valid():
            try:
                Manufacturer.objects.create(**form.cleaned_data)
                message = "Fabricante criado com sucesso!"
                redirect("/manufacturer/")
            except Exception as e:
                print(e)
        else:
            errors = form.errors

    return render(
        request,
        "forms/create-manufacturer.html",
        {"message": message, "errors": errors},
    )


@login_required
@user_passes_test(is_admin, "/")
def create_product(request):
    message = None
    errors = None
    manufacturers = Manufacturer.objects.all().order_by("-updated_at")
    groups = Group.objects.all().order_by("-updated_at")

    if request.method == "POST":
        post_data = request.POST.copy()

        manufacturer = Manufacturer.objects.get(id=post_data["manufacturer"])
        group = Group.objects.get(id=post_data["group"])

        if post_data.get("sub_group", None):
            sub_group = Group.objects.get(id=post_data["sub_group"])
            post_data["sub_group"] = sub_group

        post_data["manufacturer"] = manufacturer
        post_data["group"] = group

        form = ProductForm(post_data)

        if form.is_valid():
            try:
                Product.objects.create(**form.cleaned_data)
                message = "Produto criado com sucesso!"
                redirect("/product/")
            except Exception as e:
                print(e)
        else:
            errors = form.errors

    return render(
        request,
        "forms/create-product.html",
        {
            "message": message,
            "manufacturers": manufacturers,
            "groups": groups,
            "errors": errors,
        },
    )


@login_required
def get_subgroups(request):
    group_id = request.GET.get("parent_id")
    sub_groups = Group.objects.filter(parent_id=group_id).values()

    return JsonResponse(list(sub_groups), safe=False)


@login_required
@user_passes_test(is_admin, "/")
def create_group(request):
    message = None
    errors = None
    groups = Group.objects.all().order_by("-updated_at")

    if request.method == "POST":
        form = GroupForm(request.POST)

        if form.is_valid():
            try:
                Group.objects.create(**form.cleaned_data)
                message = "Grupo criado com sucesso!"
                redirect("/group/")
            except Exception as e:
                print(e)
        else:
            errors = form.errors

    return render(
        request,
        "forms/create-group.html",
        {"groups": groups, "message": message, "errors": errors},
    )


@login_required
@user_passes_test(is_admin, "/")
def create_sale(request):
    message = None
    errors = None
    products = Product.objects.all().order_by("-updated_at")

    if request.method == "POST":
        post_data = request.POST.copy()

        qty = post_data["qty"]
        product = Product.objects.get(id=post_data["product"])

        total = float(product.sale_price) * float(qty)
        manufacturer = product.manufacturer
        group = product.group
        sub_group = product.sub_group

        if sub_group:
            sub_group = product.sub_group

        post_data["sold_price"] = total
        post_data["product"] = product
        post_data["manufacturer"] = manufacturer
        post_data["group"] = group
        post_data["sub_group"] = sub_group
        post_data["sold_qty"] = qty

        form = SaleForm(post_data)

        if form.is_valid():
            try:
                Sale.objects.create(**form.cleaned_data)
                message = "Venda criada com sucesso!"
                redirect("/group/")
            except Exception as e:
                if type(e) is ValueError:
                    errors = e
                else:
                    print(e)
        else:
            errors = form.errors

    return render(
        request,
        "forms/create-sale.html",
        {"products": products, "message": message, "errors": errors},
    )
