from django.forms import Form
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.utils import timezone

from poetica.forms import DiscoverForm, UploadForm, EmotionForm
from poetica.forms import LoginForm, RegisterForm, ProfilePicForm, ProfileBioForm
from poetica.models import Profile, Comment, Reply

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from collections import Counter

import random
import pandas as pd
import json
import html

pd.set_option('display.max_colwidth', None)
# Create your views here.

def update_emotion_onerow(poem_id, df):

    row = df.loc[df.index == poem_id]
    index_tmp = df.index[df['Id'] == poem_id]
    index = df.at[index_tmp[0], 'Id']

    d = row.to_dict('records')[0]

    del d['Id']
    del d['First Emotion']
    del d['Second Emotion']
    del d['Third Emotion']

    top_three = sorted(d, key=d.get, reverse=True)[:3]

    df.at[index, 'First Emotion'] = top_three[0]
    df.at[index, 'Second Emotion'] = top_three[1]
    df.at[index, 'Third Emotion'] = top_three[2]

    return df


def add_to_emotion(emotion, poem_id):
    df = pd.read_csv('poetica/static/database/emotions_db.csv')

    if emotion == 'empty':
        return df

    index_tmp = df.index[df['Id'] == poem_id]
    index = df.at[index_tmp[0], 'Id']

    df.at[index, emotion] += 1

    df = update_emotion_onerow(poem_id, df)
    df.to_csv('poetica/static/database/emotions_db.csv', encoding='utf-8', index=False)



def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{"error": "' + message + '"}'
    return HttpResponse(response_json, content_type='application/json', status=status)


def get_emotion(poem_id):
    poem_id = int(poem_id)
    df = pd.read_csv('poetica/static/database/emotions_db.csv')
    row = df.loc[df.index == poem_id]

    index_tmp = df.index[df['Id'] == poem_id]
    index = df.at[index_tmp[0], 'Id']

    return df.at[index, 'First Emotion']

def get_emotion_graph(poem_id):
    poem_id = int(poem_id)
    df = pd.read_csv('poetica/static/database/emotions_db.csv')
    row = df.loc[df.index == poem_id]
    index_tmp = df.index[df['Id'] == poem_id]
    index = df.at[index_tmp[0], 'Id']
    
    graph_dict = {"admirationgraph": df.at[index, 'admiration'],
            "amusementgraph": df.at[index, 'amusement'],
            "angergraph": df.at[index, 'anger'],
            "compassiongraph": df.at[index, 'compassion'],
            "contemptgraph": df.at[index, 'contempt'],
            "contentmentgraph": df.at[index, 'contentment'],
            "disappointmentgraph": df.at[index, 'disappointment'],
            "disgustgraph": df.at[index, 'disgust'],
            "feargraph": df.at[index, 'fear'],
            "interestgraph": df.at[index, 'interest'],
            "joygraph": df.at[index, 'joy'],
            "lovegraph": df.at[index, 'love'],
            "pridegraph": df.at[index, 'pride'],
            "regretgraph": df.at[index, 'regret'],
            "reliefgraph": df.at[index, 'relief'],
            "sadnessgraph": df.at[index, 'sadness'],
            "shamegraph": df.at[index, 'shame'],
            "topvoted": df.at[index, df.at[index, 'First Emotion']]}
    print(graph_dict)

    return graph_dict


def get_rand_quote():
    quote_dict = {
        "Rumi": "I know you're tired but come, this is the way.",
        "Sylvia Plath": "Is there no way out of the mind?",
        "Audre Lorde": "Your silence will not protect you.",
        "Walt Whitman": "Do I contradict myself? Very well, then I contradict myself, I am large, I contain multitudes.",
        "Amanda Gorman": "We lay down our arms.",
        "Christina Rosetti": "Lie still, lie still, my breaking heart...",
        "Emily Dickinson": "That it will never come again is what makes life sweet.",
        "Robert Frost": "And miles to go before I sleep.",
        "John Keats": "Season of mists and mellow fruitfulness...",
        "Emily Brontë": "Be with me always—take any form—drive me mad!",
        "Lewis Carroll": "In vain we roared; in vain we tried.",
        "Mary Oliver": "Listen — are you breathing just a little, and calling it a life?",
        "Morgan Parker": "I am a dreamer with empty hands and I like the chill.",
        "Elizabeth Alexander": "The basket of remembrance has three sides; one is open, can it tilt and spill out?"
    }
    random.seed()
    rand_ind = random.randint(0, len(quote_dict)-1)
    return [list(quote_dict)[rand_ind], list(quote_dict.values())[rand_ind]]


