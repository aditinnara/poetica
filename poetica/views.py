from django.shortcuts import render

# Create your views here.
def profile(request):
    return render(request, "discover_poem_page.html")