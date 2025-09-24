from django.db import models
from Accounts.models import CustomUser
from Products.models import Product
# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    qty = models.IntegerField()
    is_active = models.BooleanField(default=True)


    def sub_total(self):
        return self.product.discount_price * self.qty
    
    def __str__(self):
        return f'CartItem: {self.product.name}'
    
    def __unicode__(self):
        return self.product