def profile_check(action_function):
    def my_wrapper_function(request, *args, **kwargs):
        try:
            request.user.profile
            return action_function(request, *args, **kwargs)
        except:
            return redirect(reverse('make-profile'))        

    return my_wrapper_function


def make_profile(request):
    new_profile = Profile(user=request.user)
    new_profile.save()

    request.user.username = request.user.social_auth.get(provider='google-oauth2').extra_data['fullname']
    request.user.save()


@login_required
#@profile_check
def home(request):
    return render(request, "mainpage.html")


def login(request):
    context = {}

    quote = get_rand_quote()
    context['quote'] = quote[1]
    context['poet'] = quote[0]

    if request.method == "GET":
        context['form'] = LoginForm()
        return render(request, 'login_page.html', context)

    form = LoginForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'login_page.html', context)

    user = authenticate(username=form.cleaned_data['username'],
                        password=form.cleaned_data['password'])
    
    auth_login(request, user)
    return redirect(reverse('home'))


def logout(request):
    auth_logout(request)
    return redirect(reverse('login'))


def register(request):
    context = {}

    quote = get_rand_quote()
    context['quote'] = quote[1]
    context['poet'] = quote[0]

    if request.method == "GET":
        context['form'] = RegisterForm()
        return render(request, "register_page.html", context)

    form = RegisterForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'register_page.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'])

    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    auth_login(request, new_user)

    new_profile = Profile(user=new_user)
    new_profile.save()

    return redirect(reverse('home'))


@login_required
#@profile_check
def profile(request):
    poem_df = pd.read_csv('poetica/static/database/poetry_db.csv')
    starred_ids = request.user.profile.starred
    starred_dict = (poem_df.loc[poem_df['Id'].isin(starred_ids)]).to_dict(orient='index')
    starred = [val for (index, val) in enumerate(starred_dict.values())]

    for poem in starred:
        poem['Poet'] = poem['Poet'].replace('\\r', '').strip()
        poem['Poem'] = poem['Poem'].replace('\\r', '\n').strip("\\r")
        poem['Title'] = poem['Title'].replace('\\r', '').strip()
        poem['emotion'] = get_emotion(poem['Id']) + "-arrow"
        poem['Id'] = int(poem['Id'])

    if request.method == "GET":
        context = {'starred': starred, 'profile': request.user.profile, 'picform': ProfilePicForm(), 'bioform': ProfileBioForm(initial={'bio': request.user.profile.bio})}
        return render(request, "profile_page.html", context)
    
    bioform = ProfileBioForm(initial={'bio': request.user.profile.bio})
    picform = ProfilePicForm()
    profile = get_object_or_404(Profile, id=request.user.id)

    if 'update-bio' in request.POST:
        bioform = ProfileBioForm(request.POST)
        if not bioform.is_valid():
            context = {'starred': starred, 'profile': request.user.profile, 'picform': picform, 'bioform': bioform}
            return render(request, "profile_page.html", context)
        profile.user = request.user
        profile.bio = bioform.cleaned_data['bio']
        profile.save()

    else:
        picform = ProfilePicForm(request.POST, request.FILES)
        if not picform.is_valid():
            context = {'starred': starred, 'profile': request.user.profile, 'picform': picform, 'bioform': bioform}
            return render(request, "profile_page.html", context)
        profile.user = request.user
        profile.profile_picture = picform.cleaned_data['profile_picture']
        profile.content_type = picform.cleaned_data['profile_picture'].content_type
        profile.save()

    context = {'starred': starred, 'profile': profile, 'picform': ProfilePicForm(),'bioform': ProfileBioForm(instance=request.user.profile)}
    return render(request, "profile_page.html", context)


