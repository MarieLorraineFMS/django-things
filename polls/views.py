"""
Logique des vues.
Chaque fonction reçoit une requête et prépare une réponse.
"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import Question

def index(request: HttpRequest) -> HttpResponse:
    """
    Vue de l'accueil des sondages.
    Affiche la liste des dernières questions publiées.
    """
    # 1. On récupère les 5 dernières questions DESC
    latest_question_list = Question.objects.order_by("-pub_date")[:5]

    # 2."context" est un dictionnaire de views.
    context = {
        "latest_question_list": latest_question_list,
    }

    # 3. 'render'.
    # Requête + nom du fichier HTML + data/context.
    return render(request, "polls/index.html", context)

def detail(request: HttpRequest, question_id: int) -> HttpResponse:
    """Affiche une question."""
    return HttpResponse(f"Infos de la question n°{question_id}.")

def results(request: HttpRequest, question_id: int) -> HttpResponse:
    """Affiche les résultats d'une question."""
    return HttpResponse(f"Résultats de la question n°{question_id}.")

def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    """Gère le vote d'une question."""
    return HttpResponse(f"Vous allez voter pour la question n°{question_id}.")