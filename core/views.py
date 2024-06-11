from django.shortcuts import render
from django.http import JsonResponse
from .models import Group

def create_product(request):
    pass

def list_product(request):
    pass

def get_product(request):
    pass

def create_manufacturer(request):
    pass

def get_subgroups(request):
    group_id = request.GET.get('parent_id')
    sub_groups = Group.objects.filter(parent_id=group_id).values('id', 'name')
    
    return JsonResponse(list(sub_groups), safe=False)

def create_group(request):
    pass

def create_subgroup(request):
    pass

def create_sale(request):
    pass