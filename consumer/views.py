from django.shortcuts import render,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from worker import models as wmodels
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

# Create your views here.

def consumer_signup_view(request):
    userform=forms.ConsumerUserForm()
    consumerform=forms.ConsumerForm()
    mydict={'userform':userform,'consumerform':consumerform}
    if request.method == 'POST':
        userform=forms.ConsumerUserForm(request.POST)
        consumerform=forms.ConsumerForm(request.POST,request.FILES)
        if userform.is_valid() and consumerform.is_valid():
            user=userform.save()
            user.set_password(user.password)
            user.save()
            consumer=consumerform.save(commit=False)
            consumer.user=user
            consumer.save()
            my_consumer_group = Group.objects.get_or_create(name='CONSUMER')
            my_consumer_group[0].user_set.add(user)
        return HttpResponseRedirect('consumerlogin')
    return render(request,'consumer/consumer_signup.html',context=mydict)

def consumer_dashboard_view(request):
    services = wmodels.Services.objects.all()
    return render(request,'consumer/consumer_dashboard.html',{'services':services})

def consumer_profile_view(request):
    consumer = models.Consumer.objects.get(user_id=request.user.id)
    return render(request,'consumer/profile.html',{'consumer':consumer})

def search_view(request):
    query = request.GET['query']
    services = wmodels.Services.objects.all().filter(skills=query)
    if 'service_ids' in request.COOKIES:
        service_ids = request.COOKIES['service_ids']
        counter=service_ids.split('|')
        service_count_in_cart=len(set(counter))
    else:
        service_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'consumer/consumer_dashboard.html',{'services':services,'word':word,'service_count_in_cart':service_count_in_cart})
    return render(request,'consumer/consumer_dashboard.html',{'services':services,'word':word,'service_count_in_cart':service_count_in_cart})


def add_to_cart_view(request,pk):
    services = wmodels.Services.objects.all()

    # For cart counter, fetching product IDs added by the customer from cookies
    if 'service_ids' in request.COOKIES:
        service_ids = request.COOKIES['service_ids']
        counter = service_ids.split('|')
        service_count_in_cart = len(set(counter))
    else:
        service_count_in_cart = 1

    # If the user is not authenticated, redirect to login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('consumerlogin'))  # Assuming 'login' is the URL name for the login page

    # If the user is authenticated, proceed with adding product to cart
    response = render(request, 'consumer/consumer_dashboard.html', {'services': services, 'service_count_in_cart': service_count_in_cart})

    # Adding product ID to cookies
    if 'service_ids' in request.COOKIES:
        service_ids = request.COOKIES['service_ids']
        if service_ids == "":
            service_ids = str(pk)
        else:
            service_ids = service_ids + "|" + str(pk)
        response.set_cookie('service_ids', service_ids)
    else:
        response.set_cookie('service_ids', pk)

    service = wmodels.Services.objects.get(id=pk)
    # messages.info(request, service.name + ' added to cart successfully!')

    return response

def cart_view(request):
    #for cart counter
    if 'service_ids' in request.COOKIES:
        service_ids = request.COOKIES['service_ids']
        counter=service_ids.split('|')
        service_count_in_cart=len(set(counter))
    else:
        service_count_in_cart=0

    # fetching product details from db whose id is present in cookie
    services=None
    total=0
    if 'service_ids' in request.COOKIES:
        service_ids = request.COOKIES['service_ids']
        if service_ids != "":
            service_id_in_cart=service_ids.split('|')
            services=wmodels.Services.objects.all().filter(id__in = service_id_in_cart)

            #for total price shown in cart
            for s in services:
                total += float(s.service_rate)
    return render(request,'consumer/cart.html',{'services':services,'total':total,'service_count_in_cart':service_count_in_cart})

def remove_service_from_cart(request,pk):
    if 'service_ids' in request.COOKIES:

        service_ids = request.COOKIES['service_ids']
        counter=service_ids.split('|')
        service_count_in_cart=len(set(counter))
    else:
        service_count_in_cart=0

    # removing product id from cookie
    total=0
    if 'service_ids' in request.COOKIES:
        service_ids = request.COOKIES['service_ids']
        service_id_in_cart=service_ids.split('|')
        service_id_in_cart=list(set(service_id_in_cart))
        service_id_in_cart.remove(str(pk))
        services=wmodels.Services.objects.all().filter(id__in = service_id_in_cart)
        #for total price shown in cart after removing product
        for s in services:
            total += float(s.service_rate)

        #  for update coookie value after removing product id in cart
        value=""
        for i in range(len(service_id_in_cart)):
            if i==0:
                value=value+service_id_in_cart[0]
            else:
                value=value+"|"+service_id_in_cart[i]
        response = render(request, 'consumer/cart.html',{'services':services,'total':total,'service_count_in_cart':service_count_in_cart})
        if value=="":
            response.delete_cookie('service_ids')
        response.set_cookie('service_ids',value)
        return response
    
# def consumer_address_view(request):
#     # this is for checking whether product is present in cart or not
#     # if there is no product in cart we will not show address form
#     service_in_cart=False
#     if 'service_ids' in request.COOKIES:
#         service_ids = request.COOKIES['service_ids']
#         if service_ids != "":
#             service_in_cart=True
#     #for counter in cart
#     if 'service_ids' in request.COOKIES:
#         service_ids = request.COOKIES['service_ids']
#         counter=service_ids.split('|')
#         service_count_in_cart=len(set(counter))
#     else:
#         service_count_in_cart=0

