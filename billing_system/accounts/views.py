from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from items.models import Item
from bills.models import Bill
from .models import User
from django.db.models import Sum
from datetime import date


def user_login(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Redirect based on role
            if user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('employee_dashboard')
        else:
            message = 'Invalid username or password'
    return render(request, 'accounts/login.html', {'message': message})

@login_required
def admin_dashboard(request):
    # Summary data
    total_bills = Bill.objects.count()
    total_revenue = Bill.objects.aggregate(total=Sum('total'))['total'] or 0
    total_employees = User.objects.filter(role='employee').count()
    todays_bills = Bill.objects.filter(created_at__date=date.today()).count()

    # Recent activity log (if you track it)
    # recent_activities = ActivityLog.objects.order_by('-timestamp')[:5] if ActivityLog.objects.exists() else []

    context = {
        'total_bills': total_bills,
        'total_revenue': total_revenue,
        'total_employees': total_employees,
        'todays_bills': todays_bills,
        # 'recent_activities': recent_activities,
    }

    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def employee_dashboard(request):
    employee_name = request.user.get_full_name() or request.user.username
    total_items = Item.objects.count()
    total_bills = Bill.objects.count()
    print("Debug: ",total_items, total_bills)

    context = {
        "employee_name": employee_name,
        "total_items": total_items,
        "total_bills": total_bills,
    }
    return render(request, 'accounts/employee_dashboard.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')
