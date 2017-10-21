from .models import Symptom, Treatment, Disease, User, Evaluation, Positive, Negative, Daily

#by disease's name , get the related symptoms and treatments
def load_data_for_disease_page(disease_name):
    the_disease = Disease.objects.get(disease_name=disease_name)
    symptoms = the_disease.symptom_set.all()
    treatments_for_symptoms = {}

    for symptom in symptoms:
        treatments = symptom.treatment_set.all()
        treatment_names = [t.treatment_name for t in treatments]
        treatments_for_symptoms[symptom.symptom_name] = treatment_names
        




