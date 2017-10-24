from django.http import Http404
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response, \
    HttpResponse, HttpResponseRedirect, get_object_or_404, get_list_or_404

import json
from .method import *
from .models import *

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

def person_index(request):
    pass

def social_index(request):
    pass

def symptom_index(request):
    pass

def symptom_detail(request):
    pass

def disease_index(request):
    all_disease = Disease.objects.all()
    context = {'all_disease':all_disease}
    return render(request,'ECO/disease_index.html',context)

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

def treatment_index(request):
    all_treatment = Treatment.objects.all()
    context = {'all_treatment':all_treatment}
    return render(request,'ECO/treatment_index.html',context)

def treatment_detail(request,treatment_id):
    the_treatment,target_symptom_and_num,num_side,num_effect,num_cost,num_time,negative_symptoms,counts = load_data_for_treatment_page(treatment_id)
    context = {}
    context['the_treatment'] = the_treatment
    context['target_symptom_and_num'] = target_symptom_and_num
    context['num_side'] = num_side
    context['num_effect'] = num_effect
    context['num_cost'] = num_cost
    context['num_time'] = num_time
    context['negative_symptoms'] = negative_symptoms
    context['counts'] = counts

    return  render(request,'ECO/treatment_detail.html',context)


































