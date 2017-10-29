from .models import Symptom, Treatment, Disease, UserInfo, Evaluation, Daily

#by disease's name , get the related symptoms and treatments
def load_data_for_disease_page(disease_id):
    the_disease = Disease.objects.get(id=disease_id)
    symptoms = the_disease.symptom_set.all()
    #treatment for symptom which this disease has
    #treatments_for_symptoms = [ {'treatments':[],'symptom':symptom},  ...]
    treatments_for_symptoms = []

    for symptom in symptoms:
        treatments = symptom.treatment_set.all()
        temp = {}
        temp['treatments'] = treatments
        temp['symptom'] = symptom
        treatments_for_symptoms.append(temp)

    treatments_for_disease = []
    patients = the_disease.userinfo_set.all()

    #count the people of each treatment
    #treatments_for_disease[treatment.treatment_name][0] represent the num ,and [1] represent the object
    #treatments_for_disease = [ {'type':'处方药'，'num':23,'treatment':treatment} , ... ]
    for patient in patients:
        treatments = patient.treatments.all()
        for treatment in treatments:
            flag = False
            index = 0
            for i,t in enumerate(treatments_for_disease):
                if t['treatment'].treatment_name == treatment.treatment_name:
                    flag = True
                    index = i
                    break

            if flag:
                treatments_for_disease[index]['num'] += 1

            else:
                temp = {}
                temp['type'] = treatment.type
                temp['num'] = 1
                temp['treatment'] = treatment
                treatments_for_disease.append(temp)


    #count the age  diagnosed  sex evaluations
    #evaluations = [  {'treatment':treatment ,'num':20, 'score':[22,44,56,44], 'symptom':[...]}, .....]
    evaluations = []
    ages = [0,0,0,0,0,0]
    diagnosed = 0
    undiagnosed = 0
    num_men = 0
    num_women = 0
    for patient in patients:
        if patient.age < 20:
            ages[0] += 1
        elif patient.age < 30:
            ages[1] += 1
        elif patient.age < 40:
            ages[2] += 1
        elif patient.age < 50:
            ages[3] += 1
        elif patient.age < 60:
            ages[4] += 1
        else:
            ages[5] += 1

        if patient.is_diagnosed:
            diagnosed += 1
        else:
            undiagnosed += 1

        if patient.sex == 'M':
            num_men += 1
        else:
            num_women += 1

        patient_evalutions = patient.evaluations.all()
        for evaluation in patient_evalutions:
            treatment_name = evaluation.treatment.treatment_name
            flag = False
            index = 0
            for i,e in enumerate(evaluations):
                if treatment_name == e['treatment'].treatment_name:
                    flag = True
                    index = i
                    break

            if flag:
                evaluations[index]['num'] += 1


                if evaluation.positive_score <= 25:
                    evaluations[index]['score'][0] += 1
                elif evaluation.positive_score <= 50:
                    evaluations[index]['score'][1] += 1
                elif evaluation.positive_score <= 75:
                    evaluations[index]['score'][2] += 1
                else:
                    evaluations[index]['score'][3] += 1

                negative_symptoms = evaluation.negative_symptoms.all()
                for negative_symptom in negative_symptoms:
                    if negative_symptom in evaluations[index]['symptom']:
                        continue

                    else:
                        evaluations[index]['symptom'].append(negative_symptom)

            else:
                temp = {}
                temp['treatment'] = evaluation.treatment
                temp['num'] = 1
                temp['score'] = [0,0,0,0]
                temp['symptom'] = []
                negative_symptoms = evaluation.negative_symptoms.all()
                for negative_symptom in negative_symptoms:
                    if negative_symptom in temp['symptom']:
                        continue

                    else:
                        temp['symptom'].append(negative_symptom)

                if evaluation.positive_score <= 25:
                    temp['score'][0] += 1
                elif evaluation.positive_score <= 50:
                    temp['score'][1] += 1
                elif evaluation.positive_score <= 75:
                    temp['score'][2] += 1
                else:
                    temp['score'][3] += 1

                evaluations.append(temp)

    return the_disease,treatments_for_symptoms,treatments_for_disease,evaluations,ages,diagnosed,undiagnosed,num_men,num_women

