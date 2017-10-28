from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Symptom, Treatment, Disease, \
    UserInfo, Evaluation,Daily,Relation

class UserInfoInline(admin.StackedInline):
    model = UserInfo
    filter_horizontal = ('diseases','symptoms','treatments','evaluations')
    extra = 1

class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff')
    inlines = (UserInfoInline,)

class SymptomAdmin(admin.ModelAdmin):
    filter_horizontal = ('diseases',)

class TreatmentAdmin(admin.ModelAdmin):
    filter_horizontal = ('symptoms',)

class DiseaseAdmin(admin.ModelAdmin):
    pass

class EvaluationAdmin(admin.ModelAdmin):
    filter_horizontal = ('negative_symptoms',)

class DailyAdmin(admin.ModelAdmin):
    pass

class RelationAdmin(admin.ModelAdmin):
    pass

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

admin.site.register(Symptom, SymptomAdmin)
admin.site.register(Treatment, TreatmentAdmin)
admin.site.register(Disease, DiseaseAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(Daily, DailyAdmin)
admin.site.register(Relation,RelationAdmin)
