from .models import Symptom, Treatment, Disease, UserInfo, Evaluation, Positive, Negative, Daily

#by disease's name , get the related symptoms and treatments
def load_data_for_disease_page(disease_id):
    the_disease = Disease.objects.get(id=disease_id)
    symptoms = the_disease.symptom_set.all()
    #treatment for symptom which this disease has
    #treatments_for_symptoms = { 'symptom.symptom_name':{'treatments':[],'obj':symptom},  ...}
    treatments_for_symptoms = {}

    for symptom in symptoms:
        treatments = symptom.treatment_set.all()
        treatments_for_symptoms[symptom.symptom_name] = {}
        treatments_for_symptoms[symptom.symptom_name]['treatments'] = treatments
        treatments_for_symptoms[symptom.symptom_name]['obj'] = symptom

    treatments_for_disease = {}
    patients = the_disease.user_set().all()

    #count the people of each treatment
    #treatments_for_disease[treatment.treatment_name][0] represent the num ,and [1] represent the object
    #treatments_for_disease = { "treatment_name":{'num':23,'obj':treatment} , ... }
    for patient in patients:
        treatments = patient.treatments.all()
        for treatment in treatments:
            if treatment.treatment_name in treatments_for_disease.keys():
                treatments_for_disease[treatment.treatment_name]['num'] += 1

            else:
                treatments_for_disease[treatment.treatment_name] = {}
                treatments_for_disease[treatment.treatment_name]['num'] = 1
                treatments_for_disease[treatment.treatment_name]['obj'] = treatment

    #count the age  diagnosed  evaluations
    #evaluations = {'treatment_name':{'num':20, 'score':42, 'symptom':[...]}, .....}
    evaluations = {}
    ages = [0,0,0,0,0,0]
    diagnosed = 0
    undiagnosed = 0
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

        patient_evalutions = patient.evaluations.all()
        for evaluation in patient_evalutions:
            treatment_name = evaluation.treatment.treatment_name
            if treatment_name in evaluations.keys():
                evaluations[treatment_name]['num'] += 1
                evaluations[treatment_name]['score'] = (evaluations[treatment_name]['score'] + evaluation.score)
                evaluations[treatment_name]['score'] /= evaluations[treatment_name]['num']
                negative_symptoms = evaluation.negative_set.all()
                for negative_symptom in negative_symptoms:
                    if negative_symptom in evaluations[treatment_name]['symptom']:
                        continue

                    else:
                        evaluations[treatment_name]['symptom'].append(negative_symptom)

            else:
                evaluations[treatment_name] = {}
                evaluations[treatment_name]['num'] = 1
                evaluations[treatment_name]['score'] = evaluation.score
                evaluations[treatment_name]['symptom'] = []
                negative_symptoms = evaluation.negative_set.all()
                for negative_symptom in negative_symptoms:
                    if negative_symptom in evaluations[treatment_name]['symptom']:
                        continue

                    else:
                        evaluations[treatment_name]['symptom'].append(negative_symptom)

    return treatments_for_symptoms,treatments_for_disease,evaluations,ages,diagnosed,undiagnosed










