from django import forms
from .models import Product, Group, Manufacturer

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    
    def __init__(self, *args, **kwargs) -> None:
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['manufacturer'] = Manufacturer.objects.all()
        self.fields['group'] = Group.objects.all()
        self.fields['sub_group'].widget.attrs.update({'class': 'subgroup-select'})
        self.fields['sub_group'].widget.attrs.update({'data-url': '/get-subgroups/'})
        self.fields['sub_group'].widget.attrs.update({'data-parent-field': 'sub_groups'})

