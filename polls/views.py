from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Question, Choice

# Accueil
def index(request: HttpRequest) -> HttpResponse:
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

# DÉTAIL
def detail(request: HttpRequest, question_id: int) -> HttpResponse:
    """Affiche une question et ses choix (Exercice 3.1)."""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

# RÉSULTATS
def results(request: HttpRequest, question_id: int) -> HttpResponse:
    return HttpResponse(f"Vous regardez les résultats de la question {question_id}.")

# VOTE
def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    return HttpResponse(f"Vous votez pour la question {question_id}.")

# TOUS LES SONDAGES
def all_polls(request: HttpRequest) -> HttpResponse:
    questions = Question.objects.all().order_by("id")
    return render(request, "polls/all_polls.html", {"questions": questions})

# STATS
def statistics(request: HttpRequest) -> HttpResponse:
    total_questions = Question.objects.count()
    total_choices = Choice.objects.count()
    context = {
        "total_questions": total_questions,
        "total_choices": total_choices,
    }
    return render(request, "polls/statistics.html", context)