@login_required
#@profile_check
def other_profile(request, id):
    user = get_object_or_404(User, id=id)

    poem_df = pd.read_csv('poetica/static/database/poetry_db.csv')
    starred_ids = user.profile.starred
    starred_dict = (poem_df.loc[poem_df['Id'].isin(starred_ids)]).to_dict(orient='index')
    starred = [val for (index, val) in enumerate(starred_dict.values())]

    for poem in starred:
        poem['Poet'] = poem['Poet'].replace('\\r', '').strip()
        poem['Poem'] = poem['Poem'].replace('\\r', '\n').strip("\\r")
        poem['Title'] = poem['Title'].replace('\\r', '').strip()
        poem['emotion'] = get_emotion(poem['Id']) + "-arrow"
        poem['Id'] = int(poem['Id'])

    if user == request.user:
        context = {'starred': starred, 'profile': user.profile, 'picform': ProfilePicForm(),'bioform': ProfileBioForm(instance=request.user.profile)}
        return render(request, "profile_page.html", context)

    context = {'starred': starred, 'profile': user.profile}
    return render(request, "other_profile_page.html", context)


@login_required
#@profile_check
def emotion_submit(request, poem_id):
    if request.method == "POST":
        form = EmotionForm(request.POST)
        if form.is_valid():
            emotion = form.cleaned_data['emotion']
            print(emotion)
            add_to_emotion(emotion, poem_id)
        else:
            print("You didn't input an emotion!")

    df = pd.read_csv('poetica/static/database/poetry_db.csv')

    poem = df.loc[df['Id'] == poem_id]
    poem = (poem.to_dict(orient='index'))[poem_id]

    poem = {'Poet': poem['Poet'].replace('\\r', '').strip(),
            'Poem': poem['Poem'].replace('\\r', '\n').strip("\\r"),
            'Title': poem['Title'].replace('\\r', '').strip(),
            'Id': int(poem_id)}

    context = {'poem': poem}
    context['poem_id'] = int(poem_id)

    emotion = get_emotion(poem['Id'])
    context['emotion'] = emotion
    context.update(get_emotion_graph(poem_id))

    context['arrow_color'] = emotion + "-arrow"
    pin_str = "https://www.pinterest.com/pin/create/button/?url=http%3A%2F%2F127.0.0.1%3A8000%2Fpoetica%2Frandom-poem&media=" + emotion + ".jpg&description=Poetica"
    context['pin'] = pin_str
    context['graph_display'] = True

    comments = Comment.objects.all().filter(poem_id=poem_id).order_by('-creation_time')
    comment_list = list()
    for comment in comments:
        comment_list.append({'comment': comment, 'replies': (Reply.objects.all().filter(comment=comment).order_by('creation_time'))})
    context['comments'] = comment_list

    return render(request, "poem_base.html", context)


@login_required
#@profile_check
def starred_poem(request, poem_id):
    poem_df = pd.read_csv('poetica/static/database/poetry_db.csv')
    starred_ids = request.user.profile.starred
    starred_dict = (poem_df.loc[poem_df['Id'].isin(starred_ids)]).to_dict(orient='index')
    poems = {str(index): val for (index, val) in enumerate(starred_dict.values())}

    for poem in poems.values():
        poem['Poet'] = poem['Poet'].replace('\\r', '').strip()
        poem['Poem'] = poem['Poem'].replace('\\r', '\n').strip("\\r")
        poem['Title'] = poem['Title'].replace('\\r', '').strip()

    poem = starred_dict[poem_id]

    key_list = list(poems.keys())
    value_list = list(poems.values())

    request.session['index'] = int(key_list[value_list.index(poem)])
    request.session['poems'] = poems

    context = {'poem': poem}
    emotion = get_emotion(poem_id)
    context['emotion'] = emotion
    context.update(get_emotion_graph(poem_id))
    context['poem_id'] = int(poem_id)

    context['arrow_color'] = emotion + "-arrow"
    pin_str = "https://www.pinterest.com/pin/create/button/?url=http://127.0.0.1:8000/poetica/random-poem&media=" + emotion + ".jpg&description=Poetica"
    context['pin'] = pin_str
    context['graph_display'] = True

    comments = Comment.objects.all().filter(poem_id=poem_id).order_by('-creation_time')
    comment_list = list()
    for comment in comments:
        comment_list.append({'comment': comment, 'replies': (Reply.objects.all().filter(comment=comment).order_by('creation_time'))})
    context['comments'] = comment_list

    return render(request, "poem_base.html", context)


