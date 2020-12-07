from api.celery import app
from single.models import Link
from openpyxl import load_workbook

@app.task()
def imports():
    try:
        wb = load_workbook('./data.xlsx')
        ws = wb['Data']
    except FileNotFoundError:
        return 'File does not exist'
        # return JsonResponse({'Error': 'File does not exist'}, status=400)
    except KeyError:
        return 'Sheet with name Data was not found!'
        # return JsonResponse({'Error': 'Sheet with name Data was not found!'}, status=400)
    else:
        for cell in ws['A']:
            try:
                link = Link.objects.get(link=cell.value)
            except Link.DoesNotExist:
                new_link = Link(link=cell.value)
                new_link.save()
        # return JsonResponse({'Succecss': 'imported!'})
        return 'links were imported successfully!'