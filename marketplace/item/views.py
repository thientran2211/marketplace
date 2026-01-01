from django.shortcuts import render, get_object_or_404
from .models import Item

# Create your views here.


def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    related_items = Item.objects.filter(
        category=item.category, is_sold=False).exclude(id=item.id)[:3]

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })
