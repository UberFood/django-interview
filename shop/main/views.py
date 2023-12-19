from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound

from .models import Item, Sale

def index(request):
    sale_list = Sale.objects.all()
    context = {"sale_list": sale_list}
    return render(request, "main/index.html", context)

def add_item(request):
    context = {}
    return render(request, "main/add_item.html", context)

def item_added(request):
    if request.method == "POST":
        item = Item()
        item.name = request.POST.get("item_name")
        item.description = request.POST.get("description")
        item.owner = request.user
        item.save()
    return HttpResponseRedirect("/main")

def my_items(request):
    User = request.user
    my_item_list = Item.objects.filter(owner = User)
    sales = Sale.objects.filter(item__owner = User)
    mixed_list = []
    for item in my_item_list:
        sale = sales.filter(item=item).first()
        bool = True
        if sale == None:
            bool = False
        price = 0
        if bool:
            price = sale.price
        mixed_list.append((item, bool, price))
    context = {"item_list": my_item_list, "mixed_list": mixed_list}
    return render(request, "main/my_items.html", context)

def sell_item_form(request, item_id):
    item = Item.objects.get(pk=item_id);
    context = {"item": item}
    return render(request, "main/sell_item_form.html", context)

def put_on_sale(request, item_id):
    if request.method == "POST":
        item = Item.objects.get(pk=item_id);
        sale = Sale()
        sale.item = item
        sale.price = request.POST.get("price")
        sale.save()
    return HttpResponseRedirect("/main")
