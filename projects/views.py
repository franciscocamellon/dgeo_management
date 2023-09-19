from django.shortcuts import render

# Create your views here.
from utils.constants import SQL_COUNT_TO_FINISHED_ACTIVITIES, SQL_TO_COUNT_ACTIVITY_TYPE, \
    SQL_TO_COUNT_ACTIVITY_TYPE_BY_SITUATION
from utils.database_utils import sql_count_execute, calculate_percentage_difference, project_donut_chart, sql_execute, \
    fase_donut_chart


def index(request):
    context = {}
    projects_query_set = sql_count_execute('SELECT COUNT(projeto.id) FROM macrocontrole.projeto')
    tasks_query_set = sql_count_execute('SELECT COUNT(atividade.id) FROM macrocontrole.atividade')
    staffs_query_set = sql_count_execute('SELECT COUNT(usuario.id) FROM dgeo.usuario')
    finished_tasks_query_set = sql_count_execute(SQL_COUNT_TO_FINISHED_ACTIVITIES)
    production_percentage = calculate_percentage_difference(tasks_query_set, finished_tasks_query_set)
    donut_chart = project_donut_chart(1)
    donut_chart_label, donut_chart_data = project_donut_chart(1, True)
    acquisition_stats = fase_donut_chart()

    context['projects_query_set'] = projects_query_set
    context['tasks_query_set'] = tasks_query_set
    context['staffs_query_set'] = staffs_query_set
    context['production_percentage'] = production_percentage
    context['finished_tasks_query_set'] = finished_tasks_query_set
    context['donut_chart_label'] = donut_chart_label
    context['donut_chart_data'] = donut_chart_data
    context['statistics'] = donut_chart
    print(acquisition_stats)
    return render(request, 'index.html', context)


def acquisition_activities(request):
    context = dict()

    query = SQL_TO_COUNT_ACTIVITY_TYPE.format(4)
    print('query: ', query)

    acquisition_stats = sql_execute(SQL_TO_COUNT_ACTIVITY_TYPE_BY_SITUATION.format(4))

    context['query'] = acquisition_stats

    return render(request, 'index.html', context)
