import csv
import io

from django.db.models import Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Deal
from .serializers import CSVImportSerializer, DealSerializer, TopSerializer


@api_view(['POST'])
def import_deals(request):
    serializer = CSVImportSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        try:
            file = serializer.validated_data['csv_file'].read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(file))
            batch = []
            for index, row in enumerate(reader):
                obj = DealSerializer(data=row)
                obj.is_valid(raise_exception=True)
                batch.append(Deal(**row))
            Deal.objects.bulk_create(batch)
            return Response('Status: OK - файл был обработан без ошибок', status=201)
        except Exception as er:
            return Response(
                f'Status: Error, Desc: {er} - в процессе обработки файла произошла ошибка.',
                status=400
            )


@api_view(['GET'])
def get_top_five(request):
    top = Deal.objects.values('customer').annotate(spent_money=Sum('total')).order_by('-spent_money')[:5]
    serializer = TopSerializer(top, many=True)
    return Response(serializer.data)

