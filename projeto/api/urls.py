from django.urls import path
from . import views
from . import matching
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('upload/', views.uploadFile, name='uploadFile'),
    path('create_matching_table/', matching.createMatchingTable, name="createMatchingTable"),
    path('populate_matching_fields/', matching.populateMatchingFields, name="populateMatchingFields"),
    path('lista_objetos/<int:id>/', views.userData, name='user_data'),
    path('get_reference_fields/', views.defaultDataTable, name='defaultDataTable'),
    path('process_form/', views.processForm, name='processForm'),
    path('userHistory/', views.userHistory, name='userHistory'),
    path('userHistory/<int:id>/delete/', views.userHistoryDelete, name='userHistoryDelete'),
    path('userHistory/<int:id>/edit/', views.userHistoryEdit, name='userHistoryEdit'),
    path('check_availability/', views.CheckAvailabilityView.as_view(), name='check_availability'),
    path('register/', views.RegisterView.as_view(), name='register'),
    #path('login/', obtain_auth_token, name='login'),
    path('login/', views.login, name='login'),
]