from django import forms
from .models import (
    Schedule,
    ScheduleDetail,
    WeekDays,
    WorkStatus
)

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['name']


class ScheduleDetailForm(forms.ModelForm):
    class Meta:
        model = ScheduleDetail
        fields = [
            'week_day',
            'status',
            'hours'
        ]

    def __init__(self, *args, **kwargs):
        super(ScheduleDetailForm, self).__init__(*args, **kwargs)

        if not self.initial:
            self.initial['week_day'] = WeekDays.MON
            self.initial['status'] = WorkStatus.WORK
            self.initial['hours'] = 8