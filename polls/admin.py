"""
Configuration de l'admin dashboard.
"""
from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3 # 3 lignes vides pour ajouter des choix rapidement

class QuestionAdmin(admin.ModelAdmin):
    """
    Personnalise la façon dont les questions sont affichées dans l'admin.
    """
    # 4.1 : on regroupe par thématique
    fieldsets = [
        ("Contenu principal", {"fields": ["question_text"]}),
        ("Calendrier de publication", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]

    # Insertion des choix dans le form directement
    inlines = [ChoiceInline]


    # 4.1 : Personalisation de la liste
    list_display = ('question_text', 'pub_date', 'display_was_published_recently')

    # 4.1 :
    # Transforme un "true/false" en icône : Check vert | Croix rouge
    # Plus visuel & rapide à comprendre
    @admin.display(boolean=True, description='Publié récemment ?')
    def display_was_published_recently(self, obj: Question) -> bool:
        return obj.was_published_recently()

    # 4.2 & 4.3 :
    # list_filter : Ajoute des filtres sur la droite pour filtrer les questions par date de publication.
    list_filter = ['pub_date']
    # search_fields : Ajoute une barre de recherche pour la recherche par mot clef sur le champ "question_text".
    search_fields = ['question_text']

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question', 'votes')
    list_filter = ['question']

# 4.1 : enregistrement des modèles
# On dit à Django : "Utilise ces modèles avec ces réglages de tableau de bord"
admin.site.register(Question, QuestionAdmin)

# Onglet du nav
admin.site.site_title = "Admin Sondages"

# Navbar text
admin.site.site_header = "TABLEAU DE BORD"

# Accueil titre
admin.site.index_title = "Ouelcome, on casse quoi aujourd'hui ?"