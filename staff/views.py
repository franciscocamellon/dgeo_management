from django.shortcuts import render

from utils.constants import STAFF_SQL_BY_PROFILE
from utils.database_utils import sql_execute, monthly_chart_by_user, monthly_activities_by_user


# Create your views here.
def acquirer_list(request):
    result = sql_execute(STAFF_SQL_BY_PROFILE.format('Aquisitor'))
    context = {'acquirer_list': result}
    return render(request, 'acquirer_list.html', context)


def reviser_list(request):
    result = sql_execute(STAFF_SQL_BY_PROFILE.format('Revisor'))
    context = {'reviser_list': result}
    return render(request, 'reviser_list.html', context)


def validator_list(request):
    result = sql_execute(STAFF_SQL_BY_PROFILE.format('Validador'))
    context = {'validator_list': result}
    return render(request, 'validator_list.html', context)


def editor_list(request):
    result = sql_execute(STAFF_SQL_BY_PROFILE.format('Editor'))
    context = {'editor_list': result}
    return render(request, 'editor_list.html', context)


def preparador_list(request):
    result = sql_execute(STAFF_SQL_BY_PROFILE.format('Preparador'))
    context = {'preparador_list': result}
    return render(request, 'preparador_list.html', context)


def activities_list_by_user(request, user_id=None):

    context = {}
    chart_label, chart_data = monthly_chart_by_user(user_id)
    result = monthly_activities_by_user(user_id, 4, 5)

    context['result'] = result
    context['chart_label'] = chart_label
    context['chart_data'] = chart_data

    return render(request, 'user_production_profile.html', context)
