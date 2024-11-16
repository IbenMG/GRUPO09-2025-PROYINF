from django.shortcuts import render

def admin_index(request):
    return render(request, 'admin.html')
