from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _

from app.models import Edificio, Departamento


class EdificioForm(ModelForm):
    class Meta:
        model = Edificio
        fields = ['nombre', 'direccion', 'ciudad', 'tipo']
        labels = {
            'nombre': _('Ingrese nombre del edificio'),
            'direccion': _('Ingrese direccion por favor'),
            'ciudad': _('Ingrese ciudad por favor'),
            'tipo': _('Ingrese tipo por favor'),
        }

class DepartamentoForm(ModelForm):
    class Meta:
        model = Departamento
        fields = ['nombres','apellidos', 'costo', 'num_cuartos', 'edificio']

    def clean_nombre(self):
        valor = self.cleaned_data['nombres']
        num_palabras = len(valor.split())

        if num_palabras < 2:
            raise forms.ValidationError("Ingrese dos nombres por favor")
        return valor

    def clean_direccion(self):
        valor = self.cleaned_data['apellidos']
        num_palabras = len(valor.split())

        if num_palabras < 2:
            raise forms.ValidationError("Ingrese dos apellidos por favor")
        return valor

class DepartamentoEdificioForm(ModelForm):

    def __init__(self, edificio, *args, **kwargs):
        super(DepartamentoEdificioForm, self).__init__(*args, **kwargs)
        self.initial['edificio'] = edificio
        self.fields["edificio"].widget = forms.widgets.HiddenInput()
        print(edificio)

    class Meta:
        model = Departamento
        fields = ['nombres','apellidos', 'costo', 'num_cuartos', 'edificio']