#     addressForm = forms.AddressForm()
#     if request.method == 'POST':
#         addressForm = forms.AddressForm(request.POST)
#         if addressForm.is_valid():
#             # here we are taking address, email, mobile at time of order placement
#             # we are not taking it from customer account table because
#             # these thing can be changes
#             name = addressForm.cleaned_data['name']
#             mobile=addressForm.cleaned_data['mobile']
#             address = addressForm.cleaned_data['address']
#             #for showing total price on payment page.....accessing id from cookies then fetching  price of product from db
#             total=0
#             if 'service_ids' in request.COOKIES:
#                 service_ids = request.COOKIES['service_ids']
#                 if service_ids != "":
#                     service_id_in_cart=service_ids.split('|')
#                     services=wmodels.Services.objects.all().filter(id__in = service_id_in_cart)
#                     for s in services:
#                         total += float(s.service_rate)

#             response = render(request, 'consumer/payment.html',{'total':total})
#             response.set_cookie('name',name)
#             response.set_cookie('mobile',mobile)
#             response.set_cookie('address',address)
#             return response
#     return render(request,'consumer/consumer_address.html',{'addressForm':addressForm, 'service_in_cart':service_in_cart ,'service_count_in_cart':service_count_in_cart})

def consumer_address_view(request):
    service_in_cart = False
    if 'service_ids' in request.COOKIES:
        service_ids = request.COOKIES['service_ids']
        if service_ids:
            service_in_cart = True

    # Count services in the cart
    service_count_in_cart = len(set(service_ids.split('|'))) if service_in_cart else 0

    addressForm = forms.AddressForm()
    if request.method == 'POST':
        addressForm = forms.AddressForm(request.POST)
        if addressForm.is_valid():
            name = addressForm.cleaned_data['name']
            mobile = addressForm.cleaned_data['mobile']
            address = addressForm.cleaned_data['address']
            total = 0
            
            # Calculate total price
            if service_in_cart:
                service_id_in_cart = service_ids.split('|')
                services = wmodels.Services.objects.filter(id__in=service_id_in_cart)
                total = sum(float(s.service_rate) for s in services)

            # Save the booking and redirect to waiting page
            consumer = models.Consumer.objects.get(user_id=request.user.id)
            for service in services:
                models.Booking.objects.create(
                    consumer=consumer,
                    service=service,
                    status='Pending',
                    name=name,
                    mobile=mobile,
                    address=address,
                )

            # Set cookies for the next step if needed
            response = render(request, 'consumer/waiting.html', {'total': total})
            response.set_cookie('total', total)
            return response

    return render(request, 'consumer/consumer_address.html', {
        'addressForm': addressForm,
        'service_in_cart': service_in_cart,
        'service_count_in_cart': service_count_in_cart
    })

def payment_view(request):
    return render(request,'consumer/payment.html')

def payment_success_view(request):
    consumer = models.Consumer.objects.get(id=request.user.id)
    services = None
    name = None
    mobile = None
    address = None

    if 'service_ids' in request.COOKIES:
        service_ids = request.COOKIES['service_ids']
        if service_ids:
            service_id_in_cart = service_ids.split('|')
            services = wmodels.Services.objects.filter(id__in=service_id_in_cart)

    # Accessing customer details from cookies
    if 'name' in request.COOKIES:
        name = request.COOKIES['name']
    if 'mobile' in request.COOKIES:
        mobile = request.COOKIES['mobile']
    if 'address' in request.COOKIES:
        address = request.COOKIES['address']

    # Check if services is not None or empty before iterating
    if services:
        for service in services:
            models.Booking.objects.get_or_create(
                consumer=consumer,
                service=service,
                status='Pending',
                name=name,
                mobile=mobile,
                address=address,
            )

    # Deleting cookies after order is placed
    response = render(request, 'consumer/payment_success.html')
    response.delete_cookie('service_ids')
    response.delete_cookie('name')
    response.delete_cookie('mobile')
    response.delete_cookie('address')
    return response


def my_bookings_view(request):
    # Get the consumer associated with the logged-in user
    consumer = models.Consumer.objects.get(user_id=request.user.id)
    
    # Fetch all bookings for the logged-in consumer
    bookings = models.Booking.objects.filter(consumer=consumer)
    
    booked_services = []
    
    for booking in bookings:
        # Fetch the service associated with each booking
        booked_service = booking.service  # Directly access the service related to the booking
        booked_services.append(booked_service)

    # Zip the booked services and bookings together for rendering
    data = zip(booked_services, bookings)

    return render(request, 'consumer/my_bookings.html', {'data': data})

def delete_booking_from_mybookings(request,pk):
    consumer = models.Consumer.objects.get(user_id=request.user.id)

    # Get the booking object to delete
    booking = get_object_or_404(models.Booking, id=pk, consumer=consumer)

    # Delete the booking
    booking.delete()
    
    # Show a success message
    messages.success(request, "Booking deleted successfully.")

    # Redirect back to the My Bookings page
    return redirect('my-bookings') 