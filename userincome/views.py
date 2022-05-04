import pdb
from django.shortcuts import render, redirect
from .models import Source, UserIncome
from django.core.paginator import Paginator
from userpreferences.models import UserPreferences
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
import datetime

def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText') #convert json to python dictionary
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'income': income,
        'page_obj': page_obj,
    }
    if UserPreferences.objects.filter(user=request.user).exists():
        currency = UserPreferences.objects.get(user=request.user).currency
    else:
        currency = 'Please add a currency'

    context['currency'] = currency

    return render(request, 'income/index.html', context)


@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'income/add-income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add-income.html', context)
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/add-income.html', context)

        UserIncome.objects.create(owner=request.user, amount=amount, date=date,
                                  source=source, description=description)
        messages.success(request, 'Record saved successfully')

        return redirect('income')


@login_required(login_url='/authentication/login')
def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'income/edit-income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit-income.html', context)
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/edit-income.html', context)
        income.amount = amount
        income. date = date
        income.source = source
        income.description = description

        income.save()
        messages.success(request, 'Record updated  successfully')

        return redirect('income')


def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'record removed')
    return redirect('income')


   
def income_source_summary(request):
    earnings = UserIncome.objects.filter(owner = request.user) #gte stands for 'greater than or equal', lte stands for 'lower than or equal' 
    final = {}
    
    def get_source_names(source):
        return source
    
    #set removes the dupliced categories
    source_list =list(set(map(get_source_names, earnings)))
 
    
    def get_earning_amount(source):
        amount = 0
        filtered_by_source = earnings.filter(source=source)
        
        #update amount
        for item in filtered_by_source:
            amount += item.amount
        return amount
        

    for x in earnings:
        for y in source_list: #key-- value
            final[str(y)] = get_earning_amount(y)
            
    #pdb.set_trace()
    return JsonResponse({'income_source_data' : final} , safe= False)    
   
""" JsonResponse’s first parameter, data, should be a dict instance. To pass any other 
    JSON-serializable object you must set the safe parameter to False.

    JSON is a format that encodes objects in a string. Serialization means to convert an object into that string, 
    and deserialization is its inverse operation (convert string -> object).
"""


def income_stats_view(request):
    return render(request, 'income/stats.html')