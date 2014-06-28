 # Create your views here.
from django.http import HttpResponse
from useraccounts.models import *
from helper import *
from forms import *
from django.shortcuts import render
from librehatti.catalog.models import *
import datetime
from django.db.models import Sum

def bill(request):
    
    purchased_item = PurchasedItem.objects.get(pk=1)
    purchase_order = PurchaseOrder.objects.get(pk=2)
    purchaseditem= PurchasedItem.objects.values('item','price','qty')
    per_price = purchased_item.item.price
    total=PurchasedItem.objects.filter(id=1).aggregate(Sum('price'))
    date= datetime.datetime.now()
    bill_date=purchase_order.date_time      
    delivery_address=purchase_order.delivery_address
    organisation=purchase_order.organisation
    buyer_id=purchase_order.buyer_id
    
    return render(request, 'bill.html', { 'STC_No':'1', 'PAN_No' :'12',
    'date': date, 'delivery_address' : delivery_address, 
    'Organisation' : organisation,'buyer_id' : buyer_id, 'L_No.': '123',
    'bill_date': bill_date,'purchaseditem' : purchaseditem,'per_price': per_price, 'total_cost': total, 'p': purchased_item })




def index(request):
  client_form = ClientForm()
  order_form = OrderForm()
  temp = {'client_form':client_form,'order_form':order_form}
  return render(request, 'index.html',temp)


def display(request):
    title = 'Search'
    results=[]
    avail_list = ['user__username', 'address__city','telephone','date_joined','company']
    avail_list2=['purchase_order__buyer_id__username','qty','item__price','item__category__name','item__name','discount','purchase_order__is_debit','price']
    #avail_list3=['is_debit']
    if 'Client' in request.GET:
        if 'client_fields' in request.GET:
          info = request.GET.getlist('client_fields')
          
          query_string = ''
          found_entries = None
          if ('q' in request.GET) and request.GET['q'].strip():
            query_string = request.GET['q']
            entry_query = get_query(query_string,info)
            found_entries = Customer.objects.filter(entry_query)
            for j in found_entries:
              for i in avail_list:
                if i in info:
                  obj = Customer.objects.filter(id=j.id).values(i)
                  results.append(obj)


                    

    if 'Order' in request.GET: 

      if 'order' in request.GET:
        order = request.GET.getlist('order')
        query_string = ''
        found_entries = None
        if ('q' in request.GET) and request.GET['q'].strip():
            query_string = request.GET['q']
            entry_query = get_query(query_string,order)
            found_entries = PurchasedItem.objects.filter(entry_query)
            for j in found_entries:
              for i in avail_list2:
                if i and 'purchase_order__is_debit' in order:
                  obj = PurchasedItem.objects.filter(id=j.id).filter(purchase_order__is_debit=True).values(i)
                  results.append(obj)
                elif i in order:  
                  obj = PurchasedItem.objects.filter(id=j.id).values(i)
                  results.append(obj)
         
    if 'q' in request.GET:
       title = request.GET['q']
 
    return render(request, 'display.html', {'results':results,'title': title})

