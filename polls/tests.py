import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """Vérifie si la date renseignée est dans le futur."""
        print("\n--- Test : publication dans le futur en cours ---")
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        resultat = future_question.was_published_recently()
        print(f"Date testée : {time}")
        print(f"Réponse : {resultat}")

        self.assertIs(resultat, False)
        print("✅ La date renseignée est dans le futur !")

    def test_was_published_recently_with_old_question(self):
        """
        Vérifie si la date renseignée est plus ancienne que 1 jour.
        """
        print("\n--- Test : publication dans le passé lointain en cours ---")
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)

        resultat = old_question.was_published_recently()
        print(f"Date testée : {time}")
        print(f"Réponse : {resultat}")

        self.assertIs(resultat, False)
        print("✅ La date renseignée est a plus de 24h !")

    def test_was_published_recently_with_recent_question(self):
        """Renvoie True si la date renseignée est dans les 24h."""
        print("\n--- Test : date dans les 24h en cours ---")
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59)
        recent_question = Question(pub_date=time)

        resultat = recent_question.was_published_recently()
        print(f"Date testée : {time}")
        print(f"Réponse : {resultat}")

        self.assertIs(resultat, True)
        print("✅ La date se situe dans les 24h !")