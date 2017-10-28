from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response, \
    HttpResponse, HttpResponseRedirect

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
        return render_to_response('404.html')


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
                user = User.objects.create_user(username, email, password)
                user.save()
            except Exception:
                result = {'status': 'error', 'error_message': 'other'}
                return HttpResponse(json.dumps(result), content_type='application/json')
            else:
                UserInfo(user=user, sex=sex, age=age, area=area).save()
                result = {'status': 'success'}
                return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            result = {'status': 'error', 'error_message': 'user_exist'}
            return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        return render_to_response('404.html')


@csrf_exempt
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('ECO:index'))


@csrf_exempt
def symptom_index(request):
    all_symptom = Symptom.objects.all()
    context = {'all_symptom': all_symptom}
    return render(request, 'ECO/symptom_index.html', context)


@csrf_exempt
def symptom_detail(request, symptom_id):
    keys = ['the_symptom', 'disease_and_num', 'treatment_and_evaluations', 'counts']
    values = load_data_for_symptom_page(symptom_id)
    context = dict(zip(keys, values))
    return render(request, 'ECO/symptom_detail.html', context)


@csrf_exempt
def disease_index(request):
    all_disease = Disease.objects.all()
    context = {'all_disease': all_disease}
    return render(request, 'ECO/disease_index.html', context)


@csrf_exempt
def disease_detail(request, disease_id):
    keys = ['disease', 'treatments_for_symptoms', 'treatments_for_disease',
            'evaluations', 'ages', 'diagnosed', 'undiagnosed', 'num_men', 'num_women']
    values = load_data_for_disease_page(disease_id)
    context = dict(zip(keys, values))
    context['counts'] = [len(context[keys[1]]), len(context[keys[2]]), len(context[keys[3]])]
    return render(request, 'ECO/disease_detail.html', context)


@csrf_exempt
def treatment_index(request):
    all_treatment = Treatment.objects.all()
    context = {'all_treatment': all_treatment}
    return render(request, 'ECO/treatment_index.html', context)


@csrf_exempt
def treatment_detail(request, treatment_id):
    keys = ['the_treatment', 'target_symptom_and_num', 'num_side',
            'num_effect', 'num_cost', 'num_time', 'negative_symptoms', 'counts']
    values = load_data_for_treatment_page(treatment_id)
    context = dict(zip(keys, values))
    return render(request, 'ECO/treatment_detail.html', context)


@csrf_exempt
@login_required
def person_index(request):
    """person_disease同"""
    user = request.user
    try:
        whole_user = user.userinfo
        disease_id = whole_user.diseases.all()[0].id
    except IndexError:
        return render_to_response('404.html')
    else:
        keys = ['disease', 'treatments_for_symptoms', 'treatments_for_disease',
                'evaluations', 'ages', 'diagnosed', 'undiagnosed', 'num_men', 'num_women']
        values = load_data_for_disease_page(disease_id)
        context = dict(zip(keys, values))
        return render(request, 'ECO/person_disease.html', context)


@csrf_exempt
@login_required
def person_symptom(request):
    user = request.user
    try:
        whole_user = user.userinfo
        disease_id = whole_user.diseases.all()[0].id
    except IndexError:
        return render_to_response('404.html')
    else:
        keys = ['disease', 'treatments_for_symptoms', 'treatments_for_disease',
                'evaluations', 'ages', 'diagnosed', 'undiagnosed', 'num_men', 'num_women']
        values = load_data_for_disease_page(disease_id)
        context = dict(zip(keys, values))
        return render(request, 'ECO/person_symptom.html', context)


@csrf_exempt
@login_required
def person_treatment(request):
    user = request.user
    try:
        whole_user = user.userinfo
        disease_id = whole_user.diseases.all()[0].id
    except IndexError:
        return render_to_response('404.html')
    else:
        keys = ['disease', 'treatments_for_symptoms', 'treatments_for_disease',
                'evaluations', 'ages', 'diagnosed', 'undiagnosed', 'num_men', 'num_women']
        values = load_data_for_disease_page(disease_id)
        context = dict(zip(keys, values))
        return render(request, 'ECO/person_treatment.html', context)


@csrf_exempt
@login_required
def person_info(request):
    pass


@csrf_exempt
@login_required
def person_update(request):
    pass


@csrf_exempt
@login_required
def person_diagram(request):
    pass


@csrf_exempt
@login_required
def social_index(request):
    return render(request, 'ECO/social_index.html')


@csrf_exempt
@login_required
def social_friendstate(request):
    user = request.user
    userinfo = user.userinfo
    follows = userinfo.you_follow.all()
    message = [f.message_set.all() for f in follows]
    context = {'message': message}
    return render(request, 'ECO/social_friendstate.html', context)


@csrf_exempt
@login_required
def social_friendlist(request):
    user = request.user
    follow_you_relation = user.user2.all()
    you_follow_relation = user.user1.all()

    you_follow = [r.user1 for r in follow_you_relation]
    follow_you = [r.user2 for r in you_follow_relation]
    context = {'you_follow': you_follow, 'follow_you': follow_you}
    return render(request, 'ECO/social_friendlist.html', context)


@csrf_exempt
@login_required
def social_sendstate(request):
    pass


@csrf_exempt
@login_required
def social_newfriend(request):
    pass


@csrf_exempt
@login_required
def social_heart(request):
    pass
