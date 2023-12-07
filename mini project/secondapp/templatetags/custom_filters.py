# custom_filters.py
from django import template
from secondapp.models import Cart

register = template.Library()

@register.filter(name='get_cart_item')
def get_cart_item(cart_id):
    return Cart.objects.get(id=int(cart_id))

@register.filter(name='calculate_total')
def calculate_total(order):
    total = 0
    for cart_id in order.cart_ids.split(','):
        cart_item = Cart.objects.get(id=int(cart_id))
        total += cart_item.product.item_price * cart_item.quantity
    return total
