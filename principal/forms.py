from django.forms import ModelForm
from django import forms
from principal.models import Personal, Ruta, Comentario, ImagenesRuta
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class PersonalForm(forms.ModelForm):
	class Meta:
		model=Personal
		exclude=['usuario','latitud','longitud']

class RutaForm(ModelForm):
	class Meta:
		model=Ruta
		exclude=['usuario','longfinal','latfinal']
        
class ComentarioForm(ModelForm):
    class Meta:
        model= Comentario
        exclude=['evento','usuario']
        
class ImagenesRutaForm(ModelForm):
    class Meta:
        model= ImagenesRuta
        exclude=['evento']



