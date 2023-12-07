import datetime

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import datetime

class Student(models.Model):
    c=(
        ("M","Male"),("F","Female")
    )
    name=models.CharField(max_length=250)
    email=models.EmailField(max_length=200)
    roll_no=models.IntegerField(unique=True)
    #date_of_birth=models.DateField(blank=True,default=None)
    fee=models.FloatField()
    gender=models.CharField(max_length=150,choices=c)
    address=models.TextField(blank=True)
    is_registered=models.BooleanField()

    def __str__(self):
        return self.name+" "+str(self.roll_no)
    class Meta:
        verbose_name_plural="Student"
class Contact_us(models.Model):

    name=models.CharField(max_length=250)
    contact_no=models.IntegerField(blank=True,unique=True)
    subject=models.CharField(max_length=250)
    message=models.TextField()
    added_on=models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="Contact Us"
class Category(models.Model):
    cat_name=models.CharField(max_length=250)
    cat_cover_pic=models.FileField(upload_to="categories/%y/%m/%d")
    cat_desciption=models.TextField()
    cat_added_on=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cat_name


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username}'s Wallet"


class register_table(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    contact_number=models.IntegerField()
    profile_pic=models.ImageField(upload_to="profiles/%y/%m/%d",null=True)
    city=models.CharField(max_length=250,null=True,blank=True)
    about=models.TextField(blank=True,null=True)
    gender=models.CharField(max_length=250,default="Male")
    added_on=models.DateField(auto_now_add=True,null=True)
    cat_added_on=models.DateField(auto_now=True,null=True)
    wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.user.username
class add_product(models.Model):
    item_chef=models.ForeignKey(User,on_delete=models.CASCADE)
    item_name=models.CharField(max_length=250)
    item_category=models.ForeignKey(Category,on_delete=models.CASCADE)
    item_price=models.FloatField()
    item_image=models.ImageField(upload_to="products/%y/%m/%d")
    item_details=models.TextField()

    def __str__(self):
        return self.item_name

ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Packed', 'Packed'),
        ('Delivered', 'Delivered'),
        ('Denied', 'Denied'),
    ]

class Order(models.Model):
    cust_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_orders')
    chef = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chef_orders', null=True, blank=True)
    cart_ids = models.CharField(max_length=250)
    delivery_address = models.TextField(blank=True)
    product_ids = models.CharField(max_length=250, default='')
    course_ids = models.CharField(max_length=250)
    invoice_id = models.CharField(max_length=250)
    status = models.BooleanField(default=False)
    processed_on = models.DateField(auto_now_add=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f'Order {self.id}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(add_product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.BooleanField(default=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='items')

    def __str__(self):
        return self.user.username
# models.py



# models.py






