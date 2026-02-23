"""
Module de gestion des modèles pour l'application Polls.
Ce fichier définit comment sont rangées nos Questions et nos Choix
dans la base de données, un peu comme un inventaire de magasin.
"""
import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    Modèle représentant une question de sondage.
    Chaque question à une date de publication et un texte.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date de publication')

    def __str__(self) -> str:
        """Affiche le texte de la question au lieu d'un numéro."""
        return str(self.question_text)

    def was_published_recently(self) -> bool:
        """Vérifie si la question a été posée il y a moins de 24h."""
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    """
    Modèle représentant un choix de réponse.
    Chaque Choix est lié à une Question, a un texte et un nombre de votes.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        """Affiche le texte du choix au lieu d'un numéro."""
        return str(self.choice_text)