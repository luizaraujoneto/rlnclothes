from django.conf import settings


def debug(request):
    """
    Adiciona a variável `DEBUG` ao contexto do template.
    """
    return {"DEBUG": settings.DEBUG}
