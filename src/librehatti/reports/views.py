"""
%% actions.py %%
This file contains the functions that will be used to generate registers.
"""

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

from helper import get_query

from django.shortcuts import render

from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import PurchasedItem
from librehatti.suspense.models import SuspenseOrder

from useraccounts.models import Customer

from datetime import datetime, timedelta

class SearchResult(View):

    def __init__(self):
        """
        Initializing required lists.
        """
	self.purchase_order_id='enable'
	
    	self.result_fields = []
        self.list_dict = {'name':'purchase_order__buyer__username', 
            'city':'purchase_order__buyer__customer__address__city',
            'phone':'purchase_order__buyer__customer__telephone',
            'joining date':'purchase_order__buyer__customer__date_joined',
            'company':'purchase_order__buyer__customer__company',
            
            'discount':'purchase_order__total_discount',
            'debit':'purchase_order__is_debit', 
	    'mode of payment':'purchase_order__mode_of_payment__method'
        }


    def view_register(self,request):
        """
        Converting data from dict to list form so that it can be render easily.
        Calling template to be rendered.
        """

    	generated_data_list = []

        for data in self.details:
        	temporary = []
        	for field in self.fields_list:
        		temporary.append(data[field])
        	generated_data_list.append(temporary)

        temp = {'client':self.selected_fields_client,
            'order':self.selected_fields_order, 'result':generated_data_list,
            'title':self.title,'order_id':self.purchase_order_id,'records':self.results
        }

        return render(request,'reports/search_result.html',temp)

        ''' def apply_filters(self,request):
        """
        Applying selected filters.
        """

        if 'date' in self.selected_fields_constraints:
            self.details = self.client_details.filter(
            	purchase_order__date_time__range = (
            		self.start_date,self.end_date))

        return self.view_register(request)'''
    
    def apply_filter(self,request):
	self.results=[]
	self.r=get_query(self.title,self.fields_list)
	self.found_entries = PurchasedItem.objects.filter(self.r)
	if 'Client' in request.GET:
		
		for entries in self.found_entries:
        		self.temp = []
                	for value in self.fields_list:
                 	       obj = PurchasedItem.objects.filter(id=entries.id).values(
                        	      value)
                      	       for temp_result in obj:
              	               	self.temp.append(temp_result)
                        self.results.append(self.temp)
        if 'Order' in request.GET:
                
		for entries in self.found_entries:
        		self.temp = []
                	for value in self.fields_list:
				try:
					if request.GET['suspense']:
						self.obj = SuspenseOrder.objects.filter(id=entries.id).values(value).filter(purchase_order__id=self.title)
				except:

                 	      		self.obj = PurchasedItem.objects.filter(id=entries.id).values(value).filter(purchase_order__id=self.title)
                      	        for temp_result in self.obj:
              	               		self.temp.append(temp_result)
                        self.results.append(self.temp)
        
        
        return self.view_register(request)

    
    def fetch_values(self,request):
        """
        Fetching values from database.
        """

    	self.details = PurchasedItem.objects.values(*self.fields_list).\
    	    filter(purchase_order__is_canceled = 0)

        return self.apply_filter(request)


    def convert_values(self,request):
        """
        Mapping selected values to there names specified in 'list_dict' in this
        file.
        """

    	self.fields_list = []
    	for value in self.selected_fields_client:
    		self.fields_list.append(self.list_dict[value])

        for value in self.selected_fields_order:
        	self.fields_list.append(self.list_dict[value])
	if 'Client' in request.GET:
		self.fields_list.append('purchase_order__buyer__id')	
	else: 
		self.fields_list.append('purchase_order__id')
	
        return self.fetch_values(request)


    def get(self,request):
        """
        Retrieve values from URL.
        Convert date into datetime format.
        """

    	

    	'''start_date_temp = datetime.strptime(request.GET['start_date'],
    		'%Y-%m-%d')
    	self.start_date = datetime(start_date_temp.year, start_date_temp.month, 
    		start_date_temp.day) + timedelta(hours=0) 

    	end_date_temp = datetime.strptime(request.GET['end_date'], '%Y-%m-%d')

        #adding 24 hours in date will convert '2014-8-10' to '2014-8-10 00:00:00'
    	
        self.end_date = datetime(end_date_temp.year, end_date_temp.month, 
    		end_date_temp.day) + timedelta(hours=24) '''
        self.title = request.GET['search']
        self.selected_fields_client = request.GET.getlist('client_fields')
        self.selected_fields_order = request.GET.getlist('order')
        #self.selected_fields_constraints = request.GET.getlist(
        	#'additional_constraints')
        self.result_fields.append(self.selected_fields_client)
        self.result_fields.append(self.selected_fields_order)

        return self.convert_values(request)

