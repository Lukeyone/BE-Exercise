# myapp/urls.py
from django.urls import path
from .views import table_api, table_page
from django.views.generic import TemplateView
from .views import TableAPI

urlpatterns = [
    path("api/new_table/", TableAPI.as_view()),
    # Main landing page – shows the table in HTML
    path("", table_page, name="home"),

    # React Table for different front end look
    path("react-table/", TemplateView.as_view(
          template_name="react_table.html"), name="react_table"),

    # Explicit route to the same table page – more semantic URL
    path("table/", table_page, name="table_page"),

    # API endpoint that returns the table data as JSON (used by frontend or tests)
    path("api/table/", table_api, name="table_api"),
]
