from django.db import models
from store.models import Product,Variation
from django.urls import reverse

# Create your models here.
class Cart(models.Model):
    cart_id     = models.CharField(max_length=250)
    date_added  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    product     = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart        = models.ForeignKey(Cart,on_delete=models.CASCADE)
    variations  = models.ManyToManyField(Variation,blank=True)
    quantity    = models.IntegerField()
    is_active   = models.BooleanField(default=True)

    def sub_total(self):
        return self.quantity * self.product.price

    def _unicode__(self):
        return self.product
