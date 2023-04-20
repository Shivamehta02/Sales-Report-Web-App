from django.urls import path
from .views import my_profile_view, edit

app_name= 'profiles'
urlpatterns = [
    path('',my_profile_view,name='my'),
    path('edit/',edit,name='edit')
]
