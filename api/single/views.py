from django.http import JsonResponse
from rest_framework.decorators import api_view
from single.tasks import imports, check_link
from celery.result import AsyncResult
from single.models import Link
from datetime import datetime, timedelta, timezone

CHECK_TIMEOUT = 30

# Create your views here.
@api_view(['GET'])
def importing(request):
    '''
    Данная функция предназначена для создания Celery task-а,
    который запускает механизм импорта данных из data.xlsx.

    Возвращает task_id в json-формате.
    '''
    task = imports.delay()
    return JsonResponse({'task': f'the id of task is {task.id}'})


@api_view(['GET'])
def get_status(request, task_id):
    """
    Данная функция необходима для проверки статуса работы Celery task-a.

    Возвращает статус выполнения Celery task-a.

    :param task_id: id Celery task-a
    :type task_id: string
    """
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JsonResponse(result, status=200)


@api_view(['GET'])
def check_single(request):
    """
    Данная функция проверяет URL-адрес на наличие результатов в БД,
    отправленный в качестве параметра в аргументе request.

    Возвращает статус в json-формате:
    status:null - если проверки данного URL-адреса не было;
    status:код-ответ - если проверка была пройдена и занесена в БД;

    """
    if 'url' in request.GET:
        url = request.GET['url']
        try:
            result = Link.objects.get(link=url)
        except Link.DoesNotExist:
            return JsonResponse({'Error': 'the results for this URL do not exist'}, status=400)
        else:
            return JsonResponse({'result': {
                'url': result.link,
                'status': result.status
            }})
    else:
        return JsonResponse({'Error': 'URL parameter is not found!'}, status=400)
    return JsonResponse({'result': 'success!'})


@api_view(['GET'])
def check_url(request):
    """
    Функция, которая запускает Celery tasks для проверки всех URL-адресов,
    находящихся в БД. Если адрес был проверен в течение 30 секунд,
    то он не будет повторно проверяться.

    Возвращает количество URL-адресов, которые необходимо проверить.

    """
    links = Link.objects.all()
    link_counter = 0
    for link in links:
        time = link.time
        if time is None or datetime.now(timezone.utc) - time > timedelta(seconds=CHECK_TIMEOUT):
            check_link.delay(url=link.link)
            link_counter += 1
    return JsonResponse({'result': f'Links to check: {link_counter}'})
