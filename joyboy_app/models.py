from django.db import models
from django.contrib.auth.models import User

class post_category(models.Model):
    title=models.CharField(max_length=30)
    def __str__(self):
        return self.title
    
class posts(models.Model):
    title=models.CharField(max_length=25)
    post_category= models.ForeignKey(post_category,on_delete=models.CASCADE)
    image=models.ImageField()
    location=models.CharField(max_length=25)
    description=models.TextField()

class booking(models.Model):
    service_name=models.CharField(max_length=30)
    service_id=models.IntegerField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    phone_number=models.BigIntegerField()
    address=models.TextField()
    date=models.DateField()
    time=models.TimeField()
    def __str__(self):
        return self.name
    
class register(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=60)
    email=models.EmailField()
    address=models.TextField()
    photo=models.ImageField(upload_to='profile_pic')
    def __str__(self):
        return self.name
    


class Turf(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='turf_photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Add the amount field

    def __str__(self):
        return self.name
    
    

