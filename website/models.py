from django.db import models
from datetime import datetime

# Create your models here.
class contact_us(models.Model):
    name = models.CharField(max_length=1000000000,null=True)
    email = models.CharField(max_length=1000000000,null=True)
    subject = models.CharField(max_length=1000000000,null=True)
    message = models.CharField(max_length=1000000000,null=True)
   
class newsletter(models.Model):
    ndate = models.DateField(auto_now_add=True)
    email = models.CharField(max_length=1000000000,null=True)

    def __str__(self):
        return (str(self.ndate))
    

class distributor(models.Model):
    submission_date = models.DateField(default=datetime.now, blank=True)
    first_name = models.CharField(max_length=1000000000,null=True)
    lat_name = models.CharField(max_length=1000000000,null=True)
    email = models.CharField(max_length=1000000000,null=True)
    phone = models.CharField(max_length=1000000000,null=True)
    country = models.CharField(max_length=1000000000,null=True)
    company = models.CharField(max_length=1000000000,null=True)
    staff = models.CharField(max_length=1000000000,null=True)
    website = models.CharField(max_length=1000000000,null=True)
    comment = models.CharField(max_length=1000000000,null=True)

    def __str__(self):
        return (self.first_name)

class ProductData(models.Model):

    suspension_type = [
        ('Front-Suspension', 'Front-Suspension'),
        ('Rear-Suspension', 'Rear-Suspension'),

    ]

    product_category = [
        ('Featured', 'Featured'),
        ('Popular', 'Popular'),
        ('Best-Seller', 'Best-Seller'),
        ('New-Arrival', 'New-Arrival'),
        ('Deal-Zone', 'Deal-Zone'),

    ]

    model_no = models.CharField(max_length=1000000000,null=True)
    product_title = models.CharField(max_length=1000000000,null=True)
    product_description = models.CharField(max_length=1000000000,null=True)
    weight = models.CharField(max_length=1000000000,null=True)
    package = models.CharField(max_length=1000000000,null=True)
    price_per_pack = models.CharField(max_length=1000000000,null=True)
    price_per_unit = models.CharField(max_length=1000000000,null=True)
    image_file = models.FileField(upload_to='media',null=True,default="None")
    search_image_file = models.FileField(upload_to='media',null=True,default="None")
    make = models.CharField(max_length=1000000000,null=True)
    market = models.CharField(max_length=1000000000,null=True)
    model = models.CharField(max_length=1000000000,null=True)
    body = models.CharField(max_length=1000000000,null=True)
    year = models.CharField(max_length=1000000000,null=True)
    suspension_type = models.CharField(max_length=1000000000,choices=suspension_type,null=True)
    product_category = models.CharField(max_length=1000000000,choices=product_category,null=True)

class watchlist(models.Model):
    user_id = models.CharField(max_length=20,default='none')
    coin_ids = models.ManyToManyField(ProductData)

class addtocart(models.Model):
    user_id = models.CharField(max_length=20,default='none')
    coin_ids = models.ManyToManyField(ProductData)


class order(models.Model):
    order_status = [
    ('Approved', 'Approved'),
    ('Pending', 'Pending'),

]
    order_date = models.DateField(default=datetime.now, blank=True)
    user_id = models.CharField(max_length=20,default='none')
    coin_ids = models.ManyToManyField(ProductData)
    confirmation_no = models.CharField(max_length=1000000000,null=True)
    payment_proof = models.FileField(upload_to='payment_proof',null=True,default="None")
    status = models.CharField(max_length=1000000000,choices=order_status,null=True)



class Bank_details(models.Model):
    first_name = models.CharField(max_length=1000000000,null=True)
    last_name = models.CharField(max_length=1000000000,null=True)
    bank_name = models.CharField(max_length=1000000000,null=True)
    account_no = models.CharField(max_length=1000000000,null=True)

    def __str__(self):
        return (self.bank_name)

class zelle_details(models.Model):
    recipient_name = models.CharField(max_length=1000000000,null=True)
    email = models.CharField(max_length=1000000000,null=True)
    phone_no = models.CharField(max_length=1000000000,null=True)

    def __str__(self):
        return (self.recipient_name)
