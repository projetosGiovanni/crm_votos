from multiprocessing import context
from django.shortcuts import render, redirect
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
    return render(request, 'base/colaborador_form.html', context)


def cadastrarEquipe(request):
    form = EquipeForm()

    if request.method == 'POST':
        form = EquipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/colaborador_form.html', context)


def cadastrarLíder(request):
    form = LíderForm()

    if request.method == 'POST':
        form = LíderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/colaborador_form.html', context)


def cadastrarCabo(request):
    form = CaboForm()

    if request.method == 'POST':
        form = CaboForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/colaborador_form.html', context)
