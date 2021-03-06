import os
from django.db import models
from django.contrib.auth.models import User
import os
from django.core.files.storage import FileSystemStorage

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Disease(models.Model):
    disease_name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    disease_infor = models.CharField(max_length=500)
    total_people = models.IntegerField()
    fresh_people = models.IntegerField()

    def __str__(self):
        return self.disease_name


class Symptom(models.Model):
    symptom_name = models.CharField(max_length=30, default=" ")
    symptom_infor = models.CharField(max_length=500, default=" ")
    diseases = models.ManyToManyField(Disease)

    def __str__(self):
        return self.symptom_name


class Treatment(models.Model):
    treatment_name = models.CharField(max_length=30, default=" ")
    treatment_info = models.CharField(max_length=500, blank=True)
    type = models.CharField(max_length=30, default=" ")
    symptoms = models.ManyToManyField(Symptom)

    def __str__(self):
        return self.treatment_name


class Evaluation(models.Model):
    disease = models.ForeignKey(Disease, null=True)
    treatment = models.ForeignKey(Treatment)
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    choices = (('1', '少于1个月'), ('2', '1-6个月'), ('3', '6-12个月'), ('4', '1年以上'))
    use_time = models.CharField(max_length=2, choices=choices, blank=True)
    negative_score = models.IntegerField(default=0)
    positive_score = models.IntegerField(default=0)
    negative_symptoms = models.ManyToManyField(Symptom)

    def __str__(self):
        return str(str(self.id) + ' ' + self.treatment.treatment_name) + '价格：' + str(self.cost)


class UserInfo(models.Model):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    fs = FileSystemStorage(location='/media/head')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to=BASE_DIR+'/media/head')
    choice_index = (('F', '女'), ('M', '男'))
    sex = models.CharField(max_length=10, default="M", choices=choice_index)
    age = models.IntegerField()
    area = models.CharField(max_length=30, default=" ")
    person_infor = models.CharField(max_length=300, default=" ")
    diseases = models.ManyToManyField(Disease, blank=True)
    symptoms = models.ManyToManyField(Symptom, blank=True)
    treatments = models.ManyToManyField(Treatment, blank=True)
    evaluations = models.ManyToManyField(Evaluation, blank=True)
    is_diagnosed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Daily(models.Model):
    date = models.DateField()
    sleep = models.CharField(max_length=20, default=" ")
    energe = models.CharField(max_length=20, default=" ")
    appetite = models.CharField(max_length=20, default=" ")
    mood = models.CharField(max_length=20, default=" ")
    weight = models.FloatField()
    exercise_time = models.FloatField()
    user = models.ForeignKey(UserInfo)

    def __str__(self):
        return self.id


class Message(models.Model):
    user = models.ForeignKey(User)
    content = models.TextField()
    like = models.IntegerField(default=0)
    post_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + self.content[:5] + '...'


class Comment(models.Model):
    user = models.ForeignKey(User)
    content = models.CharField(max_length=200)
    message = models.ForeignKey(Message)
    post_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['post_time']


class Relation(models.Model):
    user1 = models.ForeignKey(User, related_name='user1')
    user2 = models.ForeignKey(User, related_name='user2')

    def __str__(self):
        return  self.user1.username + '  follow  ' + self.user2.username
