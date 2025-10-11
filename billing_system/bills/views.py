from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .models import Bill, BillItem
from items.models import Item
import random
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
import json
from .utils import generate_bill_no


# List all bills (Admin sees all, Employee sees own)
@login_required
def bill_list(request):
    if request.user.role == 'admin':
        bills = Bill.objects.all().order_by('-created_at')
    else:
        bills = Bill.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'bills/bill_list.html', {'bills': bills})

# Create new bill
@login_required
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
    return render(request, 'bills/generate_bill.html', {'items_json': items_json, 'next_bill_no': next_bill_no})


# View bill details (for printing)
@login_required
def view_bill(request, bill_no):
    bill = get_object_or_404(Bill, bill_no=bill_no)
    return render(request, 'bills/view_bill.html', {'bill': bill})


def bill_reports(request):
    if request.user.role == 'admin':
        bills = Bill.objects.all().order_by('-created_at')
    else:
        bills = Bill.objects.filter(created_by=request.user).order_by('-created_at')

    bill_no = request.GET.get('bill_no')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    sort_by = request.GET.get('sort_by')

    # --- Filters ---
    if bill_no:
        bills = bills.filter(bill_no__icontains=bill_no)

    if min_amount:
        bills = bills.filter(total__gte=min_amount)

    if max_amount:
        bills = bills.filter(total__lte=max_amount)

    if from_date:
        bills = bills.filter(created_at__date__gte=from_date)

    if to_date:
        bills = bills.filter(created_at__date__lte=to_date)

    # --- Sorting ---
    if sort_by == "amount_asc":
        bills = bills.order_by('total')
    elif sort_by == "amount_desc":
        bills = bills.order_by('-total')
    elif sort_by == "date_asc":
        bills = bills.order_by('created_at')
    elif sort_by == "date_desc":
        bills = bills.order_by('-created_at')

    return render(request, 'bills/bill_reports.html', {'bills': bills})
