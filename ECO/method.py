from .models import Symptom, Treatment, Disease, UserInfo, Evaluation, Daily

#by disease's name , get the related symptoms and treatments
def load_data_for_disease_page(disease_id):
    the_disease = Disease.objects.get(id=disease_id)
    disease_info = the_disease.disease_infor
    disease_name = the_disease.disease_name
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
    #evaluations = [  {'treatment':treatment ,'num':20, 'score':42, 'symptom':[...]}, .....]
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
                evaluations[index]['score'] = (evaluations[treatment_name]['score'] + evaluation.score)
                evaluations[index]['score'] /= evaluations[treatment_name]['num']
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
                temp['score'] = evaluation.score
                temp['symptom'] = []
                negative_symptoms = evaluation.negative_symptoms.all()
                for negative_symptom in negative_symptoms:
                    if negative_symptom in temp['symptom']:
                        continue

                    else:
                        temp['symptom'].append(negative_symptom)
                evaluations.append(temp)

    return disease_name,disease_info,treatments_for_symptoms,treatments_for_disease,evaluations,ages,diagnosed,undiagnosed,num_men,num_women













