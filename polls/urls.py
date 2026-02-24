"""
Configuration des URLs pour l'app Polls.
"""
from django.urls import path
#  "from . import views" signifie "importe le module views qui est dans le même dossier que ce fichier urls.py"

from . import views

# app_name est utilisé pour différencier les URLs de cette app des autres apps du projet.
app_name = "polls"

urlpatterns = [
    # Route pour l'accueil de l'application
    # path("", views.index, name="index") signifie :
    # - "" : chemin vide, c'est la racine de l'app (ex: /polls/)
    # - views.index : la fonction à appeler pour cette route, définie dans views.py
    # - name="index" : un nom pour cette route, utilisé pour la référencer facilement dans le code (ex: {% url 'polls:index' %})
    path("", views.index, name="index"),
]