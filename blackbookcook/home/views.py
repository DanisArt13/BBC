from django.views import View
from django.shortcuts import render

# Create your views here.

class HomeView(View):
    print('HomeView отработал')
    def get(self, request):
        return render(request, 'home/home.html')