from django.shortcuts import render
from django.shortcuts import render_to_response, HttpResponseRedirect, RequestContext, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

from .models import Order

def view(request):
    try:
    	orders = Order.objects.filter(user=request.user)
    except:
    	pass

    return render_to_response("orders/all.html", locals(), context_instance=RequestContext(request))

