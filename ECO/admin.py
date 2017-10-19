from django.contrib import admin
from .models import Symptom, Treatment, Condition, RegisterInfo, Patient

@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    pass

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    pass

@admin.register(RegisterInfo)
class RegisterInfo(admin.ModelAdmin):
    pass

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    pass

