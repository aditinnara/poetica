from django import forms

class DiscoverForm(forms.Form):
    poets = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Audre Lorde, Sylvia Plath, Walt Whitman, Rumi"}))
    emotions = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "joy, nostalgia, euphoria"}))
    keywords = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "breadcrumbs, fawn, carousel"}))
