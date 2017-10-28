from django.db import models
from django.contrib.auth.models import User

class Disease(models.Model):
    disease_name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    disease_infor = models.CharField(max_length=500)
    total_people = models.IntegerField()
    fresh_people = models.IntegerField()

    def __str__(self):
        return self.disease_name

class Symptom(models.Model):
    symptom_name = models.CharField(max_length=30,default=" ")
    symptom_infor = models.CharField(max_length=500,default=" ")
    diseases = models.ManyToManyField(Disease)

    def __str__(self):
        return self.symptom_name

class Treatment(models.Model):
    treatment_name = models.CharField(max_length=30,default=" ")
    treatment_info = models.CharField(max_length=500,blank=True)
    type = models.CharField(max_length=30,default=" ")
    symptoms = models.ManyToManyField(Symptom)

    def __str__(self):
        return self.treatment_name

class Evaluation(models.Model):
    treatment = models.ForeignKey(Treatment)
    cost = models.DecimalField(max_digits=6, decimal_places=2,default=0)
    choices = (('1','少于1个月'),('2','1-6个月'),('3','6-12个月'),('4','1年以上'))
    use_time = models.CharField(max_length=2,choices=choices,blank=True)
    negative_score = models.IntegerField(default=0)
    positive_score = models.IntegerField(default=0)
    negative_symptoms = models.ManyToManyField(Symptom)

    def __str__(self):
        return str(self.id)

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #require the dimension of image
    image = models.ImageField(height_field=50,width_field=50,blank=True)
    choice_index = (('F','女'),('M','男'))
    sex = models.CharField(max_length=10,default="M",choices=choice_index)
    age = models.IntegerField()
    area = models.CharField(max_length=30,default=" ")
    person_infor = models.CharField(max_length=300,default=" ")
    diseases = models.ManyToManyField(Disease,blank=True)
    symptoms = models.ManyToManyField(Symptom,blank=True)
    treatments = models.ManyToManyField(Treatment,blank=True)
    evaluations = models.ManyToManyField(Evaluation,blank=True)
    is_diagnosed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Daily(models.Model):
    date = models.DateField()
    sleep = models.CharField(max_length=20,default=" ")
    energe = models.CharField(max_length=20,default=" ")
    appetite = models.CharField(max_length=20,default=" ")
    mood = models.CharField(max_length=20,default=" ")
    weight = models.FloatField()
    exercise_time = models.FloatField()
    user = models.ForeignKey(UserInfo)

    def __str__(self):
        return self.id





















