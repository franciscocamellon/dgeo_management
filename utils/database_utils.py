import datetime
import pytz
from sqlalchemy import create_engine, text

from dgeo_management.settings import TIME_ZONE
from utils.constants import DGEO_DATABASE_URL, MONTHLY_ACTIVITY_BY_USER, YEARS, SQL_TO_CHART_DATA, ACTIVITIES, \
    CURRENT_MONTHLY_ACTIVITY_BY_USER, SQL_TO_CHART_AVERAGE_DATA, WEEKLY_CHART_AVERAGE_DATA, SQL_TO_WEEKLY_CHART_DATA, \
    SQL_TO_DONUT_CHART_DATA, MANAGEMENT_DATABASE_NAME, SQL_TO_COUNT_ACTIVITY_TYPE, SQL_TO_COUNT_ACQUISITION, \
    SQL_TO_COUNT_VALIDATION, SQL_TO_COUNT_EDITION, SQL_TO_COUNT_DISSEMINATION


def get_current_month():
    project_timezone = pytz.timezone(TIME_ZONE)
    current_datetime = datetime.datetime.now(project_timezone)
    return current_datetime.month


def create_connection(db_name):
    engine = create_engine(r'{}{}'.format(DGEO_DATABASE_URL, db_name), echo=True, pool_recycle=3600, pool_pre_ping=True)
    return engine


def sql_count_execute(sql_string):
    engine = create_connection(MANAGEMENT_DATABASE_NAME)

    with engine.connect() as connection:
        result = connection.execute(text(sql_string)).fetchone()[0]

    return result


def sql_execute(sql_string):
    engine = create_connection(MANAGEMENT_DATABASE_NAME)

    with engine.connect() as connection:
        result = connection.execute(text(sql_string))

    return result


def monthly_activities_by_user(user_id, last_month, current_month):
    # TODO: do a refactoring in order to simplify the logic and maintain the readability

    last_month_query_set = sql_execute(MONTHLY_ACTIVITY_BY_USER.format(user_id, (get_current_month() - 1)))
    current_month_query_set = sql_execute(CURRENT_MONTHLY_ACTIVITY_BY_USER.format(user_id, get_current_month()))
    last_month_activity_dict = [dict(zip(last_month_query_set.keys(), row)) for row in last_month_query_set]
    current_month_activity_dict = [dict(zip(current_month_query_set.keys(), row)) for row in current_month_query_set]

    merged_activity_dict = {}

    for column in last_month_query_set.keys():
        last_month_value = last_month_activity_dict[0][column]  # Assuming only one row in each query set
        current_month_value = current_month_activity_dict[0][column]

        if last_month_value == 0:
            difference_percentage = 100.0 if current_month_value > 0 else 0.0
        else:
            difference_percentage = ((current_month_value - last_month_value) / last_month_value) * 100

        merged_activity_dict[column] = {'count': current_month_value, 'percent': round(difference_percentage, 2)}

    return prepare_activity_data(merged_activity_dict)


def monthly_chart_by_user(user_id, average=False):
    # TODO: do a refactoring in order to simplify the logic and maintain the readability

    chart_dict = {}

    sql_query = SQL_TO_CHART_AVERAGE_DATA.format(4) if average else SQL_TO_CHART_DATA.format(user_id, 4)
    user_query_set = sql_count_execute('SELECT COUNT(usuario.id) FROM dgeo.usuario')
    query_set = sql_execute(sql_query)

    for row in query_set:
        chart_dict.update(dict(zip(query_set.keys(), row)))

    if average:
        for month, total_data in chart_dict.items():
            chart_dict[month] = round(total_data / user_query_set)

    return prepare_chart_data(chart_dict)


def weekly_chart_by_user(user_id, average=False):
    # TODO: do a refactoring in order to simplify the logic and maintain the readability

    chart_dict = {}

    sql_query = WEEKLY_CHART_AVERAGE_DATA.format(4) if average else SQL_TO_WEEKLY_CHART_DATA.format(user_id, 4)
    user_query_set = sql_count_execute('SELECT COUNT(usuario.id) FROM dgeo.usuario')
    query_set = sql_execute(sql_query)

    for row in query_set:
        chart_dict.update(dict(zip(query_set.keys(), row)))

    if average:
        for month, total_data in chart_dict.items():
            chart_dict[month] = round(total_data / user_query_set)

    return prepare_chart_data(chart_dict)


def project_donut_chart(project_id, prepare=False):
    chart_dict = {}
    query_set = sql_execute(SQL_TO_DONUT_CHART_DATA.format(project_id))

    for row in query_set:
        chart_dict.update(dict(zip(query_set.keys(), row)))

    if prepare:
        return prepare_chart_data(chart_dict)

    return prepare_donut_chart_data(chart_dict)


def fase_donut_chart():
    chart_dict = {('Aquisição', 'acquisition'): prepare_data_to_chart(SQL_TO_COUNT_ACQUISITION),
                  ('Validação', 'validation'): prepare_data_to_chart(SQL_TO_COUNT_VALIDATION),
                  ('Edição', 'edition'): prepare_data_to_chart(SQL_TO_COUNT_EDITION),
                  ('Disseminação', 'dissemination'): prepare_data_to_chart(SQL_TO_COUNT_DISSEMINATION)}

    return chart_dict


def prepare_data_to_chart(sql):
    chart_dict = {}
    query_set = sql_execute(sql)

    for row in query_set:
        chart_dict.update(dict(zip(query_set.keys(), row)))

    return chart_dict


def calculate_percentage_difference(first_number, last_number):
    if last_number == 0:
        return round(0, 2)
    return round(((first_number - last_number) / last_number) * 100, 2)


def transform_query_result(sql_string):
    query_result = sql_execute(sql_string)
    staff_result = {'Aquisitor': [], 'Revisor': [], 'Validador': [], 'Editor': [], 'Preparador': []}

    for row in query_result:

        if row.perfil == 'Aquisitor':
            staff_result[row.perfil].append(row)
        elif row.perfil == 'Revisor':
            staff_result[row.perfil].append(row)
        elif row.perfil == 'Validador':
            staff_result[row.perfil].append(row)
        elif row.perfil == 'Editor':
            staff_result[row.perfil].append(row)
        elif row.perfil == 'Preparador':
            staff_result[row.perfil].append(row)
        else:
            pass
    return staff_result


def prepare_chart_data(chart_dict):
    chart_label = []
    chart_data = []

    for label, data in chart_dict.items():
        chart_label.append(label.title())
        chart_data.append(data)

    return chart_label, chart_data


def prepare_donut_chart_data(donut_chart_dict):
    donut_chart = {}

    tasks_query_set = sql_count_execute('SELECT COUNT(atividade.id) FROM macrocontrole.atividade')

    for label, data in donut_chart_dict.items():
        donut_chart[label.title()] = round((data / tasks_query_set * 100), 1)

    return donut_chart


def prepare_activity_data(activity_dict):
    activity_context = {}

    for activity, data in activity_dict.items():
        data.update({'render': ACTIVITIES[activity][1]})
        activity_context[ACTIVITIES[activity][0]] = data

    return activity_context
