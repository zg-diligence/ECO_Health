from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect,  render_to_response
from .models import Symptom, Treatment, Disease, User, Evaluation, Positive, Negative, Daily
from .method import load_data_for_disease_page

# def Index(request):
#     return render(request, 'ECO/index.html')
#
# def Register(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(request, 'ECO/home.html')
#     else:
#         form = RegisterForm()
#     return render_to_response('ECO/register.html', {'form':form})
#
# def LoginWithUsername(request):
#     if request.method == "POST":
#         form = UsernameLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             if not User.objects.filter(username=username):
#                 return render_to_response("ECO/login.html", {'form': form, 'error': '用户不存在，请重新输入！'})
#             user = authenticate(username=username, password=password)
#             if user and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect('/ECO/home/')
#             else:
#                 return render_to_response("ECO/login.html", {'form': form, 'error': '密码不正确，请重新输入！'})
#     else:
#         form = UsernameLoginForm()
#         return render_to_response("ECO/login.html", {'form':form})
#
# def LoginWithEmail(request):
#     if request.method == "POST":
#         form = EmailLoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             if not User.objects.filter(email=email):
#                 return render_to_response("ECO/login.html", {'form': form, 'error': '用户不存在，请重新输入！'})
#             user = authenticate(email=email, password=password)
#             if user and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect('/ECO/home/')
#             else:
#                 return render_to_response("ECO/login.html", {'form': form, 'error': '密码不正确，请重新输入！'})
#     else:
#         form = EmailLoginForm()
#         return render_to_response("ECO/login.html", {'form':form})
#
# def LoginOut(request):
#     logout(request)
#     return HttpResponseRedirect('/index/')
#
# @login_required(login_url='/login_with_username')
# def Home(request):
#     if request.user.is_authenticated():
#         return render(request, 'ECO/home.html')
#     else:
#         return render(request, 'ECO/index.html')

def disease_index(request):
    all_disease = Disease.objects.all()
    context = {'all_disease':all_disease}

    return render(request,'ECO/disease_index',context)

def disease_detail(request,disease_id):
    treatments_for_symptoms,treatments_for_disease,evaluations,ages,diagnosed,undiagnosed = load_data_for_disease_page(disease_id)
    context = {'treatments_for_symptoms':treatments_for_symptoms,'treatments_for_disease':treatments_for_disease}
    context['evaluations'] = evaluations
    context['ages'] = ages
    context['diagnosed'] = diagnosed
    context['undiagnosed'] = undiagnosed

    return render(request,'ECO/disease_detail',context)































