from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect,  render_to_response

def Index(request):
    return render(request, 'ECO/index.html')

def Register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'ECO/home.html')
    else:
        form = RegisterForm()
    return render_to_response('ECO/register.html', {'form':form})

def LoginWithUsername(request):
    if request.method == "POST":
        form = UsernameLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if not User.objects.filter(username=username):
                return render_to_response("ECO/login.html", {'form': form, 'error': '用户不存在，请重新输入！'})
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/ECO/home/')
            else:
                return render_to_response("ECO/login.html", {'form': form, 'error': '密码不正确，请重新输入！'})
    else:
        form = UsernameLoginForm()
        return render_to_response("ECO/login.html", {'form':form})

def LoginWithEmail(request):
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if not User.objects.filter(email=email):
                return render_to_response("ECO/login.html", {'form': form, 'error': '用户不存在，请重新输入！'})
            user = authenticate(email=email, password=password)
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/ECO/home/')
            else:
                return render_to_response("ECO/login.html", {'form': form, 'error': '密码不正确，请重新输入！'})
    else:
        form = EmailLoginForm()
        return render_to_response("ECO/login.html", {'form':form})

def LoginOut(request):
    logout(request)
    return HttpResponseRedirect('/index/')

@login_required(login_url='/login_with_username')
def Home(request):
    if request.user.is_authenticated():
        return render(request, 'ECO/home.html')
    else:
        return render(request, 'ECO/index.html')

def UserInfo(request):
    return render(request, 'ECO/user_info.html')

def UserConditions(request):
    return render(request, 'ECO/user_conditions.html')

def UserSymptoms(request):
    return render(request, 'ECO/user_symptoms.html')

def UserTreatments(request):
    return render(request, 'ECO/user_treatments.html')

def DiseIndex(request):
    return render(request, 'ECO/dise_index.html')

def DiseOverview(request, dise_id):
    return render(request, 'ECO/dise_overview.html', {'dise_id': dise_id})

def DiseSymptoms(request, dise_id):
    return render(request, 'ECO/dise_symptoms.html', {'dise_id': dise_id})

def DiseTreatments(request, dise_id):
    return render(request, 'ECO/dise_treatments.html', {'dise_id': dise_id})

def DiseCompareTreatments(request):
    return render(request, 'ECO/dise_compare_treatments.html')

def DiseEvaluateTreatments(request):
    return render(request, 'ECO/dise_evaluate_treatments.html')

def InteractIndex(request):
    return render(request, 'ECO/interact_index.html')

def InteractPatients(request):
    return render(request, 'ECO/interact_patients.html')

def InteractUserSay(request):
    return render(request, 'ECO/interact_usersay.html')

def InteractAdvancedStudy(request):
    return render(request, 'ECO/interact_advanced_study.html')