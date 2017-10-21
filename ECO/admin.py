from django.contrib import admin
from .models import Symptom, Treatment, Disease, User, Evaluation, Positive, Negative, Daily

admin.site.register([Symptom, Treatment, Disease, User, Evaluation, Positive, Negative, Daily])