@login_required
#@profile_check
def discover_quiz(request):
    if request.method == "GET":
        context = {'form': DiscoverForm()}
        return render(request, "discover_quiz.html", context)

    form = DiscoverForm(request.POST)
    if not form.is_valid():
        context = {'form': form}
        return render(request, "discover_quiz.html", context)

    poem_df = pd.read_csv('poetica/static/database/poetry_db.csv')
    poem_df = poem_df.dropna()

    emotions_df = pd.read_csv('poetica/static/database/emotions_db.csv')
    emotions_df = emotions_df.dropna()

    poets = (form.cleaned_data['poets']).split(', ')
    emotions = (form.cleaned_data['emotions']).split(', ')
    keywords = [x.lower() for x in ((form.cleaned_data['keywords']).split(', '))]

    poet_dict = (poem_df.loc[poem_df['Poet'].str.lower().isin(x.lower() for x in poets)]).to_dict(orient='index')
    emotions_dict = (emotions_df.loc[emotions_df['First Emotion'].str.lower().isin(emotions)]).to_dict(orient='index')
    keywords_dict = (poem_df.loc[poem_df['Poem'].str.lower().str.contains('|'.join(keywords))]).to_dict(orient='index')

    random_poet = ""
    random_emotions = ""
    random_keywords = ""

    if poet_dict:
        random_poet = [poet_dict[key]['Id'] for key in random.sample(poet_dict.keys(), min(len(poet_dict), 5))]
    if emotions_dict:
        random_emotions = [emotions_dict[key]['Id'] for key in random.sample(emotions_dict.keys(), min(len(emotions_dict), 5))]
    if keywords_dict:
        random_keywords = [keywords_dict[key]['Id'] for key in random.sample(keywords_dict.keys(), min(len(keywords_dict), 5))]

    if keywords == ['']:
        random_keywords = []

    poem_ids = list(set(random_poet).union(set(random_emotions), set(random_keywords)))

    poem_dict = (poem_df.loc[poem_df['Id'].isin(poem_ids)]).to_dict(orient='index')
    poems = {str(index): val for (index, val) in enumerate(poem_dict.values())}

    for poem in poems.values():
        poem['Poet'] = poem['Poet'].replace('\\r', '').strip()
        poem['Poem'] = poem['Poem'].replace('\\r', '\n').strip("\\r")
        poem['Title'] = poem['Title'].replace('\\r', '').strip()

    if poems:
        poem = poems['0']
    else:
        # case where theres no poems to show
        form.add_error(None, "No poems matched your criteria! If you would like to see a poem with your input, try uploading one or changing your criteria.")
        context = {'form': form}
        return render(request, "discover_quiz.html", context)

    request.session['index'] = 0
    request.session['poems'] = poems

    context = {'poem': poem}
    emotion = get_emotion(poem['Id'])

    poem_id = int(poem['Id'])
    context['emotion'] = emotion
    context['poem_id'] = int(poem['Id'])

    context['arrow_color'] = emotion + "-arrow"
    pin_str = "https://www.pinterest.com/pin/create/button/?url=http://127.0.0.1:8000/poetica/random-poem&media=" + emotion + ".jpg&description=Poetica"
    context['pin'] = pin_str

    context['form'] = EmotionForm()

    comments = Comment.objects.all().filter(poem_id=poem_id).order_by('-creation_time')
    comment_list = list()
    for comment in comments:
        comment_list.append({'comment': comment, 'replies': (Reply.objects.all().filter(comment=comment).order_by('creation_time'))})
    context['comments'] = comment_list

    return render(request, "discover_poem_page.html", context)


@login_required
#@profile_check
def discover_poem(request):
    context = {}
    if request.method == "GET":
        context['form'] = EmotionForm()
        return render(request, "discover_poem_page.html", context)
    return render(request, "discover_poem_page.html")


@login_required
#@profile_check
def random_poem(request):
    df = pd.read_csv('poetica/static/database/poetry_db.csv')

    random_ids = []
    for i in range(0, 5):
        random_ids.append(random.randint(0, len(df.index) - 1))
    random_poems = (df.loc[df['Id'].isin(random_ids)]).to_dict(orient='index')
    poems = {str(index): val for (index, val) in enumerate(random_poems.values())}

    for poem in poems.values():
        poem['Poet'] = poem['Poet'].replace('\\r', '').strip()
        poem['Poem'] = poem['Poem'].replace('\\r', '\n').strip("\\r")
        poem['Title'] = poem['Title'].replace('\\r', '').strip()

    poem = poems['0']

    request.session['index'] = 0
    request.session['poems'] = poems

    context = {'poem': poem}

    poem_id = int(poem['Id'])
    emotion = get_emotion(poem['Id'])
    context['poem_id'] = poem_id


    context['emotion'] = emotion
    context['arrow_color'] = emotion + "-arrow"
    pin_str = "https://www.pinterest.com/pin/create/button/?url=http%3A%2F%2F127.0.0.1%3A8000%2Fpoetica%2Frandom-poem&media=" + emotion + ".jpg&description=Poetica"
    context['pin'] = pin_str

    comments = Comment.objects.all().filter(poem_id=poem_id).order_by('-creation_time')
    comment_list = list()
    for comment in comments:
        comment_list.append({'comment': comment, 'replies': (Reply.objects.all().filter(comment=comment).order_by('creation_time'))})
    context['comments'] = comment_list

    if request.method == "GET":
        context['form'] = EmotionForm()
        return render(request, "random_poem_page.html", context)


    return render(request, "random_poem_page.html", context)


