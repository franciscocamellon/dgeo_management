from django.urls import path
from . import views

urlpatterns = [
    path('acquirer', views.acquirer_list, name='acquirer_list'),
    path('reviser', views.reviser_list, name='reviser_list'),
    path('validator', views.validator_list, name='validator_list'),
    path('editor', views.editor_list, name='editor_list'),
    path('preparador', views.preparador_list, name='preparador_list'),
    path('activities/<int:user_id>', views.activities_list_by_user, name='activities_list_by_user')
]
