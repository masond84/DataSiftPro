from django.shortcuts import render
from .models import Newsletter
# Create your views here.
def index(request):
    return render(request, 'helper/index.html')    

def newsletter(request):
    print("running")
    success = False
    if request.method == "POST":
        print(request.POST)
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        newsletter = Newsletter(name=name, email=email, message=message)
        newsletter.save()
        print("success")
        success = True
        
    return render(request, 'helper/index.html', {'success': success})