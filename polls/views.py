from datetime import datetime
from typing import Optional, Union

from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import QuerySet, Sum, Avg
from django.utils import timezone
from django.views.decorators.cache import never_cache

from polls.forms import QuestionForm

from .models import Question, Choice

# Context type
ContextValue = Union[int, float, datetime, str, None, Question, QuerySet[Question]]

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
    """Affiche les résultats."""
    # get question
    question = get_object_or_404(Question, pk=question_id)
    # => template results.html
    return render(request, "polls/results.html", {"question": question})

# VOTE
def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    try:
        # Recup ID de la selection dans le form : name="choice"
       selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # !choice
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "Choisissez une réponse !",
        })
    else:
        # Incrémenter count
        selected_choice.votes += 1
        selected_choice.save()

        q_id = int(getattr(question, 'pk'))

        # TOUJOURS renvoyer un HttpResponseRedirect après un POST.
        # Pour éviter de compter 2 fois si l'user clique sur "précédent".
        # Virgule pour indiquer que c'ets un Tuple et pas un chiffre avec des parenthèses autour
        return HttpResponseRedirect(reverse("polls:results", args=(int(q_id),)))
# TOUS LES SONDAGES
def all_polls(request: HttpRequest) -> HttpResponse:
    questions = Question.objects.all().order_by("id")
    return render(request, "polls/all_polls.html", {"questions": questions})

# STATS
def statistics(request: HttpRequest)-> HttpResponse:
    total_questions = int(Question.objects.count())
    total_choices = int(Choice.objects.count())

    # Somme de tous les votes de tous les choix
    # "aggregate" == dict
    total_votes = Choice.objects.aggregate(Sum('votes'))['votes__sum'] or 0

    # Moyenne de votes par question
    # Moyenne des votes sur l'ensemble des choix
    avg_votes = Choice.objects.aggregate(Avg('votes'))['votes__avg'] or 0

    # Dernière question ID la plus grande
    try:
        last_created_question: Optional[Question] = Question.objects.latest('id')
    except Question.DoesNotExist:
        last_created_question = None

    questions_list = Question.objects.all()

    context: dict[str, ContextValue] = {
        'total_questions': total_questions,
        'total_choices': total_choices,
        'total_votes': total_votes,
        'avg_votes': round(avg_votes, 2),
        'last_question': last_created_question,
        'questions_list': questions_list,
    }
    return render(request, 'polls/statistics.html', context)

def question_create(request: HttpRequest)-> HttpResponse:
    if request.method == 'POST':
        # Formulaire envoyé
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls:index') # Retour accueil
    else:
        # formulaire vide
        form = QuestionForm()

    return render(request, 'polls/question_form.html', {'form': form})

# QUESTION
@never_cache
def create_question(request: HttpRequest) -> HttpResponse:
    # Click "enregistrer"
    if request.method == "POST":
        question_text = request.POST.get("question_text")

        # Recup choix
        raw_choices = {
            f"choice_{i}": request.POST.get(f"choice_{i}", "").strip()
            for i in range(1, 6)
        }

        # Filtre !empty
        valid_choices = [c for c in raw_choices.values() if c]

        # 2 choix mini
        if not question_text or len(valid_choices) < 2:
            return render(request, "polls/create_question.html", {
                "error_message": "Un sondage nécessite une question & au moins 2 choix !",
                "question_text": question_text,
                "choices_data": raw_choices,
            })

        # OK
        new_q = Question(question_text=question_text, pub_date=timezone.now())
        new_q.save()

        for choice_text in valid_choices:
            new_q.choice_set.create(choice_text=choice_text, votes=0)

        return HttpResponseRedirect(reverse("polls:index"))

    return render(request, "polls/create_question.html")

def frequency(request: HttpRequest, question_id: int)-> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    choices_stats = question.get_choices()
    champion = question.get_max_choice()

    return render(request, "polls/frequency.html", {
        "question": question,
        "choices_stats": choices_stats,
        "champion": champion,
    })