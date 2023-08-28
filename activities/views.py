from django.shortcuts import render
from sqlalchemy import text

from utils.constants import ACTIVITY_BY_USER_SQL
from utils.database_utils import create_connection


# Create your views here.
def activities_list(request):
    engine = create_connection('sap')

    with engine.connect() as connection:
        activities = connection.execute(text(ACTIVITY_BY_USER_SQL.format(9)))
        context = {'activities_list': activities}

    return render(request, 'activities_list.html', context)


def activities_list_by_user(request, id=None):
    engine = create_connection('sap')

    with engine.connect() as connection:
        activities_by_user = connection.execute(text(ACTIVITY_BY_USER_SQL.format(id)))
        context = {'activities_list': activities_by_user}

    return render(request, 'activities_list_by_user.html', context)
