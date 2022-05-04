import pdb
from .models import Category, Expense
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from userpreferences.models import UserPreferences
import json
from django.http import JsonResponse, HttpResponse
import datetime
import csv
import xlwt

@login_required(login_url='/authentication/login')
def index(request):
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'expenses': expenses,
        'page_obj': page_obj,            
    }
    if UserPreferences.objects.filter(user = request.user).exists():
        currency = UserPreferences.objects.get(user=request.user).currency
    else:
        currency = 'Please add a currency'
        
    context['currency'] = currency       
        
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'expenses/add-expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add-expense.html', context)
        quantity = request.POST['quantity']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', context)
        if not quantity:
            messages.error(request, 'Quantity is required')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(owner=request.user, amount=amount, quantity=quantity, date=date,
                               category=category, description=description)
        messages.success(request, 'Expense saved successfully')

        return redirect('expenses')


@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)

        quantity = request.POST['quantity']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit-expense.html', context)

        if not quantity:
            messages.error(request, 'Quantity is required')
            return render(request, 'expenses/add_expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense.quantity = quantity
        expense. date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, 'Expense updated successfully')

        return redirect('expenses')


def expense_delete(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense deleted successfully')
    return redirect('expenses')

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText') # convert to python obj and get search input value
        
        expenses = Expense.objects.filter(
                amount__startswith = search_str, owner = request.user) or Expense.objects.filter(
                quantity__startswith = search_str, owner = request.user) or  Expense.objects.filter(
                date__startswith = search_str, owner = request.user) or Expense.objects.filter(
                description__icontains = search_str, owner = request.user) or Expense.objects.filter(
                category__icontains = search_str, owner = request.user) # i = case sensitivity

        data = expenses.values()
        
        return JsonResponse(list(data), safe=False) #send http response inside a list
    
    
def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30 * 6)    
    expenses = Expense.objects.filter( owner = request.user,
        date__gte = six_months_ago, date__lte = todays_date) #gte stands for 'greater than or equal', lte stands for 'lower than or equal' 
    final = {}
    
    def get_categories(expense):
        return expense.category
    
    #set removes the dupliced categories
    category_list =list(set(map(get_categories, expenses)))
    
    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)
        
        #update amount
        for item in filtered_by_category:
            amount += item.amount
        return amount
        

    for x in expenses:
        for y in category_list: #key-- value
            final[y] = get_expense_category_amount(y)
            
    return JsonResponse({'expense_category_data' : final} , safe= False)       
 
""" JsonResponse’s first parameter, data, should be a dict instance. To pass any other 
    JSON-serializable object you must set the safe parameter to False.

    JSON is a format that encodes objects in a string. Serialization means to convert an object into that string, 
    and deserialization is its inverse operation (convert string -> object).
"""

def expense_stats_view(request):
    return render(request, 'expenses/stats.html')


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = Expenses ' + str(datetime.datetime.now()) + '.csv'
    
    writer = csv.writer(response)
    writer.writerow(['Amount', 'Quantity', 'Description', 'Category', 'Date'])
    
    expenses = Expense.objects.filter(owner=request.user)
    
    for expense in expenses:
        writer.writerow([expense.amount, expense.quantity, expense.description, expense.category, expense.date])
        
    return response


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename = Expenses ' + str(datetime.datetime.now()) + '.xls'
    
    work_book = xlwt.Workbook(encoding='utf-8')
    work_sheet = work_book.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    columns = ['Amount', 'Quantity', 'Description', 'Category', 'Date']
    
    for col_num in range(len(columns)):
        work_sheet.write(row_num, col_num, columns[col_num], font_style)
        
    font_style = xlwt.XFStyle()
    
    rows = Expense.objects.filter(owner = request.user).values_list(
        'amount', 'quantity', 'description', 'category', 'date')
    
    for row in rows:
        row_num += 1
        
        for col_num in range(len(row)):
            work_sheet.write(row_num, col_num, str(row[col_num]), font_style)
            
    work_book.save(response)  
    return response          
