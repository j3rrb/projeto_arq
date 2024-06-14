from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Sale, Product


@receiver(pre_save, sender=Sale)
def stock_observer(sender, instance, **kwargs):
    print("Atualizando estoque...")
    product = Product.objects.get(id=instance.product.id)
    if product.bought_qty > product.sold_qty and instance.sold_qty < product.bought_qty:
        product.sold_qty += instance.sold_qty
        product.save()
    else:
        print("Estoque insuficiente!")
        raise ValueError("Estoque insuficiente!")
