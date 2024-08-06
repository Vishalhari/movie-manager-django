from django import forms
from django.forms import FileInput, URLInput, Textarea

from .models import Genre,Movies

class genreforms(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Title'}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Description'}),
        }

class Moviesforms(forms.ModelForm):
    class Meta:
        model = Movies
        fields = '__all__'
        labels = {
            'title': 'Movie Title',
            'genre': 'Genre',
            'description': 'Description',
            'releaseDate': 'Release Date',
            'actors': 'Actors',
            'banner': 'Banner',
            'imdbrating':'IMDB rating',
            'trailerLink': 'Trailer Link',
        }
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Movie Name'}),
            'actors':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Actors'}),
            'genre':forms.Select(attrs={'class': 'form-control'}),
            'users':forms.HiddenInput(attrs={'class': 'form-control'}),
            'imdbrating':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter IMDB rating'}),
            'description':Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter movie description'}),
            'releaseDate':forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'banner':FileInput(attrs={'class': 'form-control'}),
            'trailerLink':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter trailer link'}),
            'approval_status':forms.HiddenInput()
        }

        def __init__(self,*args, **kwargs):
            user_id = kwargs.pop('user_id', None)
            super(Moviesforms, self).__init__(*args, **kwargs)
            self.fields['users'].required = False
            self.fields['approval_status'].required = False


class MovieStatusForm(forms.ModelForm):
    class meta:
        model = Movies
        fields = ['approval_status']


