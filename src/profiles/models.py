from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(User)
    fullname = models.CharField(max_length=120, null=True, blank=True) 
    nickname = models.CharField(max_length=120, null=True, blank=True) 
    address1 = models.CharField(max_length=300)
    address2 = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    country = models.CharField(max_length=300)
    postal_code = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)
    default_address = models.BooleanField(default=False)
    is_billing_address = models.BooleanField(default=False)
    is_shipping_address = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s: %s %s, %s, %s %s, %s' % (self.fullname, self.address1, self.address2, self.city
, self.state, self.country, self.postal_code)

class Profile(models.Model):
    user = models.ForeignKey(User)
    stripe_id = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __unicode__(self):
        return str(self.user)
