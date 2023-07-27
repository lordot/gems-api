import csv
import io

from django.db.models import Sum, OuterRef, Count, Subquery
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .models import Deal
from .serializers import CSVImportSerializer, DealSerializer, TopSerializer


@api_view(['POST'])
def import_deals(request):
    serializer = CSVImportSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    file = serializer.validated_data['csv_file'].read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(file))

    batch = []
    for index, row in enumerate(reader):
        obj = DealSerializer(data=row)
        obj.is_valid(raise_exception=True)
        batch.append(Deal(**row))
    Deal.objects.bulk_create(batch)
    return Response(status=HTTP_200_OK)


@api_view(['GET'])
def get_top_five(request):
    # получаем список топ покупателей и общую сумму трат для каждого
    top_customers = Deal.objects.values('customer').annotate(
        spent_money=Sum('total')).order_by('-spent_money')[:5]

    # получаем список камней, которые купили хотя-бы больше двух топ клиентов
    gems_gte_two = Deal.objects.values('item').filter(
        customer__in=Subquery(top_customers.values('customer'))).annotate(
        buyers=Count('customer', distinct=True)).filter(buyers__gte=2).values('item')

    # обеденяем два списка
    tops_with_gems = []
    for customer in top_customers:
        gems = Deal.objects.values_list('item', flat=True).filter(
            customer=customer['customer'], item__in=gems_gte_two).distinct()
        customer['gems'] = [gem for gem in gems]
        tops_with_gems.append(customer)

    serializer = TopSerializer(tops_with_gems, many=True)
    return Response({'response': serializer.data})

