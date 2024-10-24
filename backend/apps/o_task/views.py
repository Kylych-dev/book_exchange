from django.shortcuts import render

from django.http import JsonResponse
from django.views import View
from .o_task import create_otask_task

import json

class WorkspaceProjectsView(View):
    def get(self, request, *args, **kwargs): pass



class CreateTaskView(View):
    def post(self, request):
        print('/*/*/*/*/*/*/*/*/')
        try:
            task_data = json.loads(request.body)
            print('Received data >>>>>>>>>>>:', task_data)
            # result = create_otask_task(task_data)
            ws_slug = '8af22c9b-2090-40ef-a5b9-dfe30b1dfae6'
            result = create_otask_task(task_data, ws_slug)
            print('Task creation result:', result)

            return JsonResponse(result, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error 1": "Invalid JSON"}, status=400)
        except Exception as e:
            print('/*/*-=-=-=/*/*-=-=/*/*/')
            return JsonResponse({"error": str(e)}, status=400)

