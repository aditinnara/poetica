from django.shortcuts import render

# Create your views here.
def home(request):
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


def random_poem(request):
    return render(request, "random_poem_page.html")


def top_liked_poem(request):
    return render(request, "top_liked_poem_page.html")


def upload_poem(request):
    return render(request, "upload_poem_page.html")
