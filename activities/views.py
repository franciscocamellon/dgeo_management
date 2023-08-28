from django.shortcuts import render
from sqlalchemy import text

from utils.constants import ACTIVITY_BY_USER_SQL
from utils.database_utils import create_connection


# Create your views here.
def activities_list(request):
    engine = create_connection('sap2')

    with engine.connect() as connection:
        activities = connection.execute(text(ACTIVITY_BY_USER_SQL.format(9)))
        context = {'activities_list': activities}

    return render(request, 'activities_list.html', context)


