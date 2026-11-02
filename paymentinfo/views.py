from django.shortcuts import render

# Create your views here.

def paymentinfo(request):
    return render(request, 'paymentinfo/paymentinfo.html')