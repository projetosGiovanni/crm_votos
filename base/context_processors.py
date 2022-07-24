from .models import Pessoa


def nav_processor(request):
    quantidade_votos = Pessoa.objects.all().count()
    return {'quantidade_votos': quantidade_votos}
