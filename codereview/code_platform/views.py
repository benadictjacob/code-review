from django.shortcuts import render, redirect
from .models import CodeFile
from localgpt_integration.preprocessing import handle_uploaded_file, generate_description
from django.http import JsonResponse
import re
def display(request):
    return render(request, "user.html")

def upload_code(request):
    if request.method == "POST":
        name = request.POST.get("name")
        uploaded_file = request.FILES.get("content")

        if not uploaded_file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        try:
            # Read file as bytes
            content = uploaded_file.read()

            # Decode if it's a text file (UTF-8 assumed)
            try:
                content_str = content.decode('utf-8')  # Converts bytes to str
            except UnicodeDecodeError:
                return JsonResponse({"error": "File format not supported"}, status=400)

            # Save to database
            CodeFile.objects.create(name=name, content=content_str)

            # Handle uploaded file
            file_path = handle_uploaded_file(content, name)

            # Generate description dynamically based on content
            query = f"Analyze the following code and   generate a discription (similar to  read  me file ) + show if there is some error and explain the error in the code +make the veriable more under standable and in the response headings and spaces should be added to make the response more clear  and dont put slash n in the discription :\n\n{content_str}"
            description = generate_description(query)
            cleaned_description = description.replace("\u00a0", " ", )
            
            return JsonResponse({"description": cleaned_description})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "user.html")

def display_code(request):
    code_files = CodeFile.objects.all()
    return render(request, "upload.html", {"code_files": code_files})
