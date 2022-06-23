from django.db import models
from django.contrib.auth.models import AbstractUser

class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=80)
    country_code = models.CharField(max_length=5)

    def __str__(self):
        return str(self.country_name)

class State(models.Model):
    state_name =  models.CharField(max_length=80)
    state_id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.state_name)



class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=80)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.city_name)


class Address(models.Model):
    area_id = models.AutoField(primary_key=True)
    area_name = models.CharField(max_length=200)
    street_name = models.CharField(max_length=200)
    house_no = models.CharField(max_length=20)
    area_pincode = models.CharField(max_length=20)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.area_name)


class MyUser(AbstractUser):
    user_contact = models.BigIntegerField(null=True)
    gender = models.CharField(max_length=20)
    is_verified= models.BooleanField(default= False)
    is_admin = models.BooleanField(default = False)

    def __str__(self):
        return str(self.username)

class IdProof(models.Model):
    idproof_id = models.AutoField(primary_key=True)
    idproof_type = models.CharField(max_length=80)
    idproof_image = models.ImageField(upload_to = 'profile/')
    myuser = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.idproof_id)

# Create your models here.