@login_required
#@profile_check
def top_liked_poem(request):
    df = pd.read_csv('poetica/static/database/poetry_db.csv')

    starred_ids = list()
    profiles = Profile.objects.all()
    for profile in profiles:
        starred_ids = starred_ids + profile.starred
    print(starred_ids)
    c = Counter(starred_ids)

    top_liked = []
    for tup in c.most_common(10):
        top_liked.append(int(tup[0]))

    random_poems = (df.loc[df['Id'].isin(top_liked)]).to_dict(orient='index')
    poems = {str(index): val for (index, val) in enumerate(random_poems.values())}

    for poem in poems.values():
        poem['Poet'] = poem['Poet'].replace('\\r', '').strip()
        poem['Poem'] = poem['Poem'].replace('\\r', '\n').strip("\\r")
        poem['Title'] = poem['Title'].replace('\\r', '').strip()

    poem = poems['0']

    request.session['index'] = 0
    request.session['poems'] = poems

    context = {'poem': poem}

    poem_id = int(poem['Id'])
    emotion = get_emotion(poem['Id'])
    context['poem_id'] = poem_id

    context['emotion'] = emotion
    context['arrow_color'] = emotion + "-arrow"
    pin_str = "https://www.pinterest.com/pin/create/button/?url=http%3A%2F%2F127.0.0.1%3A8000%2Fpoetica%2Frandom-poem&media=" + emotion + ".jpg&description=Poetica"
    context['pin'] = pin_str

    comments = Comment.objects.all().filter(poem_id=poem_id).order_by('-creation_time')
    comment_list = list()
    for comment in comments:
        comment_list.append({'comment': comment, 'replies': (Reply.objects.all().filter(comment=comment).order_by('creation_time'))})
    context['comments'] = comment_list

    if request.method == "GET":
        context['form'] = EmotionForm()
        return render(request, "top_liked_poem_page.html", context)

    return render(request, "top_liked_poem_page.html")


@login_required
#@profile_check
def upload_poem(request):
    if request.method == "GET":
        context = {'form': UploadForm()}
        return render(request, "upload_poem_page.html", context)

    form = UploadForm(request.POST)
    if not form.is_valid():
        context = {'form': form}
        return render(request, "upload_poem_page.html", context)

    poem_df = pd.read_csv('poetica/static/database/poetry_db.csv')
    emotions_df = pd.read_csv('poetica/static/database/emotions_db.csv')

    # TODO: check for preexisting poem

    title = (form.cleaned_data['title'])
    poem = (form.cleaned_data['poem'])
    author = (form.cleaned_data['author'])
    emotion = (form.cleaned_data['emotion'])

    match_title = [x.lower() for x in poem_df['Title']]
    match_author = [x.lower() for x in poem_df['Poet']]

    if (title.lower() in match_title) and (author.lower() in match_author):
        form.add_error(None, "This poem is already in our database! Try uploading another.")
        context = {'form': form}
        return render(request, "upload_poem_page.html", context)

    id_df = poem_df['Id'].idxmax() + 1

    new_row_poem_df = pd.DataFrame({
        'Title': title,
        'Poem': poem,
        'Poet': author,
        'Id': id_df
    }, index=[id_df])
    new_row_poem_df.to_csv('poetica/static/database/poetry_db.csv', mode='a', index=False, header=False)

    new_row_emotions_df = pd.DataFrame({
        'Id': id_df,
        'First Emotion': emotion,
        'Second Emotion': 'anger',
        'Third Emotion': 'contempt',
        'anger': 0,
        'contempt': 0,
        'disgust': 0,
        'fear': 0,
        'disappointment': 0,
        'shame': 0,
        'regret': 0,
        'sadness': 0,
        'compassion': 0,
        'relief': 0,
        'admiration': 0,
        'love': 0,
        'contentment': 0,
        'joy': 0,
        'pride': 0,
        'amusement': 0,
        'interest': 0
    }, index=[id_df])
    new_row_emotions_df[emotion] = 1
    new_row_emotions_df.to_csv('poetica/static/database/emotions_db.csv', mode='a', index=False, header=False)

    context = {'form': UploadForm()}
    return render(request, "upload_poem_page.html", context)


