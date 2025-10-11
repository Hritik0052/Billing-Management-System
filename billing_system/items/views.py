from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from accounts.decorators import role_required
from django.contrib.auth.decorators import login_required

# List all items (Admin + Employee)
@login_required
def item_list(request):
    items = Item.objects.all()
    return render(request, 'items/item_list.html', {'items': items})

# Add new item (Admin only)
@login_required
@role_required('admin')
def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        stock = request.POST.get('stock') or 0
        Item.objects.create(name=name, price=price, description=description, stock=stock)
        return redirect('item_list')
    return render(request, 'items/add_item.html')

# Edit item (Admin only)
@login_required
@role_required('admin')
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.price = request.POST.get('price')
        item.description = request.POST.get('description')
        item.stock = request.POST.get('stock') or 0
        item.save()
        return redirect('item_list')
    return render(request, 'items/edit_item.html', {'item': item})

# Delete item (Admin only)
@login_required
@role_required('admin')
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect('item_list')
