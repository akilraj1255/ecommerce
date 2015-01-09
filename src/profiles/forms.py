from django import forms
from .models import Address

#make the address form
class ShippingAddressForm(forms.ModelForm):
	#same_as_billing= forms.BooleanField(initial=False, required=True);

	class Meta:
		model = Address
		fields = ('fullname', 'address1', 'address2', 'city', 'state', 'country', 'postal_code') 


#make the address form
class BillingAddressForm(forms.ModelForm):
	save_card = forms.BooleanField(initial=True, required=False);

	class Meta:
		model = Address
		fields = ('fullname', 'address1', 'address2', 'city', 'state', 'country', 'postal_code')



