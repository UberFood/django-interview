from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404

from .models import Item, Sale, Wallet

from asgiref.sync import async_to_sync

from shop.consumers import YourConsumer
from channels.layers import get_channel_layer

def index(request):
    sale_list = Sale.objects.all()
    try:
        money = Wallet.objects.get(user = request.user)
    except Wallet.DoesNotExist:
        wallet = Wallet()
        wallet.user = request.user
        wallet.amount = 0
        wallet.save()
        money = wallet
    context = {"sale_list": sale_list, "money": money.amount}
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

        message = {
            "type": "websocket.send",
            "text": item.owner.username + " выставил " + item.name + " на продажу"
        }
        YourConsumer.send_message(message)
    return HttpResponseRedirect("/main")

def buy_item(request, item_id):
    if request.method == "POST":
        User = request.user
        item = Item.objects.get(pk=item_id);
        sale = Sale.objects.get(item = item)
        price = sale.price
        user_wallet = Wallet.objects.get(user = User)
        vendor_wallet = Wallet.objects.get(user = item.owner)

        user_wallet.amount -= price
        user_wallet.save()
        vendor_wallet.amount += price
        vendor_wallet.save()
        sale.delete()
        item.owner = User
        item.save()
    return HttpResponseRedirect("/main")

def add_money(request):
    if request.method == "POST":
        User = request.user
        amount = request.POST.get("amount")
        user_wallet = Wallet.objects.get(user = User)
        user_wallet.amount += int(amount)
        user_wallet.save()
    return HttpResponseRedirect("/main")
