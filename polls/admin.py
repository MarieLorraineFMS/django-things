"""
Configuration de l'admin.
"""
from django.contrib import admin
from .models import Question, Choice

class QuestionAdmin(admin.ModelAdmin):
    # 4.1 : colonnes
    list_display = ('question_text', 'pub_date', 'display_was_published_recently')

    # 4.1 : affichage icones check/X
    @admin.display(boolean=True, description='Publié récemment ?')
    def display_was_published_recently(self, obj: Question) -> bool:
        return obj.was_published_recently()

    # 4.2 & 4.3
    list_filter = ['pub_date']
    search_fields = ['question_text']

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question', 'votes')
    list_filter = ['question']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)