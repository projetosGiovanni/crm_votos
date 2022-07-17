from multiprocessing import context
from django.shortcuts import render
from django.views.generic.edit import FormView
from .models import Pessoa, Voto
from .forms import PessoaForm, GrupoForm, EquipeForm, LíderForm, CaboForm, VotoForm


# Create your views here.


def home(request):
    votos = Voto.objects.all()
    context = {'votos': votos}
    return render(request, 'base/home.html', context)


def cadastrarGrupo(request):
    form = GrupoForm()
    context = {'form': form}
    return render(request, 'base/grupo_form.html', context)


def cadastrarColaborador(request):
    pessoa_form = PessoaForm()
    form = EquipeForm()
    context = {'pessoa_form': pessoa_form}

    if request.method == 'POST':
        pessoa_form = PessoaForm(request.POST)

        if pessoa_form.is_valid():
            print("saving...")
            pessoa = pessoa_form.save()

            hierarquia = request.POST['hierarquia']

            if hierarquia == "cabo":
                pass

    return render(request, 'base/colaborador_form.html', context)
