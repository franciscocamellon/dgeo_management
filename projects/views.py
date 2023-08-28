from django.shortcuts import render

# Create your views here.

def index(request):
    context = {'activities_list': []}
    return render(request, 'index.html', context)