from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Transaction, Category
from .forms import TransactionForm
from datetime import datetime


@login_required
def index(request):
    year = request.GET.get('year', datetime.now().year)

    transactions = Transaction.objects.filter(user=request.user, date__year=year)

    total_income = transactions.filter(category__category_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(category__category_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    monthly_data = []
    for month in range(1, 13):
        month_income = \
        transactions.filter(date__month=month, category__category_type='income').aggregate(Sum('amount'))[
            'amount__sum'] or 0
        month_expense = \
        transactions.filter(date__month=month, category__category_type='expense').aggregate(Sum('amount'))[
            'amount__sum'] or 0
        monthly_data.append({
            'month': month,
            'income': float(month_income),
            'expense': float(month_expense),
        })

    expenses_by_category = transactions.filter(category__category_type='expense').values('category__name').annotate(
        total=Sum('amount'))

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'monthly_data': monthly_data,
        'expenses_by_category': list(expenses_by_category),
        'current_year': int(year),
    }
    return render(request, 'index.html', context)


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).select_related('category')
    return render(request, 'transaction_list.html', {'transactions': transactions})


@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Транзакция добавлена')
            return redirect('transaction_list')
    else:
        form = TransactionForm()
        form.fields['category'].queryset = Category.objects.filter(user=request.user)
    return render(request, 'transaction_form.html', {'form': form})