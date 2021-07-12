from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from .models import Employee
from .serializers import EmployeeSerializer


def employees(request):
    genres = Employee.objects.all()
    content = {'genres': genres}
    return render(request, 'employees/employees.html', content)


class MyGroup(permissions.BasePermission):

    def has_permission(self, request, view):
        group_user = 'MyGroup'
        user = request.user
        return group_user in [group.name for group in user.groups.all()]


class EmployeeList(APIView):
    permission_classes = [permissions.IsAuthenticated, MyGroup]

    def get(self, request, level_id=None, format=None):
        if not level_id:
            queryset = Employee.objects.all()
        else:
            queryset = Employee.objects.filter(level=level_id)
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)




# @csrf_exempt
# @api_view(['GET', ])
# def employee_list(request, format=None):
#     if request.method == 'GET':
#         em = Employee.objects.all()
#         serializer = EmployeeSerializer(em, many=True)
#         return Response(serializer.data)
#
#
# @api_view(['GET', ])
# def employee_level(request, level_id, format=None):
#     if request.method == 'GET':
#         em = Employee.objects.filter(level=level_id)
#         serializer = EmployeeSerializer(em, many=True)
#         return Response(serializer.data)