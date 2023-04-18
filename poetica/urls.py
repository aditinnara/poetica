from django.urls import path
from poetica import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('make-profile', views.make_profile, name='make-profile'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('other-profile/<int:id>', views.other_profile, name='other-profile'),
    path('discover-quiz', views.discover_quiz, name='discover-quiz'),
    path('random-poem/<int:poem_id>', views.emotion_submit, name='emotion-submit'),
    path('starred-poem/<int:poem_id>', views.starred_poem, name='starred-poem'),
    path('discover-poem', views.discover_poem, name='discover-poem'),
    path('random-poem', views.random_poem, name='random-poem'),
    path('top-liked-poem', views.top_liked_poem, name='top-liked-poem'),
    path('upload-poem', views.upload_poem, name='upload-poem'),
    path('left-arrow', views.left_arrow, name='left-arrow'),
    path('right-arrow', views.right_arrow, name='right-arrow'),
    path('photo/<int:id>', views.get_photo, name='photo'),
    path('star/<int:id>', views.star, name='star'),
    path('unstar/<int:id>', views.unstar, name='unstar'),
    path('comment/<int:poem_id>', views.comment, name='comment'),
    path('reply/<int:comment_id>', views.reply, name='reply'),
]
