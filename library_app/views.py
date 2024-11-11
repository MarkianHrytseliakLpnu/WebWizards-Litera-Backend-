from django.shortcuts import render
# Create your views here.

def canva_view(request):
    return render(request, 'canva_template.html')