from multiprocessing import context
from django.shortcuts import render
from django.views.generic.edit import FormView
from .models import Pessoa, Voto
from .forms import PessoaForm, GrupoForm, EquipeForm, LíderForm, CaboForm, VotoForm


def salvarNoBanco(request):
    if request.method == 'POST':
        pessoa_form = PessoaForm(request.POST)
        pessoa = None

        if pessoa_form.is_valid():
            print("saving...")
            pessoa = pessoa_form.save()
            print(pessoa.pk)

        form = EquipeForm(request.POST)
        if form.is_valid():
            form.save()

# Create your views here.


def home(request):
    votos = Voto.objects.all()
    context = {'votos': votos}
    return render(request, 'base/home.html', context)


def cadastrarGrupo(request):
    form = GrupoForm()
    context = {'form': form}
    return render(request, 'base/colaborador_form.html', context)


def cadastrarEquipe(request):
    hierarquia = "nova Equipe"
    pessoa_form = PessoaForm()
    form = EquipeForm()
    context = {'pessoa_form': pessoa_form, 'form': form, 'hierarquia': hierarquia}

    salvarNoBanco(request)
    return render(request, 'base/colaborador_form.html', context)
