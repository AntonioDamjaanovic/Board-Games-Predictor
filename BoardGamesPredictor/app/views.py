from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
def home(request):
    context = {

    }
    return render(request, 'app/home.html', context)

def predict(request):
    context = {

    }
    return render(request, 'app/predict.html', context)