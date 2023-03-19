from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, "mainpage.html")


def login(request):
    return render(request, "login_page.html")


def register(request):
    return render(request, "register_page.html")


def profile(request):
    return render(request, "profile_page.html")


def discover_quiz(request):
    return render(request, "discover_quiz.html")


def discover_poem(request):
    return render(request, "discover_poem_page.html")


def upload_poem(request):
    return render(request, "upload_poem_page.html")
