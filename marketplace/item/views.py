from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import NewItemForm, EditItemForm
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


@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:item_detail', item_id=item.id)
    else:
        form = NewItemForm()
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })


@login_required
def edit(request, item_id):
    item = get_object_or_404(Item, id=item_id, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:item_detail', item_id=item.id)
    else:
        form = EditItemForm(instance=item)
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })


@login_required
def delete(request, item_id):
    item = get_object_or_404(Item, id=item_id, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')
