from django.urls import path
from . import views 

urlpatterns = [
    # path('home/',views.home, name='home'),
    # path('index/',views.index, name='index'),
    # path('test/',views.get_csv, name='get_csv'),
    # path('export-csv/',views.export_csv, name='export_csv'),

    path('health-check/',views.health_check, name='health_check'),
    path('method/',views.method, name='method'),
    path('get-csv/',views.get_csv, name='get_csv'),
]
