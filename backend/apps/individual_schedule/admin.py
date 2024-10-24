from django.contrib import admin
from .models import (
    WorkStatus,
    ScheduleDetail,
    Schedule,
    EmployeeSchedule,
    Employee
)


class ScheduleDetailInline(admin.TabularInline):
    model = ScheduleDetail
    extra = 1  # Количество пустых форм для добавления новых деталей расписания

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ScheduleDetailInline]  # Подключаем inline для деталей расписания

class EmployeeScheduleAdmin(admin.ModelAdmin):
    list_display = ('employee', 'individual_schedule', 'start_date', 'end_date')
    list_filter = ('employee', 'individual_schedule')

class ScheduleDetailAdmin(admin.ModelAdmin):
    list_display = ('week_day', 'status', 'hours', 'schedule')
    list_filter = ('schedule', 'week_day', 'status')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'personnel_number', 'is_active', 'schedule')
    list_filter = ('is_active', 'schedule')

# Регистрация моделей в админке
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(EmployeeSchedule, EmployeeScheduleAdmin)
admin.site.register(ScheduleDetail, ScheduleDetailAdmin)
admin.site.register(Employee, EmployeeAdmin)












# @admin.register(ScheduleDetail)
# class ScheduleDetailAdmin(admin.TabularInline):
#     """
#    Админка для работы с индивидуальными графиками сотрудников
#     """
#     list_display = (
#         'schedule',
#         'week_day',
#         'status',
#         'hours'
#     )
#     list_filter = ('schedule', 'week_day', 'status')
#
#
# @admin.register(Schedule)
# class ScheduleAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     inlines = [ScheduleDetailInline]
#
#
# # Настройка отображения моделей в админке
# class ScheduleDetailInline(admin.TabularInline):
#     model = ScheduleDetail
#     extra = 1  # Количество пустых форм, которые будут отображаться для добавления новых деталей расписания
#
# class EmployeeScheduleAdmin(admin.ModelAdmin):
#     list_display = ('employee', 'individual_schedule', 'start_date', 'end_date')
#     list_filter = ('employee', 'individual_schedule')
#
# class EmployeeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'personnel_number', 'is_active', 'schedule')
#     list_filter = ('is_active', 'schedule')
#
# # Регистрация моделей в админке
# admin.site.register(Schedule, ScheduleAdmin)
# admin.site.register(EmployeeSchedule, EmployeeScheduleAdmin)
# admin.site.register(ScheduleDetail, ScheduleDetailAdmin)
# admin.site.register(Employee, EmployeeAdmin)