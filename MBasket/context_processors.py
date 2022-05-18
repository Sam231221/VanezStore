from .basket import Basket

#Basket(request) is gonna instantiate the Basket model
def basket(request):
    return {'basket': Basket(request)}

'''
for item in instantiate_basket:
    print(item)
{'price': Decimal('23.00'), 'qty': 1, 'product': <Product: Female Summer Shirt Pants>, 'total_price': Decimal('23.00')}
'''