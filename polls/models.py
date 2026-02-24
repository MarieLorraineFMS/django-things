"""
Définition des modèles de données.
2.2.1.3.
"""
import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    """
    Une question de sondage.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date de publication')

    def __str__(self) -> str:
        return str(self.question_text)

    # 2.2.1.3 :
    def was_published_recently(self) -> bool:
        """
        Retourne True si la question a été publiée dans les dernières 24h.
        """
        now = timezone.now()
        # Entre "hier" et "maintenant"
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    """
    Un choix de réponse lié à une question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.choice_text)