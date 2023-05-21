from django.urls import path
from .views import my_products, edit

app_name= 'products'
urlpatterns = [
    path('',my_products,name='my_products'),
    path('edit/<int:product_id>/',edit,name='edit')
]
