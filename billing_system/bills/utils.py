from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from .models import Bill
from django.shortcuts import render, redirect
from reportlab.lib import colors
import csv
from django.http import HttpResponse


# Making CSV reports 
def download_csv_report(request):
    # --- Fetch all bills ---
    if request.user.role == 'admin':
        bills = Bill.objects.all().order_by('-created_at')
    else:
        bills = Bill.objects.filter(created_by=request.user).order_by('-created_at')

    # --- Get filter params ---
    bill_no = request.GET.get('bill_no')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    sort_by = request.GET.get('sort_by')

    # --- Apply Filters ---
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

    # --- Apply Sorting ---
    if sort_by == "amount_asc":
        bills = bills.order_by('total')
    elif sort_by == "amount_desc":
        bills = bills.order_by('-total')
    elif sort_by == "date_asc":
        bills = bills.order_by('created_at')
    elif sort_by == "date_desc":
        bills = bills.order_by('-created_at')

    # --- Create CSV response ---
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_bills_report.csv"'

    writer = csv.writer(response)
    writer.writerow(["Sr No", "Customer Name", "Bill No", "Date", "Amount (₹)"])

    for i, bill in enumerate(bills, start=1):
        writer.writerow([
            i,
            bill.customer_name or "",
            bill.bill_no or "",
            bill.created_at.strftime("%d-%b-%Y"),
            f"{bill.total:.2f}"
        ])

    return response



# Making pdf reports 
def download_pdf_report(request):
    # --- Fetch all bills ---
    if request.user.role == 'admin':
        bills = Bill.objects.all().order_by('-created_at')
    else:
        bills = Bill.objects.filter(created_by=request.user).order_by('-created_at')

    # --- Get filter params --
    bill_no = request.GET.get('bill_no')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    sort_by = request.GET.get('sort_by')

    # --- Apply Filters ---
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

    # --- Apply Sorting ---
    if sort_by == "amount_asc":
        bills = bills.order_by('total')
    elif sort_by == "amount_desc":
        bills = bills.order_by('-total')
    elif sort_by == "date_asc":
        bills = bills.order_by('created_at')
    elif sort_by == "date_desc":
        bills = bills.order_by('-created_at')

    # --- Create PDF ---
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="filtered_bills_report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(A4))
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title = Paragraph("<b>Filtered Bill Report</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Table data
    data = [["Sr No", "Customer Name", "Bill Number", "Date", "Amount (in Rs)"]]
    for i, bill in enumerate(bills, start=1):
        data.append([
            i,
            bill.customer_name or "",
            bill.bill_no or "",
            bill.created_at.strftime("%d-%b-%Y"),
            f"{bill.total:.2f}"
        ])

    # Create table
    table = Table(data, colWidths=[50, 200, 120, 120, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(table)

    doc.build(elements)
    return response

# generate custom Bill no here 
def generate_bill_no():
    last_bill = Bill.objects.order_by('-bill_no').first()
    candidate = 1000
    if last_bill:
        try:
            candidate = int(last_bill.bill_no) + 1
        except (ValueError, TypeError):
            candidate = 1000

    # Keep incrementing until a non-existing bill_no is found
    while Bill.objects.filter(bill_no=candidate).exists():
        candidate += 1
    return candidate
