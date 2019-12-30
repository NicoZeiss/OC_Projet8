from django import forms

class SearchForm(forms.Form):
	user_input = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Aliment...', 'class': 'input-xl'}))