from math import prod
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from MClothing.models import Product
from .basket import Basket
import json
from decimal import Decimal

class BasketAddView(View):
    def post(self, request):
        basket = Basket(request)
        data = json.loads(request.body)

        #Adding Or Updating from Product Modal
        prod_id = data['prod_id']
        prod_code = data['prod_code']
        prod_quantity = data['prod_quantity']
        prod_obj = Product.objects.get(id=prod_id, product_code=prod_code)#type class
        basket.add(product=prod_obj, qty=int(prod_quantity))
        
        #Sending Dictionary Values to Frontend
        context = basket.session['skey']
        print('----------------------')
        print('context:',context)
        for key in context:
            prod_obj = Product.objects.get(id=key)

            #append extra key value pairs
            context[key]['id'] = prod_obj.id
            context[key]['title'] = prod_obj.title
            context[key]['thumbnail'] = prod_obj.thumbnail

        print('\nvalues:',list(context.values()))
        return JsonResponse({'products':list(context.values()),
                                 'basketqty': basket.get_cart_items(),
                                 'basketsubtotal': basket.get_subtotal_price(),
                                 },
                                safe=False)


class BasketUpdateView(View):
    def post(self, request):
        basket = Basket(request)
        product_id = int(request.POST.get('prod_id'))
        product_qty = int(request.POST.get('prod_qty'))
        product_name = request.POST.get('prod_name')
        basket.update(product=product_id, qty=product_qty)
        basket=Basket(request)
        print('--------------------------')
        print(basket.session['skey'])
        basketlength = basket.__len__()#totalquantites

        #Get the basket sessionValues to Frontend
        context = basket.session['skey']
        for key in context:
            #append extra key value pair
            context[key]['totalprice'] =float(Decimal(context[key]['price']) * context[key]['qty'])

        response = JsonResponse({
            'products': list(context.values()),
             'basketqty': basket.get_cart_items(),
             'basketsubtotal': basket.get_subtotal_price(),
        }, safe=False)
        return response


class BasketDeleteView(View):
    def post(self, request):
        print("enetered")
        basket = Basket(request)
        prod_id=int(request.POST['prod_id'])
        basket.delete(product_id=prod_id)
        
        basketqty = basket.__len__()
        print("Updated Basket:", basket.session['skey'])           
        response = JsonResponse({
                'action':'delete',
                'delete_id':prod_id,
                'basketqty':basketqty,
                'basket_subtotal_price': basket.get_subtotal_price()
            }, safe=False)
        return response