def load_data_for_treatment_page(treatment_id):
    the_treatment = Treatment.objects.get(id=treatment_id)
    taget_symptoms = the_treatment.symptoms.all()

    #[ {'symptom':symptom1,'num':23} .....  ]
    target_symptom_and_num = []

    for s in taget_symptoms:
        temp = {}
        temp['symptom'] = s
        temp['num'] = len(s.userinfo_set.all())
        target_symptom_and_num.append(temp)

    num_side = [0,0,0,0]
    num_effect = [0,0,0,0]
    num_cost = [0,0,0,0,0]
    num_time = [0,0,0,0]
    #[ {'symptom':symptom,'num':22} .....  ]
    negative_symptoms = []

    for e in the_treatment.evaluation_set.all():

        if e.positive_score <=25:
            num_effect[0] += 1
        elif e.positive_score <= 50:
            num_effect[1] += 1
        elif e.positive_score <= 75:
            num_effect[2] += 1
        else:
            num_effect[3] += 1

        if e.negative_score <= 25:
            num_side[0] += 1
        elif e.negative_score <= 50:
            num_side[1] += 1
        elif e.negative_score <= 75:
            num_side[2] += 1
        else:
            num_side[3] += 1

        if e.use_time == '1':
            num_time[0] += 1
        elif e.use_time == '2':
            num_time[1] += 1
        elif e.use_time == '3':
            num_time[2] += 1
        else:
            num_time[3] += 1

        if e.cost <= 100:
            num_cost[0] += 1
        elif e.cost <= 200:
            num_cost[1] += 1
        elif e.cost <= 500:
            num_cost[2] += 1
        elif e.cost <= 1000:
            num_cost[3] += 1
        else:
            num_cost[4] += 1

        for s in e.negative_symptoms.all():
            flag = False
            index = 0
            for i,x in enumerate(negative_symptoms):
                if x['symptom'].symptom_name == s.symptom_name:
                    flag = True
                    index = i
                    break
            if flag:
                negative_symptoms[index]['num'] += 1
            else:
                temp = {}
                temp['symptom'] = s
                temp['num'] = 1
                negative_symptoms.append(temp)

    counts = []
    counts.append(len(target_symptom_and_num))
    counts.append(len(negative_symptoms))
    counts.append(sum(num_cost))

    return the_treatment,target_symptom_and_num,num_side,num_effect,num_cost,num_time,negative_symptoms,counts

def load_data_for_symptom_page(symptom_id):
    the_symptom = Symptom.objects.get(id=symptom_id)
    diseases = the_symptom.diseases.all()
    treatments = the_symptom.treatment_set.all()

    #[ {'disease':disease1,'num':22} .....  ]
    disease_and_num = []
    for disease in diseases:
        temp = {}
        temp['num'] = disease.total_people
        temp['disease'] = disease
        disease_and_num.append(temp)

    #[ {'treatment':t1,'num':33,'num_effect':[],'num_side':[] }........ ]
    treatment_and_evaluations = []
    for treatment in treatments:
        temp = {}
        temp['treatment'] = treatment
        evaluations = treatment.evaluation_set.all()
        temp['num'] = len(evaluations)

        num_effect = [0,0,0,0]
        num_side = [0,0,0,0]

        for e in evaluations:
            if e.positive_score <=25:
                num_effect[0] += 1
            elif e.positive_score <= 50:
                num_effect[1] += 1
            elif e.positive_score <= 75:
                num_effect[2] += 1
            else:
                num_effect[3] += 1

            if e.negative_score <= 25:
                num_side[0] += 1
            elif e.negative_score <= 50:
                num_side[1] += 1
            elif e.negative_score <= 75:
                num_side[2] += 1
            else:
                num_side[3] += 1

        temp['num_side'] = num_side
        temp['num_effect'] = num_effect
        treatment_and_evaluations.append(temp)

    counts = []
    counts.append(len(disease_and_num))
    counts.append(len(treatment_and_evaluations))


    return  the_symptom,disease_and_num,treatment_and_evaluations,counts






























