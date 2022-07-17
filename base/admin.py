from django.contrib import admin

# Register your models here.
from .models import Pessoa, Grupo, Equipe, Líder, Cabo, Voto

admin.site.register(Pessoa)
admin.site.register(Grupo)
admin.site.register(Equipe)
admin.site.register(Líder)
admin.site.register(Cabo)
admin.site.register(Voto)