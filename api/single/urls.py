from django.urls import path
from single.views import check_single, importing, get_status, check_url

urlpatterns = [
    path('', importing, name='import'),
    path('tasks/<str:task_id>', get_status, name='get_status'),
    path('api/site_check', check_single, name='show_special_chat'),
    path('api/check', check_url, name='check_url'),
]
