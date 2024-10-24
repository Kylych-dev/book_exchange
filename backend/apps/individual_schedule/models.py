from django.db import models
from enumfields import Enum, EnumField

class WeekDays(Enum):
    """
    Дни недели
    """

    MON = 'Monday'
    TUE = 'Tuesday'
    WED = 'Wednesday'
    THU = 'Thursday'
    FRI = 'Friday'
    SAT = 'Saturday'
    SUN = 'Sunday'

    def __str__(self):
        return self.value

class WorkStatus(Enum):
    WORK = 'Working'
    OFF = 'Day Off'
    HOLIDAY = 'Holiday'

    def __str__(self):
        return self.value

class Schedule(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class EmployeeSchedule(models.Model):
    """
    Промежуточная модель для связи сотрудников с графиками
    """
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    individual_schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name='Дата вступления в силу',
                                  help_text='Укажите дату, с которой начинает действовать график работы', )
    end_date = models.DateField(verbose_name='Срок действия графика',
                                help_text='Укажите срок действия графика, если применимо',
                                null=True, blank=True)

    class Meta:
        verbose_name = 'Индивидуальный график сотрудника'
        verbose_name_plural = 'Индивидуальные графики сотрудников'
        constraints = [
            models.UniqueConstraint(fields=['employee', 'individual_schedule'], name='unique_employee_schedule')
        ]

    def __str__(self):
        end_date_str = self.end_date.strftime('%Y-%m-%d') if self.end_date else 'Без срока'
        return f'{self.employee} - {self.individual_schedule.name} (с {self.start_date} по {end_date_str})'


class ScheduleDetail(models.Model):
    schedule = models.ForeignKey(Schedule, related_name='details', on_delete=models.CASCADE)
    week_day = EnumField(WeekDays, max_length=11, verbose_name='день недели')
    status = EnumField(WorkStatus, max_length=20, verbose_name='Статус дня')
    hours = models.IntegerField(verbose_name='Количество рабочих часов', default=8)

    def __str__(self):
        return f"{self.week_day}: {self.status} ({self.hours} hrs)"


class Employee(models.Model):
    """
    Модель, которая содержит информацию о сотруднике. Данная модель используется для дальнейшего формирования договора
    """
    name = models.CharField(max_length=100)
    personnel_number = models.CharField(verbose_name='Табельный номер сотрудника', max_length=5,
                                        null=True, blank=True, unique=True)
    # customer = models.OneToOneField(Customer, on_delete=models.PROTECT, verbose_name='Сотрудник',
    #                                 help_text='Укажите сотрудника')
    # residency = models.ForeignKey(CategoryResident, on_delete=models.PROTECT, verbose_name='Резиденство сотрудника',
    #                               related_name='employees', help_text='Укажите резиденство сотрудника')
    # category = models.ManyToManyField(CategoryEmployee, through='CategoryEmployeeHistory',
    #                                   verbose_name='Категория сотрудника', related_name='employees',
    #                                   help_text='Укажите категорию сотрудника')
    # payroll = models.ForeignKey(Payroll, on_delete=models.PROTECT, verbose_name='Способ начисления заработной платы',
    #                             related_name='employees', help_text='Укажите способ начисления заработной платы')
    schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT, verbose_name='График работы',
                                 related_name='employees', help_text='Укажите график работы сотрудника')
    # positions = models.ManyToManyField(Position, verbose_name='История перемещения сотрудника',
    #                                    through='PositionActionEmployee', related_name='employees', blank=True,
    #                                    help_text='Укажите должность сотрудника')
    # advance_percentage = models.IntegerField(verbose_name='Процент для выдачи аванса',
    #                                          default=get_config_value('standard_advance_percentage'),
    #                                          help_text='Укажите процент для выдачи аванса')
    is_active = models.BooleanField(verbose_name='Активный сотрудник', help_text='Укажите активный ли сотрудник',
                                    default=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.name

