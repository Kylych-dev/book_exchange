from django.urls import path
from .views import (
    CreateTaskView,
    WorkspaceProjectsView
)

print('/*/*/*/*/')
urlpatterns = [
    path('workspace/projects/', WorkspaceProjectsView.as_view(), name='workspace_projects'),
    path('task/create/', CreateTaskView.as_view(), name='task_create'),
]
