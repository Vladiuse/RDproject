from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import models
from mptt.models import TreeForeignKey, MPTTModel


class Employee(MPTTModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    full_name = models.CharField(max_length=99)
    position = models.CharField(max_length=99, verbose_name='Должность')
    employment_date = models.DateField(blank=True)
    salary = models.IntegerField()
    total_paid = models.IntegerField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children', verbose_name='Начальник')

    class MPTTMeta:
        order_insertion_by = ['full_name']

    def __str__(self):
        return self.full_name

    def auto_add(self):
        PASSWORD = '2030'
        employment_date = '2020-01-01'
        DEEP = 4
        POWER = 2
        name = self.get_name()
        user = User.objects.create_user(name, password=make_password(PASSWORD))
        user.is_superuser = False
        user.is_staff = True
        user.save()
        root = Employee.objects.create(full_name=name, user=user, position='BOSS', employment_date=employment_date,
                                       salary=100, total_paid=100)
        for level in range(1, DEEP):
            for parent in Employee.objects.filter(level=level - 1):
                for count in range(POWER):
                    name = self.get_name()
                    user = User.objects.create_user(name, password=make_password(PASSWORD))
                    user.is_superuser = False
                    user.is_staff = True
                    user.save()
                    Employee.objects.create(full_name=name, user=user, parent=parent,
                                            position='employee', employment_date=employment_date,
                                            salary=100, total_paid=100
                                            )
        Employee.objects.rebuild()
        return 'All Good'

    def get_name(self):
        import random as r
        alfabet = 'abcdefghijklmnopqrstuvwxyz'
        s = ''
        while len(s) < 5:
            s += r.choice(alfabet)
        return s

    def delete_all(self):
        for employee in Employee.objects.all():
            user = employee.user
            user.delete()
            employee.delete()
        return 'DELETE ALL'
