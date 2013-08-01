from django import forms
from .models import Client, RedirectUri, Scope


class ClientForm(forms.ModelForm):
    
    class Meta:
        fields = ("name", "access_host")
        model = Client


class RedirectUriForm(forms.ModelForm):
    
    class Meta:
        fields = ("client", "url")
        model = RedirectUri


class ScopeForm(forms.ModelForm):
    
    class Meta:
        fields = ("short_name", "full_name", "description")
        model = Scope
