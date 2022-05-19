from multiprocessing import context
from django.shortcuts import render
from django.views.generic import TemplateView, View
from MClothing.models import Product
from django.http.response import JsonResponse
from MBasket.basket import Basket
from .models import DeliveryOptions, Order, OrderItem ,BillingAddress
import datetime
from django.contrib.auth.models import User
import requests
class Home(TemplateView):
    template_name = 'frontendbase.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featuredproducts"] = Product.products.filter(is_featured=True).order_by('-id')[:4]
        context["recentproducts"] = Product.products.all().order_by('-published_on')[:4]
        
        return context

class SearchEngineView(View):
    def post(self, request):
        query = request.POST['keyword']
        print(query)
        product_queryset =  Product.products.filter(title__icontains=query)
        print(product_queryset)
        if len(product_queryset) > 0 and len(query) > 0:
            product_list = [] #inititae an empty list
            
            #Append all customer obj into the list using loop.
            for obj in product_queryset:
                item= {
                    'pk': obj.id,
                    'url': obj.get_absolute_url(),
                    'title': obj.title 
                }
                product_list.append(item)
            
            #now attach customer_list  to the response
            response = product_list    
        else:
            response = "Sorry, We don't currently have "+str(query)    

        return JsonResponse({'queryset':response}, safe=False)
        

class UserCartView(View):
    def get(self, request):
        basket = Basket(request)
        print('Total price:',basket.get_subtotal_price())
        return render(request, 'your-cart.html', {'basket': basket})


class CheckoutView(View):
    def get(self,request):
        basket = Basket(request)

        context={
            'deliveryoptions':DeliveryOptions.objects.all()
        }
        return render(request, 'checkout.html', context)

class GuestUserPaymentView(View):
    def get(self, request):
        print('--------------------')
        print('Guest User Payment View')
        basket = Basket(request)
        transaction_id = datetime.datetime.now().timestamp()

        token = request.GET.get("token")
        amount = request.GET.get("amount")

        deliveryid = request.GET.get('deliveryid')
        print(token, amount, deliveryid)
        print(basket.get_total_price() ,float(int(amount)/100))

        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
            "token": token,
            "amount": amount
        }
        headers = {
            "Authorization": "Key test_secret_key_de01b0c1f02b48759df0953a0dcfc8f0"
        }
        user_obj, created = User.objects.get_or_create(email=request.GET.get("email"))
        user_obj.username = request.GET.get("name")
        user_obj.save()

        order_obj = Order.objects.create(user=user_obj, complete=False)

        response = requests.post(url, payload, headers=headers)  # sending data to url
        resp_dict = response.json()

        if resp_dict.get("idx") and deliveryid and basket.get_total_price() ==  float(int(amount)/100):    
            userbillingaddress, created = BillingAddress.objects.get_or_create(user=user_obj)

            userbillingaddress.full_name = request.GET.get("name")
            userbillingaddress.email = request.GET.get("email")
            userbillingaddress.address = request.GET.get("address")
            userbillingaddress.city = request.GET.get("city")
            userbillingaddress.save()

            #attach items to the order
            for item in basket:
                OrderItem.objects.create(order=order_obj, product=item["product"], price=item["price"], quantity=item["qty"])
            
            # set transaction id and complete status
            order_obj.complete=True  
            order_obj.transaction_id = transaction_id
            order_obj.save()

            basket.clear()
            #Httporesonse or redirect won't work because we havhe use api and we have promises a json response
            return JsonResponse({'success':True}, safe=False)    
        else:
            return JsonResponse({'message':"Payment couldn't be completed", 'success':False}, safe=False)    
          


class LoggedInUserPaymentView(View):
    def get(self, request):
        print('Initaiting Khalti Verificatiion...')
        basket = Basket(request)
        transaction_id = datetime.datetime.now().timestamp()

        token = request.GET.get("token")
        amount = request.GET.get("amount")
        deliveryid = request.GET.get('deliveryid')
        print(token, amount, deliveryid)

        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
            "token": token,
            "amount": amount
        }
        headers = {
            "Authorization": "Key test_secret_key_de01b0c1f02b48759df0953a0dcfc8f0"
        }

        order_obj = Order.objects.create(user=request.user, complete=False)

        response = requests.post(url, payload, headers=headers)  # sending data to url
        resp_dict = response.json()
        print('idx:',resp_dict.get('idx')) 
        print(basket.get_total_price() ,float(int(amount)/100))
        if resp_dict.get("idx") and deliveryid and basket.get_total_price() ==  float(int(amount)/100):    
            #CREATE BILLING ADDRESS FOR NEW LOGGED IN USER FOR TANSPORTING GOODS
            #include created else userbillingaddress will be a tuple
            userbillingaddress, created = BillingAddress.objects.get_or_create(user=request.user)
            print( request.GET.get("fullname"),  request.GET.get("email"),  request.GET.get("address"),  request.GET.get("city"),  request.GET.get("zip"))
            userbillingaddress.full_name = request.GET.get("fullname")
            userbillingaddress.email = request.GET.get("email")
            userbillingaddress.phone = request.GET.get("phonenumber")
            userbillingaddress.address = request.GET.get("address")
            userbillingaddress.city = request.GET.get("city")
            userbillingaddress.postal_code = request.GET.get('zip')
            userbillingaddress.save()

            print('-------------------')
            print('creating')
            #attach items to the order
            for item in basket:
                OrderItem.objects.create(order=order_obj, product=item["product"], price=item["price"], quantity=item["qty"])
            
            # set transaction id and complete status
            order_obj.complete=True  
            order_obj.transaction_id = transaction_id
            order_obj.save()

            basket.clear()
            #Httporesonse or redirect won't work because we havhe use api and we have promises a json response
            return JsonResponse({'success':True}, safe=False)    
        else:
            return JsonResponse({'message':"Payment couldn't be completed", 'success':False}, safe=False)    
          
