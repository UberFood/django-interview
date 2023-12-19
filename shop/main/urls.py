from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("add_item/", views.add_item, name="add_item"),
    path("add_item/item_added/", views.item_added, name="item_added"),
]
