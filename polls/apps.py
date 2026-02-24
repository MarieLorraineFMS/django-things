"""
Configuration de l'app Polls.
"""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """
    Définit les réglages spécifiques à l'app 'polls'.
    """

    # default_auto_field définit le type d'ID par défaut pour chaque donnée.
    # BigAutoField permet de créer des milliards de lignes sans être bloqué par le nombre.
    default_auto_field = 'django.db.models.BigAutoField'
    # name est le nom de l'app, utilisé par Django pour identifier cette app.
    name = 'polls'
    # "Gestion des Sondages" : Le nom "humain" qui apparaîtra dans l'admin.
    verbose_name = "Gestion des Sondages"
