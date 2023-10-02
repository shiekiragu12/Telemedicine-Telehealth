import json

from facilities.models import Substance, SubstanceUseTitle, SubstanceUsage, MentalForm
from doctor.forms import MentalHealthForm
from django.contrib import messages


def get_post_value(post_request, field_name):
    return post_request.get(field_name)


def check_is_empty(value):
    if value == '' or None:
        return None
    return value


def get_substance_usage(post_request):
    substances = Substance.objects.all()
    substance_titles = SubstanceUseTitle.objects.all()

    substance_usages = []
    for substance in substances:
        substance_usage = SubstanceUsage()
        for title in substance_titles:
            field_name = f'substance_{substance.id}_{title.form_name}'
            field_value = get_post_value(post_request, field_name)
            setattr(substance_usage, title.form_name, check_is_empty(field_value))

        substance_usage.substance = substance
        substance_usages.append(substance_usage)
    return substance_usages


def update_existing_substance_usage(old_sub_usage, new_sub_usage):
    substance_titles = SubstanceUseTitle.objects.all()
    for title in substance_titles:
        field_value = getattr(new_sub_usage, title.form_name, '')
        setattr(old_sub_usage, title.form_name, check_is_empty(field_value))
    old_sub_usage.save()


def take_care_of_mental_form(request, appointment_id):
    existing_form = MentalForm.objects.filter(appointment=appointment_id).first()
    selected_slots = request.POST.getlist('selected_slots', None)
    request.POST._mutable = True
    request.POST.update({'appointment': appointment_id})
    request.POST.update({'selected_slots': json.dumps(selected_slots)})
    request.POST._mutable = False
    form = MentalHealthForm(request.POST)
    if existing_form:
        form = MentalHealthForm(request.POST, instance=existing_form)

    if form.is_valid():
        mental_form = form.save()
        substance_usages = get_substance_usage(request.POST)
        for substance_usage in substance_usages:
            substance_usage.mental_form = mental_form
            existing_sub_usage = SubstanceUsage.objects.filter(mental_form=mental_form,
                                                               substance=substance_usage.substance).first()
            if existing_sub_usage:
                update_existing_substance_usage(existing_sub_usage, substance_usage)
            else:
                substance_usage.save()
        messages.success(request, "Mental health confidentiality agreement form saved successfully")
    else:
        messages.error(request, "Something went wrong")