from django import forms
from .models import Pessoa, Grupo, Equipe, Líder, Cabo, Voto


class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = '__all__'


class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = '__all__'


class EquipeForm(forms.ModelForm):
    class Meta:
        model = Equipe
        fields = ['grupo']


class EquipeFormAll(forms.ModelForm):
    class Meta:
        model = Equipe
        fields = '__all__'


class LíderForm(forms.ModelForm):
    class Meta:
        model = Líder
        fields = ['equipe']


class LíderFormAll(forms.ModelForm):
    class Meta:
        model = Líder
        fields = '__all__'


class CaboForm(forms.ModelForm):
    class Meta:
        model = Cabo
        fields = ['líder']


class CaboFormAll(forms.ModelForm):
    class Meta:
        model = Cabo
        fields = '__all__'


class VotoForm(forms.ModelForm):
    class Meta:
        model = Voto
        fields = ['cabo']
        labels = {
            'cabo': 'Cabo eleitoral'
        }
