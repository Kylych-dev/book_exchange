import requests

import requests


def authenticate_otask():
    url = "https://api.otask.ru/api/v1/auth/login"
    payload = {
        "email": "mirbekov.kylych@mail.ru",
        "password": "mirbekov 1993"
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        auth_token = response.json().get("token")
        print(auth_token, '<<<<<<<<<<<<<< Token')
        if auth_token:
            return auth_token
        else:
            raise Exception("Токен доступа не найден в ответе.")
    else:
        raise Exception(f"Ошибка аутентификации: {response.text}")


def create_otask_task(task_data, ws_slug):
    auth_token = authenticate_otask()
    task_url = f'https://api.otask.ru/api/v1/ws/{ws_slug}/tasks/create'

    # task_url = 'https://api.otask.ru/api/v1/ws/{ws_slug}/tasks/create'.format(
    #     ws_slug='da1b32e7-58ac-4aad-acdf-eb85c64ca352')
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    body = {
        "name": "Первая задача",
        "board_column_id": 8,
        "board_id": 11,
        "comment": "quisquam",
        "description": "Et culpa ea voluptatem perspiciatis aut perferendis ad et.",
        "end_at": "2024-06-18T07:00:00.000Z",
        "priority_id": 17,
        "project_id": 15,
        "custom_fields": [
            {
                "id": 1,
                "value": "Example value"
            }
        ],
        "files": [
            {
                "name": "124.pdf",
                "temp_src": "DLuKWdN9nUm8wxoc89bl9qjb7QDNHOhZfQkn4H1V.pdf"
            }
        ],
        "performers": [
            1,
            2,
            3
        ],
        "tags": [
            1,
            2,
            3
        ],
        "subtasks": [
            {
                "id": None,
                "end_at": "2024-06-18T07:00:00.000Z",
                "is_completed": False,
                "name": "Подзадача",
                "performers": [
                    1,
                    2
                ]
            }
        ],
        "reminder_date": "18.06.2024 11:33",
        "recurring": {
            "skip_weekends": True,
            "time": "07:00",
            "timezone": "Europe/Moscow",
            "type": "every-day",
            "value": "10"
        }
    }

    task_response = requests.post(task_url, headers=headers, json=body)

    if task_response.status_code == 201:
        return task_response.json()
    else:
        return {"error": "Ошибка создания задачи: " + task_response.text}




# данные для создания задачи
task_data = {
    "name": "Первая задача",
    "board_column_id": 8,
    "board_id": 11,
    "comment": "Тестовый комментарий",
    "description": "Описание задачи",
    "end_at": "2024-06-18T07:00:00.000Z"
}

# Вызов функции для создания задачи
# result = create_otask_task(task_data)
# print(result)

# def create_otask_task(task_data):
#     url = "https://api.otask.ru/auth/login"
#     payload = {
#         "username": "mirbikov.kylych@mail.ru",
#         "password": "mirbekov 1993"
#     }
#     response = requests.post(url, json=payload)
#     if response.status_code == 200:
#         auth_token = response.json().get("access_token")
#         task_url = 'https://api.otask.ru/api/v1/ws/{ws_slug}/tasks/create'
#         headers = {
#             'Authorization': 'Bearer {token}'.format(token=auth_token),
#         }
#         task_response = requests.post(task_url, headers=headers, json=task_data)
#         if task_response.status_code == 200:
#             return task_response.json()
#         else:
#             return {"error": "Ошибка создания задачи: " + task_response.text}
#     else:
#         return {"error": "Ошибка входа: " + response.text}




'''
https://api.otask.ru/api/v1/ws/{ws_slug}/tasks/create
Требуется аутентификация 
'''