from django.urls import path
from .views import (
    ScheduleCreateView,
    ScheduleUpdateView,
    ScheduleListView
)

urlpatterns = [
    path('schedule/create/', ScheduleCreateView.as_view(), name='schedule_create'),
    path('schedule/<int:pk>/edit/', ScheduleUpdateView.as_view(), name='schedule_edit'),
    path('schedule/list/', ScheduleListView.as_view(), name='schedule_list'),

]
