# myapp/urls.py
from django.urls import path
from .views import table_api, table_page

urlpatterns = [
    path("",          table_page, name="home"), 
    path("table/",    table_page, name="table_page"),
    path("api/table/", table_api,  name="table_api"),
]
