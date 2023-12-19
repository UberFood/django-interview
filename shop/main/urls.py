from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("add_item/", views.add_item, name="add_item"),
    path("add_item/item_added/", views.item_added, name="item_added"),
    path("my_items/", views.my_items, name="my_items"),
    path("my_items/sell/<int:item_id>", views.sell_item_form, name="sell_item_form"),
    path("my_items/sell/on_sale/<int:item_id>", views.put_on_sale, name="put_on_sale"),
]
