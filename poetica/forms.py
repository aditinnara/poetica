from django import forms

EMOTION_CHOICES = (
    ('anger', ("anger")),
    ('contempt', ("contempt")),
    ('disgust', ("disgust")),
    ('fear', ("fear")),
    ('disappointment', ("disappointment")),
    ('shame', ("shame")),
    ('regret', ("regret")),
    ('sadness', ("sadness")),
    ('compassion', ("compassion")),
    ('relief', ("relief")),
    ('admiration', ("admiration")),
    ('love', ("love")),
    ('contentment', ("contentment")),
    ('joy', ("joy")),
    ('pride', ("pride")),
    ('amusement', ("amusement")),
    ('interest', ("interest"))
)

class DiscoverForm(forms.Form):
    poets = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Audre Lorde, Sylvia Plath, Walt Whitman, Rumi"}))
    emotions = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "joy, nostalgia, euphoria"}))
    keywords = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "breadcrumbs, fawn, carousel"}))


class UploadForm(forms.Form):
    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Who Said It Was Simple"}))
    poem = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control", 'placeholder': "There are so many roots to the tree of anger..."}))
    author = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Audre Lorde"}))
    emotion = forms.ChoiceField(choices=EMOTION_CHOICES, widget=forms.Select(attrs={'class': "form-control"}))

