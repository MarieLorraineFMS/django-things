from django.http import HttpRequest, HttpResponse

# En ajoutant 'HttpRequest' on dit à Pylance :
# "Le paramètre request est un objet de type requête HTTP de Django"
def index(request: HttpRequest) -> HttpResponse:
    """
    Vue pour l'index de l'application.
    """
    return HttpResponse("Bonjour l'ami")