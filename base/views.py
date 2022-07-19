from multiprocessing import context
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .models import Pessoa, Grupo, Equipe, Líder, Cabo, Voto
from .forms import PessoaForm, GrupoForm, EquipeForm, EquipeFormAll, LíderForm, LíderFormAll, CaboForm, CaboFormAll, VotoForm


# Funções auxiliares


def cadastrar(request, hierarquia_form, hierarquia, superior):
    pessoa_form = PessoaForm(request.POST)
    if pessoa_form.is_valid():
        pessoa = pessoa_form.save()
        pessoa.hierarquia = hierarquia
        pessoa.save()

        if hierarquia_form.is_valid():
            superior_pk = int(request.POST[superior])

            if hierarquia == 'coordenador':
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


def editar(request, context, hierarquia_selecionada, superior, pessoa):

    superior_enviado = request.POST.get(superior)
    pessoa_enviada = request.POST.get(pessoa)
    cpf_pessoa_enviada = pessoa_enviada[-15:-1]

    try:
        superior_alterar = Grupo.objects.get(grupo=superior_enviado)
        pessoa_alterar = Pessoa.objects.get(cpf=cpf_pessoa_enviada)
    except:
        superior_alterar = None
        pessoa_alterar = None

    if superior_alterar != None and pessoa_alterar != None:
        hierarquia_selecionada.grupo = superior_alterar
        hierarquia_selecionada.coordenador = pessoa_alterar
        hierarquia_selecionada.save()
        return redirect('equipes')
    else:
        context['erro'] = True
        return render(request, 'base/editar_colaborador.html', context)


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


# --------------------- GRUPOS ---------------------
def grupos(request):
    grupos = Grupo.objects.all()
    context = {'colaboradores': grupos, 'link': 'editar-grupo'}
    return render(request, 'base/colaboradores.html', context)


def cadastrarGrupo(request):
    hierarquia_form = GrupoForm()
    if request.method == 'POST':
        hierarquia_form = GrupoForm(request.POST)
        if hierarquia_form.is_valid():
            hierarquia_form.save()
            return redirect('home')

    context = {'pessoa_form': hierarquia_form, 'título': 'novo grupo', 'hierarquia': 'grupo'}
    return render(request, 'base/colaborador_form.html', context)


def editarGrupo(request, pk):
    grupo = Grupo.objects.get(id=pk)

    if request.method == 'POST':
        hierarquia_form = GrupoForm(request.POST, instance=grupo)
        hierarquia_form.save()
        return redirect('grupos')

    context = {'pessoa_form': GrupoForm(instance=grupo), 'título': 'Edite o grupo', 'hierarquia': 'grupo'}
    return render(request, 'base/colaborador_form.html', context)


# --------------------- EQUIPES ---------------------
def equipes(request):
    equipes = Equipe.objects.all()
    context = {'colaboradores': equipes, 'link': 'editar-equipe'}
    return render(request, 'base/colaboradores.html', context)


def cadastrarEquipe(request):
    if request.method == 'POST':
        return cadastrar(request, EquipeForm(request.POST), 'coordenador', 'grupo')

    context = {
        'form': EquipeForm(),
        'pessoa_form': PessoaForm(),
        'título': 'Cadastrar nova equipe', 'hierarquia': 'coordenador'}
    return render(request, 'base/colaborador_form.html', context)


def editarEquipe(request, pk):
    equipe_selecionada = Equipe.objects.get(id=pk)
    pessoas = Pessoa.objects.exclude(hierarquia='eleitor')
    grupos = Grupo.objects.all()
    equipes = Equipe.objects.all()
    context = {'erro': False, 'título': 'Edite a equipe', 'subtítulo': 'da equipe',
               'equipe_selecionada': equipe_selecionada, 'grupos': grupos, 'pessoas': pessoas}

    if request.method == 'POST':
        return editar(request, context, equipe_selecionada, 'grupo', 'coordenador')

    return render(request, 'base/editar_colaborador.html', context)


# --------------------- LÍDERES ---------------------
def líderes(request):
    líderes = Líder.objects.all()
    context = {'colaboradores': líderes, 'link': 'editar-líder'}
    return render(request, 'base/colaboradores.html', context)


def cadastrarLíder(request):
    if request.method == 'POST':
        return cadastrar(request, LíderForm(request.POST), 'líder', 'equipe')

    context = {
        'form': LíderForm(),
        'pessoa_form': PessoaForm(),
        'título': 'Cadastrar novo líder', 'hierarquia': 'líder'}
    return render(request, 'base/colaborador_form.html', context)


def editarLíder(request, pk):
    líder = Líder.objects.get(id=pk)

    if request.method == 'POST':
        hierarquia_form = LíderFormAll(request.POST, instance=líder)
        hierarquia_form.save()
        return redirect('líderes')

    context = {'pessoa_form': LíderFormAll(instance=líder), 'título': 'Edite o(a) líder', 'hierarquia': 'líder'}
    return render(request, 'base/colaborador_form.html', context)


# --------------------- CABOS ELEITORAIS ---------------------
def cabos(request):
    cabos = Cabo.objects.all()
    context = {'colaboradores': cabos, 'link': 'editar-cabo'}
    return render(request, 'base/colaboradores.html', context)


def cadastrarCabo(request):
    if request.method == 'POST':
        return cadastrar(request, CaboForm(request.POST), 'cabo', 'líder')

    context = {
        'form': CaboForm(),
        'pessoa_form': PessoaForm(),
        'título': 'Cadastrar novo cabo eleitoral', 'hierarquia': 'cabo eleitoral'}
    return render(request, 'base/colaborador_form.html', context)


def editarCabo(request, pk):
    cabo = Cabo.objects.get(id=pk)

    if request.method == 'POST':
        hierarquia_form = CaboFormAll(request.POST, instance=cabo)
        hierarquia_form.save()
        return redirect('cabo')

    context = {'pessoa_form': CaboFormAll(instance=cabo), 'título': 'Edite o(a) cabo', 'hierarquia': 'cabo'}
    return render(request, 'base/colaborador_form.html', context)

# --------------------- ELEITORES ---------------------


def cadastrarVoto(request):
    if request.method == 'POST':
        return cadastrar(request, VotoForm(request.POST), 'eleitor', 'cabo')

    context = {
        'form': VotoForm(),
        'pessoa_form': PessoaForm(),
        'título': 'Cadastrar novo eleitor', 'hierarquia': 'eleitor'}
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
