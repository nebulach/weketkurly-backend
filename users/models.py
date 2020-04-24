from django.db import models


class User(models.Model):
    account     = models.CharField(max_length=45, null=False, unique=True)
    grade       = models.ForeignKey('Grade', models.SET_NULL, blank=True, null=True)
    password    = models.CharField(max_length=300)
    name        = models.CharField(max_length=45)
    email       = models.EmailField(max_length=100, null=False, unique=True)
    phone       = models.CharField(max_length=15)
    gender      = models.ForeignKey('Gender', models.SET_NULL, blank=True, null=True)
    birth       = models.CharField(max_length=15)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

class Gender(models.Model):
    name        = models.CharField(max_length=10)

    class Meta:
        db_table = 'genders'

class Grade(models.Model):
    name        = models.CharField(max_length = 10)
    info        = models.CharField(max_length = 45, blank = True, null = True)
    percentage  = models.DecimalField(max_digits = 3, decimal_places = 1)

    class Meta:
        db_table = 'grades'

class Address(models.Model):
    user            = models.ForeignKey('User', on_delete=models.CASCADE)
    address         = models.CharField(max_length=200)
    is_capital_area = models.BooleanField(default=False)

    class Meta:
        db_table = 'addresses'

