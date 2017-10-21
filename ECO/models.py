from django.db import models

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
        self.symptom_name

class Treatment(models.Model):
    treatment_name = models.CharField(max_length=30,default=" ")
    type = models.CharField(max_length=30,default=" ")
    symptoms = models.ManyToManyField(Symptom)

class Evaluation(models.Model):
    treatment = models.ForeignKey(Treatment)
    score = models.IntegerField(default=-1)

class Positive(models.Model):
    from_eval = models.ForeignKey(Evaluation)
    #target  symptom
    symptom = models.ForeignKey(Symptom)

class Negative(models.Model):
    from_eval = models.ForeignKey(Evaluation)
    #side-effect
    symptom = models.ForeignKey(Symptom)

class User(models.Model):
    user_name = models.CharField(max_length=30,default=" ")
    pass_word = models.CharField(max_length=30,default=" ")
    email = models.EmailField()
    #require the dimension of image
    image = models.ImageField(height_field=50,width_field=50)
    sex = models.CharField(max_length=10,default=" ")
    age = models.IntegerField()
    area = models.CharField(max_length=30,default=" ")
    person_infor = models.CharField(max_length=300,default=" ")
    diseases = models.ManyToManyField(Disease)
    symptoms = models.ManyToManyField(Symptom)
    treatments = models.ManyToManyField(Treatment)
    evaluations = models.ManyToManyField(Evaluation)
    is_diagnosed = models.BooleanField()

    def __str__(self):
        return self.user_name

class Daily(models.Model):
    date = models.DateField()
    sleep = models.CharField(max_length=20,default=" ")
    energe = models.CharField(max_length=20,default=" ")
    appetite = models.CharField(max_length=20,default=" ")
    mood = models.CharField(max_length=20,default=" ")
    weight = models.FloatField()
    exercise_time = models.FloatField()
    user = models.ForeignKey(User)

























