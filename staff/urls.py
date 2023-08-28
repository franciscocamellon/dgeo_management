from django.urls import path
from . import views

urlpatterns = [
    path('staff/acquirer', views.acquirer_list, name='acquirer_list'),
    path('staff/reviser', views.reviser_list, name='reviser_list'),
    path('staff/validator', views.validator_list, name='validator_list'),
    path('staff/editor', views.editor_list, name='editor_list'),
    path('staff/preparador', views.preparador_list, name='preparador_list'),
    path('staff/activities/<int:user_id>', views.activities_list_by_user, name='activities_list_by_user')
]
