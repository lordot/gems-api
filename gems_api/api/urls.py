from django.urls import path

from .views import import_deals, get_top_five

urlpatterns = [
    path('import', import_deals),
    path('top', get_top_five)
]
