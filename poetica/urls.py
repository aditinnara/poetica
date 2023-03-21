from django.urls import path
from poetica import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('discover-quiz', views.discover_quiz, name='discover-quiz'),
    path('discover-poem', views.discover_poem, name='discover-poem'),
    path('random-poem', views.random_poem, name='random-poem'),
    path('top-liked-poem', views.top_liked_poem, name='top-liked-poem'),
    path('upload-poem', views.upload_poem, name='upload-poem'),
]