@login_required
#@profile_check
def left_arrow(request):
    index = request.session['index']
    poems = request.session['poems']

    if index == 0:
        index = len(poems) - 1
    else:
        index = index - 1

    request.session['index'] = index
    poem = poems[str(index)]
    context = {'poem': poem}

    poem_id = int(poem['Id'])
    emotion = get_emotion(poem['Id'])
    context['poem_id'] = poem_id

    context['emotion'] = emotion
    context['arrow_color'] = emotion + "-arrow"
    pin_str = "https://www.pinterest.com/pin/create/button/?url=http%3A%2F%2F127.0.0.1%3A8000%2Fpoetica%2Frandom-poem&media=" + emotion + ".jpg&description=Poetica"
    context['pin'] = pin_str

    comments = Comment.objects.all().filter(poem_id=poem_id).order_by('-creation_time')
    comment_list = list()
    for comment in comments:
        comment_list.append({'comment': comment, 'replies': (Reply.objects.all().filter(comment=comment).order_by('creation_time'))})
    context['comments'] = comment_list

    if request.method == "GET":
        context['form'] = EmotionForm()
        return render(request, "poem_base.html", context)

    return render(request, "poem_base.html", context)


@login_required
#@profile_check
def right_arrow(request):
    index = request.session['index']
    poems = request.session['poems']

    if index == len(poems) - 1:
        index = 0
    else:
        index = index + 1

    request.session['index'] = index
    poem = poems[str(index)]

    context = {'poem': poem}

    emotion = get_emotion(poem['Id'])
    poem_id = int(poem['Id'])
    context['emotion'] = emotion
    context['poem_id'] = poem_id

    context['arrow_color'] = emotion + "-arrow"
    pin_str = "https://www.pinterest.com/pin/create/button/?url=http%3A%2F%2F127.0.0.1%3A8000%2Fpoetica%2Frandom-poem&media=" + emotion + ".jpg&description=Poetica"
    context['pin'] = pin_str
    context['form'] = EmotionForm()

    comments = Comment.objects.all().filter(poem_id=poem_id).order_by('-creation_time')
    comment_list = list()
    for comment in comments:
        comment_list.append({'comment': comment, 'replies': (Reply.objects.all().filter(comment=comment).order_by('creation_time'))})
    context['comments'] = comment_list

    if request.method == "GET":
        context['form'] = EmotionForm()
        return render(request, "poem_base.html", context)


    return render(request, "poem_base.html", context)


@login_required
#@profile_check
def get_photo(request, id):
    info = get_object_or_404(Profile, id=id)
    print('Photo #{} fetched from database: {} (type={})'.format(id, info.profile_picture, type(info.profile_picture)))

    return HttpResponse(info.profile_picture, content_type=info.content_type)

@login_required
#@profile_check
def star(request, id):
    index = request.session['index']
    poems = request.session['poems']
    poem = poems[str(index)]

    context = {'poem': poem}

    emotion = get_emotion(poem['Id'])
    poem_id = int(poem['Id'])
    context['emotion'] = emotion
    context['poem_id'] = poem_id

    context['arrow_color'] = emotion + "-arrow"

    pin_str = "https://www.pinterest.com/pin/create/button/?url=http%3A%2F%2F127.0.0.1%3A8000%2Fpoetica%2Frandom-poem&media=" + emotion + ".jpg&description=Poetica"
    context['pin'] = pin_str
    context['form'] = EmotionForm()

    comments = Comment.objects.all().filter(poem_id=poem_id).order_by('-creation_time')
    comment_list = list()
    for comment in comments:
        comment_list.append({'comment': comment, 'replies': (Reply.objects.all().filter(comment=comment).order_by('creation_time'))})
    context['comments'] = comment_list

    starred = request.user.profile.starred
    star_set = set(starred)
    star_set.add(id)
    request.user.profile.starred = list(star_set)
    request.user.profile.save()

    return render(request, "poem_base.html", context)


