import random as r
import time

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django_seed import Seed
from employees.models import Employee
from faker import Faker


def check_time(func):
    def surogate(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(end - start)

    return surogate


EMP_DATE = '2020-01-01'
PASSWORD = '2030'
POSITIONS = ['Owner', 'CEO', 'Manager', 'TeamLead', 'Developer']


def add_root():
    fake = Faker('ru_Ru')
    user = User.objects.create_user(username=fake.simple_profile()['username'], password=make_password(PASSWORD))
    root = Employee(user=user,
                    full_name=fake.name(),
                    position=POSITIONS[0],
                    salary=r.randint(3100, 4000),
                    total_paid=0,
                    employment_date=EMP_DATE)
    root.save()
    print('Root Employee Add')


def add_level(level):
    seeder = Seed.seeder()
    CHILDREN_COUNT = 2
    parents_list = Employee.objects.filter(level=level - 1)
    print(parents_list)
    fake = Faker('ru_Ru')
    for parent in parents_list:
        seeder.add_entity(Employee, CHILDREN_COUNT,
                          {'user': lambda x: User.objects.create_user(username=fake.simple_profile()['username'],
                                                                      password=make_password(PASSWORD)),
                           'full_name': lambda x: fake.name(),
                           'position': POSITIONS[level],
                           'salary': lambda x: r.randint(3100, 4000),
                           'total_paid': 0,
                           'employment_date': EMP_DATE,
                           'parent': parent})
        seeder.execute()
        Seed.instance = None
        Seed.seeders = {}
        Seed.fakers = {}
        seeder = Seed.seeder()
    Employee.objects.rebuild()


@check_time
def run():
    add_root()
    for level in range(1, 4):
        add_level(level)
