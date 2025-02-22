from django.shortcuts import render, redirect
from .models import CodeFile

# Create your views here
name=''
content=''

def display(request):
    return render(request, "user.html")

def upload_code(request):
    if request.method == "POST":
        name = request.POST.get("name")
        content = request.FILES.get("content").read().decode('utf-8')
        CodeFile.objects.create(name=name, content=content)
        code_files = CodeFile.objects.all()
        return redirect('display')
    return render(request, "user.html")

def display_code(request):
    code_files = CodeFile.objects.all()
    return render(request, "upload.html", {"code_files": code_files})