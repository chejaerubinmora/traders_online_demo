from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver


class Stock(models.Model):
    product = models.OneToOneField('trader.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Product(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    currency = models.CharField(max_length=1)
    price = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=Product)
def product_postsave_hook(sender, instance, created, raw, **kwargs):
    if created and not raw:
        Stock.objects.create(product=instance, quantity=instance.quantity)


class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey('trader.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=Order)
def order_postsave_hook(sender, instance, created, raw, **kwargs):
    if created and not raw:
        ordered_product = instance.product
        quantity = instance.quantity
        product_data = {
            "user": instance.user,
            "quantity": instance.quantity,
            "name": ordered_product.name,
            "price": ordered_product.price,
            "currency": ordered_product.currency
        }
        Product.objects.create(**product_data)
        stock = ordered_product.stock
        stock.quantity -= quantity
        stock.save()
