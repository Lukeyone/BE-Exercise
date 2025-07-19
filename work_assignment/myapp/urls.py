from django.urls import path
from .views import table_api, table_page

urlpatterns = [
    path("api/table/", table_api, name="table_api"),  # JSON
    path("table/",      table_page, name="table_page"),  # HTML
]
