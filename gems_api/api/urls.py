from django.urls import path

from .views import get_top_five, import_deals

urlpatterns = [
    path('import', import_deals),
    path('top', get_top_five)
]
