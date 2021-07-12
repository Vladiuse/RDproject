from django.urls import path
from . import views


app_name = 'employees'
urlpatterns = [
    path('',views.employees, name='all'),
    # path('api/', views.employee_list),
    # path('api/<int:level_id>/', views.employee_level)
    path('api/', views.EmployeeList.as_view(), name='employee_all'),
    path('api/<int:level_id>/', views.EmployeeList.as_view(), name='employee_level')
]


