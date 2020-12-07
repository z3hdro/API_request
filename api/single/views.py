from django.http import JsonResponse
from rest_framework.decorators import api_view
from single.tasks import imports
# from single.models import Link
# from openpyxl import load_workbook

# Create your views here.
@api_view(['GET'])
def importing(request):
    task = imports.delay()
    return JsonResponse({'task': f'the id of task is {task.id}'})
    # try:
    #     wb = load_workbook('./data.xlsx')
    #     ws = wb['Data']
    # except FileNotFoundError:
    #     return JsonResponse({'Error': 'File does not exist'}, status=400)
    # except KeyError:
    #     return JsonResponse({'Error': 'Sheet with name Data was not found!'}, status=400)
    # else:
    #     for cell in ws['A']:
    #         try:
    #             link = Link.objects.get(link=cell.value)
    #         except Link.DoesNotExist:
    #             new_link = Link(link=cell.value)
    #             new_link.save()
        # return JsonResponse({'Succecss': 'imported!'})

@api_view(['GET'])
def get_status(request, task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JsonResponse(result, status=200)

@api_view(['GET'])
def check_single(request):
    if 'url' in request.GET:
        url = request.GET['url']
        try:
            result = Link.objects.get(link=url)
        except Link.DoesNotExist:
            return JsonResponse({'Error': 'the results for this URL do not exist'}, status=400)
        else:
            return JsonResponse({'result': {
                'url':result.link,
                'status':result.status
            }})
    else:
        return JsonResponse({'Error': 'URL parameter is not found!'}, status=400)
    return JsonResponse({'result':'success!'})
