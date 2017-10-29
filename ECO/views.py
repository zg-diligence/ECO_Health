from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response, \
    HttpResponse, HttpResponseRedirect

import json
import math
from .method import *
from .models import *

R = 100

@csrf_exempt
def page_not_found(request):
    return render_to_response('404.html')


@csrf_exempt
def page_error(request):
    return render_to_response('500.html')


@csrf_exempt
def index(request):
    # uesr = User.objects.get(username='li')
    # print(uesr.userinfo.image.name)
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

    # 计算治疗手段人数比例
    total_num = sum([treatment['num'] for treatment in context['treatments_for_disease']])
    for treatment in context['treatments_for_disease']:
        treatment['num_rate'] = 100*treatment['num']/total_num

    # 计算疗效评分人数比例
    print(context['evaluations'])
    for evaluation in context['evaluations']:
        score_sum = sum(evaluation['score'])
        # evaluation['score_rate'] = [40,20,10,20]
        evaluation['score_rate'] = [100*score/score_sum for score in evaluation['score']]

    # 计算年龄段比例
    context['age_rate'] = [100*num/sum(context['ages']) for num in context['ages']]

    # 计算男女比例 决定比例图参数
    men_to_wemen = values[-2]/(values[-2] + values[-1])
    cut_x = R*(1+math.cos(2*math.pi*men_to_wemen))
    cut_y = R*(1-math.sin(2*math.pi*men_to_wemen))
    if math.fabs(cut_x-200) < 1e-6 and math.fabs(cut_y-100) < 1e-6:
        cut_x, cut_y = 200.0, 100.0

    context['direction_1'] = '0' if cut_y < 100 else '1'
    context['direction_2'] = '1' if cut_y < 100 else '0'
    context['cut_off'] = str(cut_x) + " " + str(cut_y)
    print(context['cut_off'])

    # 计算就诊情况比例
    is_to_not = values[-4]/(values[-3]+values[-4])*100
    context['diagnosed_rate'] = is_to_not
    context['undiagnosed_rate'] = 100 - is_to_not

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

    # 计算治疗手段针对的各症状人数比例
    total_num = sum([item['num'] for item in context['target_symptom_and_num']])
    for item in context['target_symptom_and_num']:
        item['num_rate'] = 100*item['num']/total_num

    # 计算副作用各症状人数比例
    total_num = sum([item['num'] for item in context['negative_symptoms']])
    for item in context['negative_symptoms']:
        item['num_rate'] = 100*item['num']/total_num
        print(item['num_rate'])

    # 计算治疗手段有效性程度人数比例以及饼图参数
    # context['effect_rate'] = [0.2, 0.1, 0.3, 0.4]
    context['effect_rate'] = [num/sum(context['num_effect']) for num in context['num_effect']]
    context['effect_angle'] = [0 if rate < 0.5 else 1 for rate in context['effect_rate']]
    rate_sum = [sum(context['effect_rate'][:i]) for i in [1,2,3,4]]
    context['effect_cut_off'] = [str(R*(1+math.cos(2*math.pi*rate))) + ' ' + str(R*(1-math.sin(2*math.pi*rate))) for rate in rate_sum]
    # print(context['effect_rate'], context['effect_angle'], context['effect_cut_off'])

    # 计算治疗手段副作用程度人数比例以及饼图参数
    # context['side_rate'] = [0.2, 0.1, 0.3, 0.4]
    context['side_rate'] = [num/sum(context['num_side']) for num in context['num_side']]
    context['side_angle'] = [0 if rate < 0.5 else 1 for rate in context['side_rate']]
    rate_sum = [sum(context['side_rate'][:i]) for i in [1,2,3,4]]
    context['side_cut_off'] = [str(R*(1+math.cos(2*math.pi*rate))) + ' ' + str(R*(1-math.sin(2*math.pi*rate))) for rate in rate_sum]
    print(context['side_rate'], context['side_angle'], context['side_cut_off'])

    # 计算使用时长人数比例
    context['num_rate'] = [100*num/sum(context['num_time']) for num in context['num_time']]

    # 计算花销人数比例
    context['cost_rate'] = [100*num/sum(context['num_cost']) for num in context['num_cost']]

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
def person_disease(request):
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

    you_follow = [r.user1.userinfo for r in follow_you_relation]
    follow_you = [r.user2.userinfo for r in you_follow_relation]
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
