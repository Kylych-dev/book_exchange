from django.utils import timezone
from django.views.generic import View, ListView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Schedule, ScheduleDetail
from .forms import ScheduleForm, ScheduleDetailForm


class ScheduleListView(ListView):
    model = Schedule
    template_name = 'schedule_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context



class ScheduleCreateView(View):

    def get(self, request):
        schedule_form = ScheduleForm()
        detail_forms = [
            ScheduleDetailForm(prefix=str(i)) for i in range(7)
        ]

        return render(request, 'schedule_form.html', {
            'schedule_form': schedule_form,
            'detail_forms': detail_forms,
        })


    def post(self, request):
        schedule_form = ScheduleForm(request.POST)
        detail_forms = [ScheduleDetailForm(request.POST, prefix=str(i)) for i in range(7)]

        if schedule_form.is_valid() and all(form.is_valid() for form in detail_forms):
            schedule = schedule_form.save()

            # Сохраняем детали расписания
            for form in detail_forms:
                detail = form.save(commit=False)
                detail.schedule = schedule
                detail.save()

            return redirect('schedule_detail', pk=schedule.pk)

        # Если есть ошибки, возвращаем их в форму
        return render(request, 'schedule_form.html', {
            'schedule_form': schedule_form,
            'detail_forms': detail_forms,
        })


class ScheduleUpdateView(View):
    def get(self, request, pk):
        schedule = get_object_or_404(Schedule, pk=pk)
        schedule_form = ScheduleForm(instance=schedule)
        detail_forms = [ScheduleDetailForm(instance=detail, prefix=str(i)) for i, detail in enumerate(schedule.details.all())]

        return render(request, 'schedule_form.html', {
            'schedule_form': schedule_form,
            'detail_forms': detail_forms,
        })

    def post(self, request, pk):
        schedule = get_object_or_404(Schedule, pk=pk)
        schedule_form = ScheduleForm(request.POST, instance=schedule)
        detail_forms = [ScheduleDetailForm(request.POST, instance=detail, prefix=str(i)) for i, detail in enumerate(schedule.details.all())]

        if schedule_form.is_valid() and all(form.is_valid() for form in detail_forms):
            schedule_form.save()

            for form in detail_forms:
                form.save()

            return redirect('schedule_detail', pk=schedule.pk)

        return render(request, 'schedule_form.html', {
            'schedule_form': schedule_form,
            'detail_forms': detail_forms,
        })