from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Symptom, Treatment, Disease, \
    UserInfo, Evaluation, Positive, Negative, Daily

class UserInfoInline(admin.StackedInline):
    model = UserInfo

class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff')
    inlines = (UserInfoInline,)

class SymptomAdmin(admin.ModelAdmin):
    pass

class TreatmentAdmin(admin.ModelAdmin):
    pass

class DiseaseAdmin(admin.ModelAdmin):
    pass

class EvaluationAdmin(admin.ModelAdmin):
    pass

class PositiveAdmin(admin.ModelAdmin):
    pass

class NegativeAdmin(admin.ModelAdmin):
    pass

class DailyAdmin(admin.ModelAdmin):
    pass

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

admin.site.register(Symptom, SymptomAdmin)
admin.site.register(Treatment, TreatmentAdmin)
admin.site.register(Disease, DiseaseAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(Positive, PositiveAdmin)
admin.site.register(Negative, NegativeAdmin)
admin.site.register(Daily, DailyAdmin)
