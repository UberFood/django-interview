from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound

from .models import Item

def index(request):
    item_list = Item.objects.all()
    context = {"item_list": item_list}
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
