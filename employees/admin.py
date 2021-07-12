import random as r

from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.db.models import F
from .models import Employee


class CategoryListFilter(admin.SimpleListFilter):
    # employee
    title = _('Подпись Фильтра')
    parameter_name = 'LEVEL'

    def lookups(self, request, model_admin):
        return (
            ('0', _('LEVEL 0')),
            ('1', _('LEVEL 1')),
            ('2', _('LEVEL 2')),
            ('3', _('LEVEL 3')),
            ('4', _('LEVEL 4')),
        )

    #
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(level=str(self.value()))


class EmployeeAdmin(admin.ModelAdmin):
    list_display_links = ('parent', 'full_name')
    list_display = ('full_name', 'position', 'salary', 'total_paid', 'parent', 'user')
    change_list_template = "admin/clean_data.html"
    list_filter = ('position', CategoryListFilter)

    def get_urls(self):
        urls = super(EmployeeAdmin, self).get_urls()
        custom_urls = [url('^clean/$', self.clean_data, name='clean_data'), ]

        return custom_urls + urls

    def clean_data(self, request):
        Employee.objects.update(total_paid=F('total_paid')+10)
        # Employee.objects.update(total_paid=0)
        # for employee in Employee.objects.all():
        #     employee.total_paid = r.randint(1, 100)
        #     employee.save()
        self.message_user(request, 'Данные о зп отчищены')
        return HttpResponseRedirect('../')


admin.site.register(Employee, EmployeeAdmin)
