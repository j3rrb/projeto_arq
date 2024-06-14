from django import forms
from .models import Product, Group, Manufacturer, Sale


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ["id"]


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "__all__"
        exclude = ["id"]


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = "__all__"
        exclude = ["id"]


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = "__all__"
        exclude = ["id"]
