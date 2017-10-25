from django.urls import reverse
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response, \
    HttpResponse, HttpResponseRedirect

import json
from .method import load_data_for_disease_page
from .models import Symptom, Treatment, Disease, UserInfo, Evaluation,Daily

@csrf_exempt
def page_not_found(request):
    return render_to_response('404.html')

@csrf_exempt
def page_error(request):
    return render_to_response('500.html')

@csrf_exempt
def index(request):
    user = request.user
    if str(user) == 'AnonymousUser':
        return render(request, "ECO/index.html")
    else:
        return HttpResponseRedirect(reverse('ECO:home'))

@csrf_exempt
@login_required
def home(request):
    return render(request, "ECO/home.html")

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        info = request.POST
        username = info['username']
        password = info['password']
        try:
            User.objects.get(username=username)
        except Exception:
            result = {'status': 'error', 'error_message': 'user_not_exist'}
            return HttpResponse(json.dumps(result), content_type='application/json')
        user = authenticate(request=request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            try:
                info['remember_me']
            except Exception:
                request.session.set_expiry(0)
            result = {'status': 'success'}
            return HttpResponse(json.dumps(result), content_type='application/json')
        result = {'status': 'error', 'error_message': 'wrong_password'}
        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        return Http404("页面访问错误")

@csrf_exempt
def user_register(request):
    if request.method == "POST":
        info = request.POST
        username = info['username']
        try:
            User.objects.get(username=username)
        except Exception:
            password = info['password']
            email = info['email']
            sex = info['sex']
            age = info['age']
            area = info['area']
            try:
                User.objects.create_user(username, email, password).save()
            except Exception:
                result = {'status': 'error', 'error_message':'other'}
                return HttpResponse(json.dumps(result), content_type='application/json')
            else:
                user = User.objects.get(username=username)
                user.userinfo_set.create(sex=sex, age=int(age), area=area)
                result = {'status':'success'}
                return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            result = {'status': 'error', 'error_message':'user_exist'}
            return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        return Http404("页面访问错误")

@csrf_exempt
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('ECO:index'))

@csrf_exempt
def disease_index(request):
    all_disease = Disease.objects.all()
    context = {'all_disease':all_disease}
    return render(request,'ECO/disease_index.html',context)

@csrf_exempt
def symptom_index(request):
    pass

@csrf_exempt
def treatment_index(request):
    pass

@csrf_exempt
def person_index(request):
    pass

@csrf_exempt
def social_index(request):
    pass

@csrf_exempt
def disease_detail(request,disease_id):
    disease_name,disease_info, treatments_for_symptoms,treatments_for_disease,evaluations,ages,diagnosed,undiagnosed,num_men,num_women = load_data_for_disease_page(disease_id)
    context = {'treatments_for_symptoms':treatments_for_symptoms,'treatments_for_disease':treatments_for_disease}
    context['evaluations'] = evaluations
    context['ages'] = ages
    context['diagnosed'] = diagnosed
    context['undiagnosed'] = undiagnosed
    context['disease_info'] = disease_info
    context['num_men'] = num_men
    context['num_women'] = num_women
    context['disease_name'] = disease_name

    counts = []
    counts.append(len(treatments_for_symptoms))
    counts.append(len(treatments_for_disease))
    counts.append(len(evaluations))

    context['counts'] = counts

    return render(request,'ECO/disease_detail.html',context)
