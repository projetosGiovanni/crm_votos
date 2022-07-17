from multiprocessing import context
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .models import Pessoa, Grupo, Equipe, Líder, Cabo, Voto
from .forms import PessoaForm, GrupoForm, EquipeForm, LíderForm, CaboForm, VotoForm


# Função auxiliar


def cadastrar(request, hierarquia_form, hierarquia, superior):
    pessoa_form = PessoaForm(request.POST)
    if pessoa_form.is_valid():
        pessoa = pessoa_form.save()

        if hierarquia_form.is_valid():
            superior_pk = int(request.POST[superior])

            if hierarquia == 'equipe':
                grupo = Grupo.objects.get(pk=superior_pk)
                equipe = Equipe(grupo=grupo, coordenador=pessoa)
                equipe.save()
            if hierarquia == 'líder':
                equipe = Equipe.objects.get(pk=superior_pk)
                líder = Líder(equipe=equipe, líder=pessoa)
                líder.save()
            if hierarquia == 'cabo':
                líder = Líder.objects.get(pk=superior_pk)
                cabo = Cabo(líder=líder, cabo=pessoa)
                cabo.save()
            if hierarquia == 'eleitor':
                cabo = Cabo.objects.get(pk=superior_pk)
                voto = Voto(cabo=cabo, eleitor=pessoa)
                voto.save()
            return redirect('home')


def atualizar(hierarquia_form, pessoa_form):
    if hierarquia_form.is_valid() and pessoa_form.is_valid():
        hierarquia_form.save()
        pessoa_form.save()
        return redirect('home')

# Create your views here.


def home(request):
    votos = Voto.objects.all()
    context = {'votos': votos}
    return render(request, 'base/home.html', context)


def cadastrarGrupo(request):
    form = GrupoForm()
    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'pessoa_form': form, 'título': 'novo grupo', 'hierarquia': 'grupo'}
    return render(request, 'base/colaborador_form.html', context)


def cadastrarEquipe(request):
    if request.method == 'POST':
        return cadastrar(request, EquipeForm(request.POST), 'equipe', 'grupo')

    context = {'form': EquipeForm(), 'pessoa_form': PessoaForm(), 'título': 'nova equipe', 'hierarquia': 'coordenador'}
    return render(request, 'base/colaborador_form.html', context)


def cadastrarLíder(request):
    if request.method == 'POST':
        return cadastrar(request, LíderForm(request.POST), 'líder', 'equipe')

    context = {'form': LíderForm(), 'pessoa_form': PessoaForm(), 'título': 'novo líder', 'hierarquia': 'líder'}
    return render(request, 'base/colaborador_form.html', context)


def cadastrarCabo(request):
    if request.method == 'POST':
        return cadastrar(request, CaboForm(request.POST), 'cabo', 'líder')

    context = {
        'form': CaboForm(),
        'pessoa_form': PessoaForm(),
        'título': 'novo cabo eleitoral', 'hierarquia': 'cabo eleitoral'}
    return render(request, 'base/colaborador_form.html', context)


def cadastrarVoto(request):
    if request.method == 'POST':
        return cadastrar(request, VotoForm(request.POST), 'eleitor', 'cabo')

    context = {'form': VotoForm(), 'pessoa_form': PessoaForm(), 'título': 'novo eleitor', 'hierarquia': 'eleitor'}
    return render(request, 'base/colaborador_form.html', context)


def editarVoto(request, pk):
    voto = Voto.objects.get(id=pk)
    pessoa = voto.eleitor

    if request.method == 'POST':
        hierarquia_form = VotoForm(request.POST, instance=voto)
        pessoa_form = PessoaForm(request.POST, instance=pessoa)
        return atualizar(hierarquia_form, pessoa_form)

    context = {'form': VotoForm(instance=voto), 'pessoa_form': PessoaForm(
        instance=pessoa), 'título': 'novo eleitor', 'hierarquia': 'eleitor'}
    return render(request, 'base/colaborador_form.html', context)


def deletarVoto(request, pk):
    voto = Voto.objects.get(id=pk)
    pessoa = voto.eleitor
    if request.method == 'POST':
        voto.delete()
        pessoa.delete()
        return redirect('home')
    context = {'obj': voto}
    return render(request, 'base/delete.html', context)
