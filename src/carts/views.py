import datetime, json

from django.shortcuts import render, HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

from profiles.models import Profile
from profiles.forms  import ShippingAddressForm, BillingAddressForm
from products.models import Product, Variation

from orders.models import Order, ShippingStatus
from orders.custom import id_generator

from .models import Cart, CartItem


import stripe
import datetime
stripe.api_key = "sk_test_4Xq26ftwpl3AQ4oc30Nj3FPd"

def add_ajax(request):
    if request.is_ajax() and request.POST:
       #do some stuff and convert the stuff to json
        request.session.set_expiry(120000)
        
        try:
            the_id = request.session['cart_id']
        except:
            new_cart = Cart()
            new_cart.save()
            request.session['cart_id'] = new_cart.id
            the_id = new_cart.id
        
        cart = Cart.objects.get(id=the_id)

        slug = request.POST['slug']
        qty = request.POST['qty']
        try:
            product = Product.objects.get(slug=slug)
        except Exception:
            product = None

        product_var = [] #product variation

        for item in request.POST:
            key = item
            val = request.POST[key]
            try:
                #__iexact ignore upper/lower case 
                v = Variation.objects.get(product=product, category__iexact=key, title__iexact=val)
                product_var.append(v)
            except:
                pass

        #update the cart item.              
        cart_item = CartItem.objects.create(cart=cart, product=product)
        if len(product_var) > 0:
            cart_item.variations.add(*product_var)
        cart_item.quantity = qty
        cart_item.save()

        badge = cart.cartitem_set.count()
        new_data = json.dumps(badge)
        return HttpResponse(new_data, content_type='application/json')
       
    else:
        raise Http404        

#take any user as request, return the user's stripe_id
def add_stripe(user):
    profile, create = Profile.objects.get_or_create(user=user)
    if len(profile.stripe_id) > 2:
        print "exists"
        pass
    else:
        new_customer = stripe.Customer.create(
            email = user.email,
            description = "Added to stripe on %s" %(datetime.datetime.now())
        )    
        profile.stripe_id = new_customer.id
        profile.save()

    return profile.stripe_id



def view(request):
    try:
        the_id = request.session['cart_id']
    except:
        the_id = None
    if the_id:
        cart = Cart.objects.get(id=the_id)
        new_total = 0.00
        for item in cart.cartitem_set.all():
            line_total = float(item.product.price) * item.quantity
            new_total += line_total
        request.session['items_total'] = cart.cartitem_set.count()
        request.session['cart_items'] = len(cart.cartitem_set.all())
        cart.total = new_total
        cart.save()
        context = {"cart": cart}
        if request.session['items_total'] == 0:
             empty_message = "Your Cart is Empty."
             context = {"empty": True, "empty_message": empty_message}

    else:
        empty_message = "Your Cart is Empty."
        context = {"empty": True, "empty_message": empty_message}
    
    try: 
        stripe_id = add_stripe(request.user)
    except:
        pass

    template = "cart/view.html"
    return render(request, template, context)


def remove_from_cart(request, id):
    #If the cart doesn't exist, don't delete
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        return HttpResponseRedirect(reverse("cart"))

    cartitem = CartItem.objects.get(id=id)
    #cartitem.delete()
    cartitem.cart = None
    cartitem.save()
    #send "success message"

    return HttpResponseRedirect(reverse("cart"))
        

def add_to_cart(request, slug):
    request.session.set_expiry(120000)

    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id
    
    cart = Cart.objects.get(id=the_id)

    try:
        product = Product.objects.get(slug=slug)
    except Exception:
        product = None

    product_var = [] #product variation
    if request.method == "POST":
        qty = request.POST['qty']
        for item in request.POST:
            key = item
            val = request.POST[key]
            try:
                #__iexact ignore upper/lower case 
                v = Variation.objects.get(product=product, category__iexact=key, title__iexact=val)
                product_var.append(v)
            except:
                pass
        #update the cart item.              
        cart_item = CartItem.objects.create(cart=cart, product=product)
        if len(product_var) > 0:
            cart_item.variations.add(*product_var)
        cart_item.quantity = qty
        cart_item.save()
        # success message
        return HttpResponseRedirect(reverse("cart"))
    #error message
    return HttpResponseRedirect(reverse("cart"))


@login_required
def checkout(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        cart = False
        return HttpResponseRedirect(reverse("cart"))

    amount = int(cart.total * 100)
 
    try: 
        stripe_id = add_stripe(request.user)
    except:
        pass

    new_number = id_generator()
    shipping_address_form = ShippingAddressForm(request.POST or None)
    billing_address_form = BillingAddressForm(request.POST or None)

    new_order, created = Order.objects.get_or_create(cart=cart, user=request.user)
    if(created):
        new_order.order_id = str(new_number[:2]) + str(cart.id) + str(new_number[3:])
        new_order.user = request.user
        new_order.status = "Started"
        new_order.save()


    if request.method == "POST": 
        shipping_address_form = ShippingAddressForm(request.POST)
        billing_address_form = BillingAddressForm(request.POST)
        profile = request.user.get_profile()
        token = request.POST['stripeToken'] 
        customer = stripe.Customer.retrieve(stripe_id)
        #save the card into stripe for later use
        new_card = customer.cards.create(card=token)
       
        if billing_address_form.is_valid() and shipping_address_form.is_valid():
            form1 = shipping_address_form.save(commit=False)
            print form1  
            form2 = billing_address_form.save(commit=False)
            print form2 
            form1.user = request.user
            form2.user = request.user
            form1.is_shipping_address = True;
            form2.is_billing_address = True;

            #clean the data or the save_card will already be false ????
            if billing_address_form.cleaned_data['save_card'] == True:
                #save card info, and show the card with billing address only
                new_card.address_line1 = form2.address1
                if len(form2.address2) > 1:
                    new_card.address_line2 = form2.address2
                new_card.address_city = form2.city
                new_card.address_zip = form2.postal_code
                new_card.address_country = form2.country
                new_card.save()
                try:
                    form1.save()
                    form2.save()
                    print "form saved!"
                except:
                    pass    
            else:
                print 'did not save card'   
            charge = stripe.Charge.create (
                amount=amount,
                currency="usd",
                customer = customer.id,
                description = "Payment for order %s" %(new_order.order_id)
            )  

            if charge:
                print "charged!"
                new_order.status = 'Collected'
                new_order.cc_four = new_card.last4
                #we saved the form before     
                add_shipping = ShippingStatus(order=new_order)
                add_shipping.save()
                new_order.billing_address = form2
                new_order.shipping_address = form1
                #the order is done, we have all the info of the order saved
                new_order.save()
                #new_order.addresses.add(form2)  
                cart.user = request.user 
                #the cart should not be accessed anymore
                cart.active = False
                cart.save()
                #request.session.flush() --> delete the whole thing and also log the user out
                del request.session['cart_id']
                del request.session['cart_items']
                del request.session['items_total']
                return HttpResponseRedirect('/orders')


    template = "cart/checkout.html"
    context = {"cart": cart, "billing_address_form": billing_address_form, "shipping_address_form": shipping_address_form}
    return render(request, template, context)
