from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import *


class UserInfoInline(admin.StackedInline):
    model = UserInfo
    filter_horizontal = ('diseases', 'symptoms', 'treatments', 'evaluations')
    extra = 1


class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff')
    inlines = (UserInfoInline,)


class UserinfoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'sex', 'age', 'area',)
    list_filter = ('age', 'area',)


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

class CommentInline(admin.StackedInline):
    model = Comment

class MessageAdmin(admin.ModelAdmin):
    inlines = (CommentInline,)

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

admin.site.register(UserInfo, UserinfoAdmin)
admin.site.register(Symptom, SymptomAdmin)
admin.site.register(Treatment, TreatmentAdmin)
admin.site.register(Disease, DiseaseAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(Daily, DailyAdmin)
admin.site.register(Relation, RelationAdmin)
admin.site.register(Message,MessageAdmin)