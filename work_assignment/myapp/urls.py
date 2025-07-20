# myapp/urls.py
from django.urls import path
from .views import table_api, table_page

urlpatterns = [
    # Main landing page – shows the table in HTML
    path("", table_page, name="home"),

    # Explicit route to the same table page – more semantic URL
    path("table/", table_page, name="table_page"),

    # API endpoint that returns the table data as JSON (used by frontend or tests)
    path("api/table/", table_api, name="table_api"),
]
