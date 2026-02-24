"""
Définition des modèles de données.
2.2.1.3.
"""
import datetime
from typing import TYPE_CHECKING
from django.db import models
from django.utils import timezone

# --- Pylance things ---
# TYPE_CHECKING : vaut "True" pour VS Code & "False" quand le site tourne.
#
# On l'utilise pour importer des outils dont Pylance a besoin pour ne pas "paniquer",
# mais qui ne sont pas nécessaires à l'exécution.

if TYPE_CHECKING:
    # Le RelatedManager est l'outil que Django utilise pour gérer les relations "Question -> Choice".
    # On l'importe ici uniquement pour que Pylance puisse comprendre que "choice_set" est un RelatedManager de Choice.
    # Sans ça, Pylance se plaint que "choice_set" n'existe pas ou qu'on ne peut pas faire "choice_set.all()".
    from django.db.models.manager import RelatedManager

class Question(models.Model):
    """
    Une question du sondage.
    """
    question_text = models.CharField(max_length=200, verbose_name="Question")
    pub_date = models.DateTimeField('date de publication')

    # On déclare 'choice_set' pour que Pylance comprenne que c'est un RelatedManager de Choice.
    # En réalité, Django crée automatiquement cet attribut "choice_set" pour gérer la relation inverse de "Choice -> Question".
    choice_set: 'RelatedManager[Choice]'

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self) -> str:
        # 2.2.3> 3 & 4 Affiche les 20 premiers caractères de la question suivis de la date de publication
        short_text = self.question_text[:20]
        return f"{short_text}... (Publiée le : {self.pub_date.strftime('%d/%m/%Y')})"

    # 2.2.3> 1 :
    def age(self)-> datetime.timedelta:
        # Ecart entre "maintenant" et sa "création"
        ecart = timezone.now() - self.pub_date
        return ecart

    # 2.2.1.3 :
    def was_published_recently(self) -> bool:
        """
        Retourne True si la question a été publiée dans les dernières 24h.
        """
        now = timezone.now()
        # Entre "hier" et "maintenant"
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def get_choices(self) -> list[tuple[str, int, float]]:
            """Retourne la liste des choix avec votes et proportions.
            tuple : (texte_du_choix, nb_votes, proportion_en_%)
            """
            # On utilise choice_set pour lister tous les Choices liés à cette Question
            all_choices = list(self.choice_set.all())

            # Calcul du nombre total de votes pour cette question
            # On convertit les votes en int au cas où ils seraient stockés comme des string.
            total_votes: int = sum(int(c.votes) for c in all_choices)

            resultats: list[tuple[str, int, float]] = []
            for c in all_choices:
                c_votes = int(c.votes)
                proportion: float = (c_votes / total_votes * 100) if total_votes > 0 else 0.0
                resultats.append((str(c.choice_text), c_votes, proportion))

            return resultats

    def get_max_choice(self) -> tuple[str, int, float]|None:
        """Retourne le choix ayant reçu le plus de votes."""
        all_choices = list(self.choice_set.all())

        if not all_choices:
            return None

        # Trouve le choix avec le plus de votes
        champion = max(all_choices, key=lambda c: int(c.votes))

        total_votes: int = sum(int(c.votes) for c in all_choices)
        champ_votes = int(champion.votes)
        proportion: float = (champ_votes / total_votes * 100) if total_votes > 0 else 0.0

        return (str(champion.choice_text), champ_votes, proportion)

class Choice(models.Model):
    """
    Un choix de réponse lié à une question.
    """
    # La relation "ForeignKey" indique que chaque Choice est lié à une Question.
    # "on_delete=models.CASCADE" signifie que si la Question est supprimée, tous les Choices liés seront aussi supprimés.
    # C'est ce lien qui permet à Django de créer automatiquement l'attribut "choice_set" dans Question pour accéder à tous les Choices liés.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200,verbose_name="Choix")
    votes = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Choix"
        verbose_name_plural = "Choix"

    def __str__(self) -> str:
        return str(self.choice_text)