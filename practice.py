SIZE_TUPLE = [
    ('Size S','Size S'),
    ('Size M','Size M'),
    ('Size L','Size L'),    
    ('Size XL','Size XL'),               
] 
list1, list2=list(), list()
for key,value in SIZE_TUPLE:
    list1.append(key)
    list2.append(value)
    
dict2={
    'sizes':dict(zip(list1, list2))
}
