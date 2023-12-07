from django import forms

from secondapp.models import add_product,Order


class add_product_form(forms.ModelForm):
    class Meta:
        model=add_product
        fields=["item_name","item_category","item_price","item_image","item_details"]

class UpdateOrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_status']