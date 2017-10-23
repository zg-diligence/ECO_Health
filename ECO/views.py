from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, HttpResponseRedirect

from .method import load_data_for_disease_page
from .models import Symptom, Treatment, Disease, UserInfo, Evaluation,Daily

def index(request):
    return render(request, "ECO/index.html")

def to_register(request):
    return render(request, "ECO/register.html")

def to_login(request):
    return render(request, "ECO/login.html")

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
            return HttpResponseRedirect('/closends/to_login')
    else:
        return render_to_response('ECO/register.html', {'error_message', '注册失败'})

def user_login(request):
    if request.method == "POST":
        info = request.POST
        username = info['username']
        password = info['password']
        user = authenticate(request=request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/closends/home')
        return render_to_response('ECO/login.html', {'error_message', '登录失败'})
    else:
        return render_to_response('ECO/login.html', {'error_message', '登录失败'})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/closends/to_login')

@login_required
def home(request):
    user = request.user
    print(user.username, user.email)
    return render(request, "ECO/home.html")

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





























