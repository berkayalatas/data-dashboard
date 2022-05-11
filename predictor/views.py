from django.shortcuts import render, redirect
from .forms import DataForm
from .models import Data

def index(request):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('predictions')
    else:
        form = DataForm()    
        
    
    context = {
        'form' : form,
    }
    return render(request, 'predictor/index.html', context)

def predictions(request):
    predicted_sports = Data.objects.all()
    context = {
        'predicted_sports': predicted_sports,
    }
    return render(request, 'predictor/predictions.html', context)

