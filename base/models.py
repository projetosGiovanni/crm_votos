from django.db import models


class Pessoa(models.Model):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    logradouro = models.CharField(max_length=200, null=True, blank=True)
    bairro = models.CharField(max_length=200, null=True, blank=True)
    cidade = models.CharField(max_length=200, null=True, blank=True)
    cep = models.CharField(max_length=10, null=True, blank=True)
    cpf = models.CharField(max_length=14, null=True, blank=True, unique=True)
    nascimento = models.CharField(max_length=10, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Grupo(models.Model):
    grupo = models.CharField(max_length=200)
    rgb = models.CharField(max_length=9, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.grupo


class Equipe(models.Model):
    grupo = models.ForeignKey(Grupo, null=True, on_delete=models.RESTRICT)
    coordenador = models.ForeignKey(Pessoa, null=True, on_delete=models.RESTRICT)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.coordenador.nome


class Líder(models.Model):
    equipe = models.ForeignKey(Equipe, null=True, on_delete=models.RESTRICT)
    líder = models.ForeignKey(Pessoa, null=True, on_delete=models.RESTRICT)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.líder.nome


class Cabo(models.Model):
    líder = models.ForeignKey(Líder, null=True, on_delete=models.RESTRICT)
    cabo = models.ForeignKey(Pessoa, null=True, on_delete=models.RESTRICT)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cabo.nome


class Voto(models.Model):
    cabo = models.ForeignKey(Cabo, null=True, on_delete=models.RESTRICT)
    eleitor = models.ForeignKey(Pessoa, null=True, on_delete=models.RESTRICT)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.eleitor.nome
