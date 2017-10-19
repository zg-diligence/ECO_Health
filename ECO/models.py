from django.db import models

class Symptom(models.Model):
    pass

class Treatment(models.Model):
    pass

class Condition(models.Model):
    pass

class RegisterInfo(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=25)
    sex = models.CharField(max_length=10)
    birthday = models.DateField()

class Patient(models.Model):
    pass