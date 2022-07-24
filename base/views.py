from multiprocessing import context
from django.shortcuts import render, redirect
from django.db.models import Q
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


def editar(request, context, hierarquia_selecionada, novo_superior, pessoa, superior, redirect_url):

    pessoa_enviada = request.POST.get('pessoa')
    cpf_pessoa_enviada = pessoa_enviada[-15:-1]

    try:
        nova_pessoa = Pessoa.objects.get(cpf=cpf_pessoa_enviada)
    except:
        context['erro'] = True
        return render(request, 'base/editar_colaborador.html', context)

    nova_pessoa.hierarquia = pessoa
    nova_pessoa.save()

    setattr(hierarquia_selecionada, pessoa, nova_pessoa)
    setattr(hierarquia_selecionada, superior, novo_superior)
    hierarquia_selecionada.save()

    return redirect(redirect_url)


def atualizar(hierarquia_form, pessoa_form):
    if hierarquia_form.is_valid() and pessoa_form.is_valid():
        hierarquia_form.save()
        pessoa_form.save()
        return redirect('home')


def zipColaborador(colaboradores, superior_nome):
    colaboradores_tupla = []
    for colaborador in colaboradores:
        superior = getattr(colaborador, superior_nome)
        colaborador_tupla = (superior, colaborador)
        colaboradores_tupla.append(colaborador_tupla)
    return colaboradores_tupla


# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    votos = Voto.objects.filter(
        Q(eleitor__nome__icontains=q) |
        Q(cabo__cabo__nome__icontains=q) |
        Q(cabo__líder__líder__nome__icontains=q) |
        Q(cabo__líder__equipe__coordenador__nome__icontains=q) |
        Q(cabo__líder__equipe__grupo__grupo__icontains=q)
    )
    print(votos)

    context = {'votos': votos}
    return render(request, 'base/home.html', context)


# --------------------- GRUPOS ---------------------
def grupos(request):
    grupos = Grupo.objects.all()
    context = {'colaboradores': grupos, 'colaborador_str': 'Grupo', 'colaborador_link': 'editar-grupo'}
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

    equipes_tupla = zipColaborador(equipes, 'grupo')

    context = {'colaboradores': equipes_tupla, 'colaborador_str': 'Equipe',
               'colaborador_link': 'editar-equipe', 'superior_str': 'Grupo', 'superior_link': 'editar-grupo'}
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
    equipe = Equipe.objects.get(id=pk)
    grupos = Grupo.objects.all()

    pessoas = Pessoa.objects.exclude(hierarquia='eleitor')
    pessoas = list(pessoas.values('nome', 'cpf'))

    pessoa_str = 'coordenador'
    superior_str = 'grupo'

    context = {'erro': False, 'título': 'Edite a equipe', 'pessoa_str': pessoa_str,
               'superior_str': superior_str, 'pessoas': pessoas, 'superiores': grupos,
               'pessoa_selecionada': equipe.coordenador, 'hierarquia_selecionada': equipe.grupo}

    if request.method == 'POST':
        superior_enviado = request.POST.get('superior')
        try:
            novo_superior = Grupo.objects.get(grupo=superior_enviado)
        except:
            context['erro'] = True
            return render(request, 'base/editar_colaborador.html', context)

        return editar(
            request, context, equipe, novo_superior, pessoa_str, superior_str,
            redirect_url='equipes')

    return render(request, 'base/editar_colaborador.html', context)


# --------------------- LÍDERES ---------------------
def líderes(request):
    líderes = Líder.objects.all()

    líderes_tupla = zipColaborador(líderes, 'equipe')

    context = {'colaboradores': líderes_tupla, 'colaborador_str': 'Líder',
               'colaborador_link': 'editar-líder', 'superior_str': 'Equipe', 'superior_link': 'editar-equipe'}
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
    equipes = Equipe.objects.all

    pessoas = Pessoa.objects.exclude(hierarquia='eleitor')
    pessoas = list(pessoas.values('nome', 'cpf'))

    pessoa_str = 'líder'
    superior_str = 'coordenador'

    context = {'erro': False, 'título': 'Edite o(a) Líder', 'pessoa_str': pessoa_str,
               'superior_str': superior_str, 'pessoas': pessoas, 'superiores': equipes,
               'pessoa_selecionada': líder.líder, 'hierarquia_selecionada': líder.equipe}

    if request.method == 'POST':
        superior_enviado = request.POST.get('superior')
        try:
            novo_superior = Pessoa.objects.get(nome=superior_enviado)
            novo_superior = Equipe.objects.get(coordenador=novo_superior)
        except:
            print("Coordenador errado!")
            context['erro'] = True
            return render(request, 'base/editar_colaborador.html', context)

        return editar(
            request, context, líder, novo_superior, pessoa_str, superior_str,
            redirect_url='líderes')

    return render(request, 'base/editar_colaborador.html', context)


# --------------------- CABOS ELEITORAIS ---------------------
def cabos(request):
    cabos = Cabo.objects.all()

    cabos_tupla = zipColaborador(cabos, 'líder')

    context = {'colaboradores': cabos_tupla, 'colaborador_str': 'Cabo',
               'colaborador_link': 'editar-cabo', 'superior_str': 'Líder', 'superior_link': 'editar-líder'}
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
    líderes = Líder.objects.all

    pessoas = Pessoa.objects.exclude(hierarquia='eleitor')
    pessoas = list(pessoas.values('nome', 'cpf'))

    pessoa_str = 'cabo'
    superior_str = 'líder'

    context = {'erro': False, 'título': 'Edite o(a) Cabo Eleitoral', 'pessoa_str': pessoa_str,
               'superior_str': superior_str, 'pessoas': pessoas, 'superiores': líderes,
               'pessoa_selecionada': cabo.cabo, 'hierarquia_selecionada': cabo.líder}

    if request.method == 'POST':
        superior_enviado = request.POST.get('superior')
        try:
            novo_superior = Pessoa.objects.get(nome=superior_enviado)
            novo_superior = Líder.objects.get(líder=novo_superior)
        except:
            print("Líder errado!")
            context['erro'] = True
            return render(request, 'base/editar_colaborador.html', context)

        return editar(
            request, context, cabo, novo_superior, pessoa_str, superior_str,
            redirect_url='cabos')

    return render(request, 'base/editar_colaborador.html', context)
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