@login_required
#@profile_check
def unstar(request, id):
    index = request.session['index']
    poems = request.session['poems']
    poem = poems[str(index)]

    context = {'poem': poem}

    emotion = get_emotion(poem['Id'])
    poem_id = int(poem['Id'])
    context['emotion'] = emotion
    context['poem_id'] = poem_id

    context['arrow_color'] = emotion + "-arrow"

    pin_str = "https://www.pinterest.com/pin/create/button/?url=http%3A%2F%2F127.0.0.1%3A8000%2Fpoetica%2Frandom-poem&media=" + emotion + ".jpg&description=Poetica"
    context['pin'] = pin_str
    context['form'] = EmotionForm()

    comments = Comment.objects.all().filter(poem_id=poem_id).order_by('-creation_time')
    comment_list = list()
    for comment in comments:
        comment_list.append({'comment': comment, 'replies': (Reply.objects.all().filter(comment=comment).order_by('creation_time'))})
    context['comments'] = comment_list

    starred = request.user.profile.starred
    star_set = set(starred)
    star_set.remove(id)
    request.user.profile.starred = list(star_set)
    request.user.profile.save()

    return render(request, "poem_base.html", context)


@login_required
#@profile_check
def comment(request, poem_id):
    index = request.session['index']
    poems = request.session['poems']
    poem = poems[str(index)]

    context = {'poem': poem}

    emotion = get_emotion(poem['Id'])
    poem_id = int(poem['Id'])
    context['emotion'] = emotion
    context['poem_id'] = poem_id

    context['arrow_color'] = emotion + "-arrow"

    pin_str = "https://www.pinterest.com/pin/create/button/?url=http%3A%2F%2F127.0.0.1%3A8000%2Fpoetica%2Frandom-poem&media=" + emotion + ".jpg&description=Poetica"
    context['pin'] = pin_str
    context['form'] = EmotionForm()

    if 'comment-input' not in request.POST or not request.POST['comment-input']:
        comments = Comment.objects.all().filter(poem_id=poem_id).order_by('-creation_time')
        comment_list = list()
        for comment in comments:
            comment_list.append({'comment': comment, 'replies': (Reply.objects.all().filter(comment=comment).order_by('creation_time'))})
            context['comments'] = comment_list
        return render(request, "poem_base.html", context)
    
    new_comment = Comment(user=request.user, comment_text=request.POST['comment-input'], creation_time=timezone.now(), poem_id=poem_id)
    new_comment.save()

    comments = Comment.objects.all().filter(poem_id=poem_id).order_by('-creation_time')
    comment_list = list()
    for comment in comments:
        comment_list.append({'comment': comment, 'replies': (Reply.objects.all().filter(comment=comment).order_by('creation_time'))})
    context['comments'] = comment_list
    return render(request, "poem_base.html", context)


@login_required
#@profile_check
def reply(request, comment_id):
    index = request.session['index']
    poems = request.session['poems']
    poem = poems[str(index)]

    context = {'poem': poem}

    emotion = get_emotion(poem['Id'])
    poem_id = int(poem['Id'])
    context['emotion'] = emotion
    context['poem_id'] = poem_id

    context['arrow_color'] = emotion + "-arrow"

    pin_str = "https://www.pinterest.com/pin/create/button/?url=http%3A%2F%2F127.0.0.1%3A8000%2Fpoetica%2Frandom-poem&media=" + emotion + ".jpg&description=Poetica"
    context['pin'] = pin_str
    context['form'] = EmotionForm()

    if 'reply-input' not in request.POST or not request.POST['reply-input']:
        comments = Comment.objects.all().filter(poem_id=poem_id).order_by('-creation_time')
        comment_list = list()
        for comment in comments:
            comment_list.append({'comment': comment, 'replies': (Reply.objects.all().filter(comment=comment).order_by('creation_time'))})
            context['comments'] = comment_list
        return render(request, "poem_base.html", context)

    new_reply = Reply(user=request.user, reply_text=request.POST['reply-input'], creation_time=timezone.now(), comment=Comment.objects.get(id=comment_id))
    new_reply.save()

    comments = Comment.objects.all().filter(poem_id=poem_id).order_by('-creation_time')
    comment_list = list()
    for comment in comments:
        comment_list.append({'comment': comment, 'replies': (Reply.objects.all().filter(comment=comment).order_by('creation_time'))})
        context['comments'] = comment_list
    return render(request, "poem_base.html", context)  