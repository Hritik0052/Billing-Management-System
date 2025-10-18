from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Bill, BillItem
from items.models import Item
from accounts.models import User
from django.contrib import messages
import random
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
import json
from .utils import generate_bill_no
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def create_bill(request):
    # Serialize items queryset to list of dicts with necessary fields
    items_qs = Item.objects.all()
    items = list(items_qs.values('id', 'name', 'price'))
    items_json = json.dumps(items, cls=DjangoJSONEncoder)  # JSON string for template
    
    last_bill = Bill.objects.last()
    last_bill_no = last_bill.bill_no if last_bill else 0
    next_bill_no = last_bill_no + 1


    if request.method == 'POST':
        customer_name = request.POST.get('customerName')
        customer_phone = request.POST.get('customerMobile')
        selected_items = request.POST.getlist('item')
        quantities = request.POST.getlist('quantity')


        print("Customer Name: ", customer_name,"customerMobile: ",customer_phone)
        print(quantities, " & ", selected_items)

        bill = Bill.objects.create(
            bill_no=generate_bill_no(),
            customer_name=customer_name,
            customer_phone=customer_phone,
            created_by=request.user
        )

        total = 0
        for i, item_id in enumerate(selected_items):
            item = get_object_or_404(Item, id=item_id)
            qty = int(quantities[i])
            subtotal = item.price * qty
            BillItem.objects.create(
                bill=bill,
                item=item,
                quantity=qty,
                price=item.price,
                subtotal=subtotal
            )
            total += subtotal

        bill.total = total
        bill.save()
        return redirect('view_bill', bill_no=next_bill_no)

    # Pass JSON string to template under 'items_json' key
    return render(request, 'admin/generate_bill.html', {'items_json': items_json, 'next_bill_no': next_bill_no})


# 🟢 Add Item
@login_required
def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')

        if name and price:
            Item.objects.create(
                name=name,
                price=price,
                description=description
            )
            messages.success(request, f'Item "{name}" added successfully!')
            return redirect('all_items')
        else:
            messages.error(request, 'Name and Price are required.')

    return render(request, 'items/add_item.html')


# 🔵 All Items
@login_required
def all_items(request):
    items = Item.objects.all().order_by('-created_at')
    return render(request, 'items/all_items.html', {'items': items})


# 🟡 Edit Item
@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')

        item.name = name
        item.price = price
        item.description = description
        item.save()

        messages.success(request, f'Item "{item.name}" updated successfully!')
        return redirect('all_items')

    return render(request, 'items/edit_item.html', {'item': item})


# 🔴 Delete Item
@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item_name = item.name
    item.delete()
    messages.warning(request, f'Item "{item_name}" has been deleted.')
    return redirect('all_items')






# 🟢 Add Employee
@login_required
def add_employee(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = 'employee'

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            User.objects.create(
                username=username,
                email=email,
                password=make_password(password),  # hash password
                role=role
            )
            messages.success(request, f'Employee "{username}" added successfully!')
            return redirect('all_employees')

    return render(request, 'admin/add_employee.html')


# 🔵 All Employees
@login_required
def all_employees(request):
    employees = User.objects.filter(role='employee').order_by('username')
    return render(request, 'admin/all_employees.html', {'employees': employees})


# 🟡 Edit Employee
@login_required
def edit_employee(request, user_id):
    employee = get_object_or_404(User, id=user_id, role='employee')

    if request.method == 'POST':
        employee.username = request.POST.get('username')
        employee.email = request.POST.get('email')
        password = request.POST.get('password')

        if password:  # Only update password if provided
            employee.password = make_password(password)

        employee.save()
        messages.success(request, f'Employee "{employee.username}" updated successfully!')
        return redirect('all_employees')

    return render(request, 'admin/edit_employee.html', {'employee': employee})


# 🟣 View Employee
@login_required
def view_employee(request, user_id):
    employee = get_object_or_404(User, id=user_id, role='employee')
    return render(request, 'admin/view_employee.html', {'employee': employee})


# 🔴 Delete Employee
@login_required
def delete_employee(request, user_id):
    employee = get_object_or_404(User, id=user_id, role='employee')
    username = employee.username
    employee.delete()
    messages.warning(request, f'Employee "{username}" has been deleted.')
    return redirect('all_employees')


# 🔴 Delete Employee
def total_bills(request):
    bills = Bill.objects.all()
    return render(request, 'admin/all_bills.html', {'bills': bills})