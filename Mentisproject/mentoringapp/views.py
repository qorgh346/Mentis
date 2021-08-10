from django.shortcuts import render

# Create your views here.

def mentoring(request):
    return render(request, "mentoring.html")
