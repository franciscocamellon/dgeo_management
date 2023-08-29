import datetime
from datetime import timezone

import pytz
from sqlalchemy import create_engine, text

from dgeo_management.settings import TIME_ZONE
from utils.constants import DGEO_DATABASE_URL, MONTHLY_ACTIVITY_BY_USER, YEARS, SQL_TO_CHART_DATA, ACTIVITIES, \
    CURRENT_MONTHLY_ACTIVITY_BY_USER


def get_current_month():
    project_timezone = pytz.timezone(TIME_ZONE)
    current_datetime = datetime.datetime.now(project_timezone)
    return current_datetime.month


def create_connection(db_name):
    engine = create_engine(r'{}{}'.format(DGEO_DATABASE_URL, db_name), echo=True)
    return engine


def sql_count_execute(sql_string):
    engine = create_connection('sap')

    with engine.connect() as connection:
        result = connection.execute(text(sql_string)).fetchone()[0]

    return result


def sql_execute(sql_string):
    engine = create_connection('sap')

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


def monthly_chart_by_user(user_id):
    query_set = sql_execute(SQL_TO_CHART_DATA.format(user_id, 4))
    chart_dict = {}

    for row in query_set:
        chart_dict.update(dict(zip(query_set.keys(), row)))

    return prepare_chart_data(chart_dict)


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


def prepare_activity_data(activity_dict):
    activity_context = {}

    for activity, data in activity_dict.items():
        data.update({'render': ACTIVITIES[activity][1]})
        activity_context[ACTIVITIES[activity][0]] = data

    return activity_context
