#register our app into the admin, as we can see in the admin
from django.contrib import admin

# Register your models here.
from .models import Address, Profile

class AddressAdmin(admin.ModelAdmin):
	class Meta:
		model = Address
		fields = '__all__'

admin.site.register(Address, AddressAdmin)


class ProfileAdmin(admin.ModelAdmin):
	class Meta:
		model = Profile
		fields = '__all__'

admin.site.register(Profile, ProfileAdmin)