from decimal import Decimal
from MClothing.models import Product

class Basket():
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    
    Note in session key, there are key-value pairs. So
    You can try this:
    py manage.py shell
    from django.contrib.sessions.models import Session
    s= Session.objects.get(pk='2uyjd58ac565llkud7gr99lvgs5tr30u')
    s.get_decoded()
    
    Note: 1l7d8zc4bobr56kz4ui8ag6xpt39imuqis a value of sesssion id(you can get it by inspecting in browser)
    It returns dictionary with user_id key-value pair.That's why we can directly visit the page after first time when loginto site
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        
        #If there is no session id set a new one. basket should be set since if statement fails we get unknown arg
        if 'skey' not in self.session:
            basket = self.session['skey'] = {}  #basket = self.session['skey'] = {'test':234234}
            
        self.basket = basket
        print('\nAt Initialization, Basket Session Products:',self.basket)

        
    """
    Adding and updating the users basket session data
    """
    def add(self, product, qty):
        product_id = str(product.id) #get the product id
        
        if product_id not in self.basket:  #'skey'
            print('Adding new product id with new qty')
            self.basket[product_id] = {'price': str(product.price), 'qty': qty} #create
        
        if self.basket[product_id]['qty'] != qty:
            print('Updating Quantity for the existing product.') 
            self.basket[product_id]['qty'] = qty
       
        self.save()


    """
    Collect the product_id in the session data
    Append extra key: product and 'total_price' to basket dictionary
    
    Return products  for cart items while looping
    Used in CONTEXT_PROCESSORS
    """
    def __iter__(self):
        print('keys',self.basket.keys())
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)

        #but it reference to the same memory location
        basket = (
            self.basket.copy()
        )  
     
        #Append extra key value in existing basket dictionary.
        for product in products:
            #appending  new key 'product' in nested key
            basket[str(product.id)]['product'] = product
            

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = Decimal(item['price']) * item['qty']
            yield item
            
        print('\nIter:',basket)    

        
    """
    Get the basket data and count the qty of items
    self.basket.values()
    {'price': '23.00'},
    {'qty': 1}}
    """ 
    def __len__(self):
        return sum(item['qty'] for item in self.basket.values())


    """
    Update values in session dictionary
    """
    def update(self, product, qty):
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()

    def get_cart_items(self):
        count=0;
        for i in self.basket:
            print('key:',i)
            count=count+1
        return count
    
    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())


    def delete(self, product_id):
        """
        Delete item from session data
        """
        product_id = str(product_id)

        if product_id in self.basket:
            del self.basket[product_id]
            print(product_id)
            self.save()

    def save(self):
        self.session.modified = True