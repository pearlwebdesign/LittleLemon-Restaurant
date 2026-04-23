from django.shortcuts import render   # ✅ correct import

def index(request):
    return render(request, 'index.html')