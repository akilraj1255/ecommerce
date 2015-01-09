from django.db import models
from django.contrib.auth.models import User

from carts.models import Cart
from profiles.models import Address

# Create your models here.

STATUS_CHOICES = (
	('Started', 'Started'),
	('Abandoned', 'Abandoned'), 
	('Collected', 'Collected'),
)

class Order(models.Model):
    user = models.ForeignKey(User)
    cart = models.ForeignKey(Cart)
    order_id = models.CharField(max_length=120, default="ABC123", unique=True)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="Started")
    billing_address = models.OneToOneField(Address, null=False, blank=False, related_name='+')
    shipping_address = models.OneToOneField(Address, null=False, blank=False, related_name='+')
    cc_four = models.CharField(max_length=4, null=True, blank=True)

    def __unicode__(self):
    	return "Order number is %s" %(self.order_id)

    class Meta:
        ordering = ['-status', '-cart']  


SHIPPING_STATUS = (
    ('Not Shipped', 'Not Shipped'),
    ('Shipping Soon', 'Shipping Soon'),
    ('Shipped', 'Shipped')
)

class ShippingStatus(models.Model):
    order = models.ForeignKey(Order)
    status = models.CharField(max_length=120, default='Not Shipped', choices=SHIPPING_STATUS)
    tracking_number = models.CharField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return str(self.status)