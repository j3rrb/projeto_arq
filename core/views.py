from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Group, Sale, Product, Manufacturer


def is_admin(user):
    return user.is_superuser


@login_required
def index(request):
    if request.method == "GET":
        return render(request, "index.html")


@login_required
@user_passes_test(is_admin, '/')
def create_product(request):
    pass


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
@user_passes_test(is_admin, '/')
def get_product(request):
    pass


@login_required
@user_passes_test(is_admin, '/')
def create_manufacturer(request):
    pass


@login_required
def get_subgroups(request):
    group_id = request.GET.get("parent_id")
    sub_groups = Group.objects.filter(parent_id=group_id).values()

    return JsonResponse(list(sub_groups), safe=False)


@login_required
@user_passes_test(is_admin, '/')
def create_group(request):
    pass


@login_required
@user_passes_test(is_admin, '/')
def create_subgroup(request):
    pass


@login_required
@user_passes_test(is_admin, '/')
def create_sale(request):
    pass
