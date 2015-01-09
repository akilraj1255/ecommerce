from django.core.urlresolvers import reverse
from django.db import models
# Create your models here. Where the way the tables are looked like in your database
class ProductManager(models.Manager):
    def all(self):
        return super(ProductManager, self).filter(active=True).exclude(price=None).exclude(price=0)

    def custom_all(self):
        return super(ProductManager, self).filter(active=True).exclude(price=None).exclude(price=0)                    
    
    
PRODUCT_CATEGORIES = (
    ('tops', 'tops'),
    ('dresses', 'dresses'),
    ('outwear', 'outwear'),
    ('pants', 'pants'),
    ('shorts', 'shorts'),
    ('skirts', 'skirts'),
    ('sales', 'sales'),
)

class Product(models.Model):
    title = models.CharField(max_length=120, null=False, blank=False) 
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=100, default=29.99)
    sale_price = models.DecimalField(decimal_places=2, max_digits=100,\
                                                null=True, blank=True)
    slug = models.SlugField(unique=True)

    #first time, won't change when updated
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    #will change once updated
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)
    category = models.CharField(max_length=120, choices=PRODUCT_CATEGORIES, default='tops')
    
    objects = ProductManager()


    #instance method, python2.7 , python 3 doesn't recommond unicode
    def __unicode__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'slug')

    def get_price(self):
        return self.price

    def get_absolute_url(self):
        return reverse("single_product", kwargs={"slug": self.slug})  


class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to='products/images/')
    featured = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    description = models.BooleanField(default=False)
    size = models.BooleanField(default=False)
    front = models.BooleanField(default=False)
    back = models.BooleanField(default=False)
    detail = models.BooleanField(default=False)
    productSet = models.BooleanField(default=False)

    def __unicode__(self):
        return self.product.title




class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager, self).filter(active=True)

    def sizes(self):
        return self.all().filter(category='size')

    def colors(self):
        return self.all().filter(category='color')


VAR_CATEGORIES = (
    ('size', 'size'),
    ('color', 'color'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product)
    category = models.CharField(max_length=120, choices=VAR_CATEGORIES, default='size')
    title = models.CharField(max_length=120)
    image = models.ForeignKey(ProductImage, null=True, blank=True)
    price = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    objects = VariationManager()

    def __unicode__(self):
        return self.title



