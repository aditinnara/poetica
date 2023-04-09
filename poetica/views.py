from django.forms import Form
from django.shortcuts import render
from poetica.forms import DiscoverForm, UploadForm, EmotionForm

import random
import pandas as pd
import html

pd.set_option('display.max_colwidth', None)
# Create your views here.


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


def home(request):
    return render(request, "mainpage.html")


def login(request):
    quote = get_rand_quote()
    return render(request, "login_page.html", {"quote": quote[1], "poet": quote[0]})


def register(request):
    quote = get_rand_quote()
    return render(request, "register_page.html", {"quote": quote[1], "poet": quote[0]})


def profile(request):
    return render(request, "profile_page.html")


def discover_quiz(request):
    if request.method == "GET":
        context = {'form': DiscoverForm()}
        return render(request, "discover_quiz.html", context)

    form = DiscoverForm(request.POST)
    if not form.is_valid():
        context = {'form': form}
        return render(request, "discover_quiz.html", context)

    poem_df = pd.read_csv('poetica/static/database/poetry_db.csv')
    emotions_df = pd.read_csv('poetica/static/database/emotions_db.csv')

    poets = (form.cleaned_data['poets']).split(', ')
    emotions = (form.cleaned_data['emotions']).split(', ')
    keywords = (form.cleaned_data['keywords']).split(', ')

    poet_dict = (poem_df.loc[poem_df['Poet'].isin(poets)]).to_dict(orient='index')
    emotions_dict = (emotions_df.loc[emotions_df['First Emotion'].isin(emotions)]).to_dict(orient='index')
    keywords_dict = (poem_df.loc[poem_df['Poem'].str.contains('|'.join(keywords))]).to_dict(orient='index')

    random_poet = [poet_dict[key]['Id'] for key in random.sample(poet_dict.keys(), min(len(poet_dict), 5))]
    random_emotions = [emotions_dict[key]['Id'] for key in random.sample(emotions_dict.keys(), min(len(emotions_dict), 5))]
    random_keywords = [keywords_dict[key]['Id'] for key in random.sample(keywords_dict.keys(), min(len(keywords_dict), 5))]

    poem_ids = list(set(random_poet).union(set(random_emotions), set(random_keywords)))

    poem_dict = (poem_df.loc[poem_df['Id'].isin(poem_ids)]).to_dict(orient='index')
    poems = {str(index): val for (index, val) in enumerate(poem_dict.values())}

    for poem in poems.values():
        poem['Poet'] = poem['Poet'].replace('\\r', '').strip()
        poem['Poem'] = poem['Poem'].replace('\\r', '\n').strip("\\r")
        poem['Title'] = poem['Title'].replace('\\r', '').strip()

    poem = poems['0']

    request.session['index'] = 0
    request.session['poems'] = poems

    context = {'poem': poem}

    return render(request, "discover_poem_page.html", context)


def discover_poem(request):
    if request.method == "GET":
        context = {'form': EmotionForm()}
        return render(request, "discover_poem_page.html", context)
    return render(request, "discover_poem_page.html")


def random_poem(request):
    df = pd.read_csv('poetica/static/database/poetry_db.csv')

    random_ids = []
    for i in range(0,5):
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
    print("this happened")

    if request.method == "GET":
        context = {'form': EmotionForm()}
        return render(request, "random_poem_page.html", context)

    return render(request, "random_poem_page.html", context)


def top_liked_poem(request):
    if request.method == "GET":
        context = {'form': EmotionForm()}
        return render(request, "top_liked_poem_page.html", context)
    return render(request, "top_liked_poem_page.html")


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
    # TODO: change the top three emotions every time emotion is updated

    title = (form.cleaned_data['title'])
    poem = (form.cleaned_data['poem'])
    author = (form.cleaned_data['author'])
    emotion = (form.cleaned_data['emotion'])

    id_df = poem_df['Id'].idxmax() + 1
    print(id_df)

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

    if request.method == "GET":
        context = {'form': EmotionForm()}
        return render(request, "poem_base.html", context)

    return render(request, "poem_base.html", context)


def right_arrow(request):
    index = request.session['index']
    poems = request.session['poems']

    if index == len(poems) - 1:
        index = 0
    else:
        index = index + 1

    request.session['index'] = index
    poem = poems[str(index)]
    print("this is poem", poem)
    context = {'poem': poem}

    if request.method == "GET":
        print("in get")
        context = {'form': EmotionForm()}
        return render(request, "poem_base.html", context)

    print("not in get")

    return render(request, "poem_base.html", context)
