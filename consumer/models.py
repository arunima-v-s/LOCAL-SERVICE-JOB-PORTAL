from django.db import models
from django.contrib.auth.models import User
from worker .models import Worker
from worker import models as wmodels

# Create your models here.

class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True, blank=True)  # Optional relationship
    phone = models.CharField(max_length=20, null=False)
    city = models.CharField(max_length=25, null=False)
    profile_pic = models.ImageField(upload_to='profile_pic', null=True, blank=True)
    status = models.CharField(max_length=20,default='Pending')

    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    
    def __str__(self):
        return self.user.username
    

class Booking(models.Model):
    STATUS = (
        ('Order Confirmed', 'Order Confirmed'),
        ('Delivered', 'Delivered'),
    )
    consumer = models.ForeignKey('Consumer', on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(wmodels.Services, on_delete=models.CASCADE, null=True)
    worker = models.ForeignKey(wmodels.Worker, on_delete=models.CASCADE, null=True)  # Add this line
    name = models.CharField(max_length=100, null=True)  # Add this line
    email = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=500, null=True)
    mobile = models.CharField(max_length=20, null=True)
    order_date = models.DateField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, null=True, choices=STATUS)
