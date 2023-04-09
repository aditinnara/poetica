from django import forms

EMOTION_CHOICES = (
    ('empty', ("-- select an option --")),
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
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()
        emotion = cleaned_data.get('emotion')

        if emotion == 'empty':
            raise forms.ValidationError("You must input an emotion.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


class EmotionForm(forms.Form):
    emotion = forms.ChoiceField(choices=EMOTION_CHOICES, widget=forms.Select(attrs={'class': "form-control"}))
