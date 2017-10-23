from django.http import Http404
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response, \
    HttpResponse, HttpResponseRedirect, get_object_or_404, get_list_or_404

import json
from .method import load_data_for_disease_page
from .models import Symptom, Treatment, Disease, UserInfo, Evaluation, Positive, Negative, Daily

@csrf_exempt
def page_not_found(request):
    return render_to_response('404.html')

@csrf_exempt
def page_error(request):
    return render_to_response('500.html')

@csrf_exempt
def index(request):
    return render(request, "ECO/index.html")

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        info = request.POST
        username = info['username']
        password = info['password']
        print(username, password)
        user = authenticate(request=request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return HttpResponse("ok", RequestContext(request))
        return HttpResponse("error", RequestContext(request))
    else:
        return HttpResponse("error", RequestContext(request))

@csrf_exempt
def user_register(request):
    if request.method == "POST":
        info = request.POST
        username = info['username']
        password = info['password']
        email = info['email']
        try:
            User.objects.create_user(username, email, password).save()
        except:
            return render_to_response('ECO/register.html', {'error_message', '注册失败'})
        else:
            return HttpResponseRedirect('/ECO/to_login')
    else:
        return render_to_response('ECO/register.html', {'error_message', '注册失败'})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/ECO')

@csrf_exempt
@login_required
def home(request):
    user = request.user
    print(user.username, user.email)
    return render(request, "ECO/home.html")

def disease_index(request):
    all_disease = Disease.objects.all()
    context = {'all_disease':all_disease}

    return render(request,'ECO/',context)

def disease_detail(request,disease_id):
    treatments_for_symptoms,treatments_for_disease,evaluations,ages,diagnosed,undiagnosed = load_data_for_disease_page(disease_id)
    context = {'treatments_for_symptoms':treatments_for_symptoms,'treatments_for_disease':treatments_for_disease}
    context['evaluations'] = evaluations
    context['ages'] = ages
    context['diagnosed'] = diagnosed
    context['undiagnosed'] = undiagnosed

    return render(request,'ECO/',context)
