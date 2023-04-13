from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from poetica.models import Profile

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

MAX_UPLOAD_SIZE = 2500000

class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_picture',)
        widgets = {
            'profile_picture': forms.FileInput(attrs={'style': "display: none;", 'onchange': "submit();"})
        }
        labels = {
            'profile_picture': "Profile Picture"
        }

    def clean_picture(self):
        profile_picture = self.cleaned_data['profile_picture']
        if not profile_picture or not hasattr(profile_picture, 'content_type'):
            raise forms.ValidationError('You must upload a picture')
        if not profile_picture.content_type or not profile_picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if profile_picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return profile_picture


class ProfileBioForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio',)
        widgets = {
            'bio': forms.Textarea(attrs={'id':"user_bio_area", 'class': "form-control", 'rows': 5, 'placeholder': "your bio here"}),
        }
        labels = {
            'bio': "",
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': "form-control", 'id': "usernameForm"}))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'class': "form-control", 'id': "passwordForm"}))

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        return cleaned_data


class RegisterForm(forms.Form):
    email      = forms.CharField(max_length=50, widget = forms.EmailInput(attrs={'class': "form-control", 'id': "emailForm"}))
    username   = forms.CharField(max_length=20, widget = forms.TextInput(attrs={'class': "form-control", 'id': "usernameForm"}))
    password  = forms.CharField(max_length=200, label='Password', widget=forms.PasswordInput(attrs={'class': "form-control", 'id': "passwordForm"}))
    confirm_password  = forms.CharField(max_length=200, label='Confirm', widget=forms.PasswordInput(attrs={'class': "form-control", 'id': "passwordConfirmForm"}))

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords did not match.")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        return username


class DiscoverForm(forms.Form):
    poets = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Audre Lorde, Sylvia Plath, Walt Whitman, Rumi"}))
    emotions = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "joy, regret, compassion"}))
    keywords = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "breadcrumbs, fawn, carousel"}))
    def clean(self):
        cleaned_data = super().clean()
        if not any(cleaned_data[x] for x in ['poets', 'emotions', 'keywords']):
            raise forms.ValidationError("You must fill out at least one of the fields.")

        return cleaned_data


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
