from django.contrib import admin
from .models import Order, ShippingStatus
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    search_fields = ['user', 'order_id']
    list_display = ['user', 'order_id', 'status', 'cart', 'billing_address', 'shipping_address']
    list_filter = ['user', 'status']
    readonly_fields = ['user', 'cart', 'order_id', 'cc_four']

    class Meta:
    	model = Order

    def get_readonly_fiels(self, request, obj=None):
        if obj:
            return ['order_id',]
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        return True    

admin.site.register(Order, OrderAdmin)	

class ShippingStatusAdmin(admin.ModelAdmin):
	class Meta:
		model = ShippingStatus

admin.site.register(ShippingStatus, ShippingStatusAdmin)			
    