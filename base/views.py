from multiprocessing import context
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .models import Pessoa, Grupo, Equipe, Líder, Cabo, Voto
from .forms import PessoaForm, GrupoForm, EquipeForm, LíderForm, CaboForm, VotoForm


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
    if request.method == 'POST':
        hierarquia_form = EquipeForm(request.POST)
        pessoa_form = PessoaForm(request.POST)
        if pessoa_form.is_valid():
            pessoa = pessoa_form.save()

            if hierarquia_form.is_valid():
                grupo_pk = int(request.POST['grupo'])
                grupo = Grupo.objects.get(pk=grupo_pk)
                equipe = Equipe(grupo=grupo, coordenador=pessoa)
                equipe.save()
                return redirect('home')

    hierarquia = 'coordenador'
    pessoa_form = PessoaForm()
    hierarquia_form = EquipeForm()

    context = {'form': hierarquia_form, 'pessoa_form': pessoa_form, 'hierarquia': hierarquia}
    return render(request, 'base/colaborador_form.html', context)


def cadastrarLíder(request):
    if request.method == 'POST':
        hierarquia_form = LíderForm(request.POST)
        pessoa_form = PessoaForm(request.POST)
        if pessoa_form.is_valid():
            pessoa = pessoa_form.save()

            if hierarquia_form.is_valid():
                equipe_pk = int(request.POST['equipe'])
                equipe = Equipe.objects.get(pk=equipe_pk)
                equipe = Líder(equipe=equipe, líder=pessoa)
                equipe.save()
                return redirect('home')

    hierarquia = 'líder'
    pessoa_form = PessoaForm()
    hierarquia_form = LíderForm()

    context = {'form': hierarquia_form, 'pessoa_form': pessoa_form, 'hierarquia': hierarquia}
    return render(request, 'base/colaborador_form.html', context)


def cadastrarCabo(request):
    if request.method == 'POST':
        hierarquia_form = CaboForm(request.POST)
        pessoa_form = PessoaForm(request.POST)
        if pessoa_form.is_valid():
            pessoa = pessoa_form.save()

            if hierarquia_form.is_valid():
                líder_pk = int(request.POST['líder'])
                líder = Líder.objects.get(pk=líder_pk)
                líder = Cabo(líder=líder, cabo=pessoa)
                líder.save()
                return redirect('home')

    hierarquia = 'cabo eleitoral'
    pessoa_form = PessoaForm()
    hierarquia_form = CaboForm()

    context = {'form': hierarquia_form, 'pessoa_form': pessoa_form, 'hierarquia': hierarquia}
    return render(request, 'base/colaborador_form.html', context)


def cadastrarVoto(request):
    if request.method == 'POST':
        hierarquia_form = VotoForm(request.POST)
        pessoa_form = PessoaForm(request.POST)
        if pessoa_form.is_valid():
            pessoa = pessoa_form.save()

            if hierarquia_form.is_valid():
                cabo_pk = int(request.POST['cabo'])
                cabo = Cabo.objects.get(pk=cabo_pk)
                cabo = Voto(cabo=cabo, eleitor=pessoa)
                cabo.save()
                return redirect('home')

    hierarquia = 'Eleitor'
    pessoa_form = PessoaForm()
    hierarquia_form = VotoForm()

    context = {'form': hierarquia_form, 'pessoa_form': pessoa_form, 'hierarquia': hierarquia}
    return render(request, 'base/colaborador_form.html', context)
