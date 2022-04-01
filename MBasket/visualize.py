from urllib import request

basket.session = request.session

session = {'basket': <MBasket.basket.Basket object at 0x04853E50>}= 
{'skey':{
'9': {'price': '23.00',
'qty': 1
},
'8': {'price': '33.00',
'qty': 1
}
},
'\_auth_user_id': '1', '\_auth_user_backend': 'django.contrib.auth.backends.ModelBackend',
'\_auth_user_hash': '6fe56f13fdaa7f813ef5f5c05c6cdcca7173e832e70f70f508251f3d10224607'
}

#At initalization
basket= self.session.get('skey')= {
'8': {
    'price': '33.00',
    'qty': 1
    },
'9': {
    'price': '23.00',
    'qty': 1
    }
}

#when we loop the basket the basket will changed as def **iter**(self) is called
iter=self.session.get('skey')=[
{
'price': Decimal('23.00'),
'qty': 1,
'product': '<Product: Female Summer Shirt Pants>',
'total_price': Decimal('23.00')
},

        {
            'price': Decimal('33.00'),
            'qty': 1,
            'product': '<Product: Esprit Ruffle ShirtPant Pairs>',
            'total_price': Decimal('33.00')
        },

]

[{
'price': '33.00',
'qty': 1,
'title': 'Esprit Ruffle ShirtPant Pairs',
'thumbnail': 'https://res.cloudinary.com/dcgrv6shk/image/upload/v1648044862/VanezStore/product1_gypgoa.jpg'},

    {'price': '23.00',
    'qty': 2,
    'title': 'Esprit Ruffle ShirtPant Pairs',
     'thumbnail': 'https://res.cloudinary.com/dcgrv6shk/image/upload/v1648044862/VanezStore/product1_gypgoa.jpg'},

     {'price': '33.00',
      'qty': 1,
       'title': 'Esprit Ruffle ShirtPant Pairs',
       'thumbnail': 'https://res.cloudinary.com/dcgrv6shk/image/upload/v1648044862/VanezStore/product1_gypgoa.jpg'}

]

{'8': {'price': '33.00', 'qty': 1, 'title': 'Esprit Ruffle ShirtPant Pairs', 'thumbnail': 'https://res.cloudinary.com/dcgrv6shk/image/upload/v1648044862/VanezStore/product1_gypgoa.jpg'}, '9': {'price': '23.00', 'qty': 2, 'title': 'Esprit Ruffle ShirtPant Pairs', 'thumbnail': 'https://res.cloudinary.com/dcgrv6shk/image/upload/v1648044862/VanezStore/product1_gypgoa.jpg'}}
