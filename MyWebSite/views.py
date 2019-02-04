from django.shortcuts import render

def get_index(request):
    context = {}
    return render(request,'index.html',context)