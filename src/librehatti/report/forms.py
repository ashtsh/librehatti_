from django import forms
#from search_choices import CLIENT_FIELD_CHOICES,CLIENT_ORDER_CHOICES, CLIENT_ORDER_TYPES_CHOICES
#from search_choices import JOB_SEARCH_CHOICES
from search_choices import *


class ClientForm(forms.Form):
        client_fields = forms.MultipleChoiceField(required=False,
        widget=forms.CheckboxSelectMultiple, choices=CLIENT_FIELD_CHOICES)
        
       
        
        
class OrderForm(forms.Form):
        order = forms.MultipleChoiceField(required=False,
        widget=forms.CheckboxSelectMultiple, choices=CLIENT_ORDER_CHOICES)

