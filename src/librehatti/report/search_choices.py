CLIENT_FIELD_CHOICES = (
		('user__username', 'Name'),
    ('address__city', 'Address'),
	  ('telephone', 'Phone'),
	  ('date_joined','Date of Joining'),('company','Company'),
	  )
	  
CLIENT_ORDER_CHOICES=(('purchase_order__buyer_id__username','Buyer ID'),('item__name','Item'),('item__category__name','Category'),
		('qty','Quantity'),
		('item__price','Unit Price'),('price','Total Price'),('discount','Discount')
		,('purchase_order__is_debit','Debit'),
		)
