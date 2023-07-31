from django.db.models import Count, Subquery, Sum, OuterRef
from rest_framework.exceptions import ValidationError

from .models import Customer, Deal, Item
from .serializers import CustomerSerializer, DealSerializer, ItemSerializer


def get_top_and_deals():
    """
    SQL запрос для получения топ клиентов и сделок с топ камнями.
    В результате получаем два списка для сведения данных.
    """
    top_customers = Customer.objects.annotate(
        spent_money=Sum('deals__total')).order_by('-spent_money')[:5]

    top_gems = Item.objects.filter(
        deals__customer__in=top_customers).annotate(
        buyers=Count('deals__customer__username', distinct=True)).filter(
        buyers__gte=2)

    gems_by_customers = Deal.objects.filter(
        customer__in=top_customers,
        item__in=top_gems
    )

    top_customers_data = list(top_customers.values('username', 'spent_money'))
    deals_data = list(gems_by_customers.values(
        'customer__username', 'item__name').distinct())

    return top_customers_data, deals_data


def bulk_items_and_customers(reader):
    """
    Функция парсинга и создания costumers и items из csv файлы
    создание происходит с помощью bulk_create.

    Уже имеющеся costumers и items отсекаются из создания.
    """
    ex_cust = {
        customer.username: customer.id for customer in Customer.objects.all()
    }
    ex_item = {item.name: item.id for item in Item.objects.all()}
    new_cust, new_items = {}, {}

    for idx, row in enumerate(reader):
        try:
            if (row['customer'] not in ex_cust and
                    row['customer'] not in new_cust):
                customer_serializer = CustomerSerializer(
                    data={'username': row['customer']}
                )
                customer_serializer.is_valid(raise_exception=True)
                new_cust[row['customer']] = Customer(username=row['customer'])

            if row['item'] not in ex_item and row['item'] not in new_items:
                item_serializer = ItemSerializer(
                    data={'name': row['item']}
                )
                item_serializer.is_valid(raise_exception=True)
                new_items[row['item']] = Item(name=row['item'])
        except ValidationError as err:
            raise ValidationError(
                f'Ошибка данных в строке {idx} - {err.detail}'
            )
    Item.objects.bulk_create(new_items.values())
    Customer.objects.bulk_create(new_cust.values())


def bulk_create_deals(reader):
    """
    Функция парсинга и валидации и создания deals из csv файлы
    создание происходит с помощью bulk_create.
    """
    customers = {
        customer.username: customer for customer in Customer.objects.all()
    }
    items = {item.name: item for item in Item.objects.all()}
    deals = []
    for idx, row in enumerate(reader):
        try:
            data = {
                'date': row['date'],
                'total': row['total'],
                'quantity': row['quantity'],
                'customer': customers.get(row['customer']),
                'item': items.get(row['item'])
            }
            serializer = DealSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                obj = Deal(**data)
                deals.append(obj)
        except ValidationError as err:
            raise ValidationError(
                f'Ошибка данных в строке {idx} - {err.detail}'
            )
    Deal.objects.bulk_create(deals)
