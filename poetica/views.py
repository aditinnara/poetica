from django.shortcuts import render
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
    return render(request, "discover_quiz.html")


def discover_poem(request):
    return render(request, "discover_poem_page.html")


def random_poem(request):
    df = pd.read_csv('poetica/static/database/poetry_db.csv')
    row = df.loc[df['Id'] == 55]

    context = {"poet": row['Poet'].to_string(index=False).replace('\\r', '\n'),
               "poem": row['Poem'].to_string(index=False).replace('\\r', '\n'),
               "title": row['Title'].to_string(index=False).replace('\\r', '\n')}

    return render(request, "random_poem_page.html", context)


def top_liked_poem(request):
    return render(request, "top_liked_poem_page.html")


def upload_poem(request):
    return render(request, "upload_poem_page.html")
