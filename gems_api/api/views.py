import csv
import io

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .serializers import CSVImportSerializer, TopSerializer
from .services import (bulk_create_deals, bulk_items_and_customers,
                       get_top_and_deals)


@api_view(['POST'])
def import_deals(request):
    # проверяем формат полученных данных из POST запроса
    serializer = CSVImportSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    file = serializer.validated_data['csv_file'].read().decode('utf-8')

    # создаем, если необходимо новых costumers и items из csv файла
    reader = csv.DictReader(io.StringIO(file))
    bulk_items_and_customers(reader)

    # валидируем и создаем deal из csv файла
    reader = csv.DictReader(io.StringIO(file))
    bulk_create_deals(reader)

    return Response(status=HTTP_200_OK)


@api_view(['GET'])
def get_top_five(request):
    # Получаем топ 5 покупателей и их сделки с самыми популярынми камнями
    top_customers, deals = get_top_and_deals()

    # Обьеденияем данные из двух запросов в список для сериализатора
    for obj in top_customers:
        obj['gems'] = []
        for deal in deals:
            if deal['customer__username'] == obj['username']:
                obj['gems'].append(deal['item__name'])

    # Отправляем данные в сериализатор
    serializer = TopSerializer(top_customers, many=True)
    return Response({'response': serializer.data})
