# Compte-rendu : Administration Django (Étape 2.2.1.3)

**Auteur :** Marie-Lorraine
**Date :** 2026-02-24

## <span style="color:red">1. Observations de l'interface d'administration</span>

### <span style="color:green">Voyez-vous tous les attributs de vos classes ?</span>

Par défaut, Django n'affiche que le résultat de la méthode `__str__`.
Cependant, grâce à la configuration de la classe `QuestionAdmin` dans `admin.py` & à l'utilisation de `list_display`, nous voyons maintenant :

- Le texte de la question (`question_text`)
- La date de publication (`pub_date`)
- Le statut de publication récente (`was_published_recently`)

### <span style="color:green">Pouvez-vous filtrer vos données suivants tous les attributs ?</span>

Oui, grâce à l'ajout de `list_filter = ['pub_date']`.
_Actuellement :_ On peut filtrer par date (Aujourd'hui, 7 derniers jours, etc.).
_Note :_ On ne peut pas filtrer par le texte de la question directement via le menu latéral, car ce n'est pas pertinent pour un filtre, mais on utilise la recherche pour cela.

### <span style="color:green">Pouvez-vous trier vos données suivants tous les attributs ?</span>

Oui, en cliquant sur les en-têtes de colonnes dans l'interface.

- La colonne "Question Text" trie par ordre alphabétique.
- La colonne "Date de publication" trie par chronologie.
- Nous avons configuré le tri par défaut sur la date la plus récente (`ordering = ('-pub_date',)`).

### <span style="color:green">Pouvez-vous chercher un contenu parmi tous les champs ?</span>

Oui, grâce à `search_fields = ['question_text']`.
Une barre de recherche est apparue en haut de la liste. Si je tape un mot clé présent dans une de mes 5 questions, Django filtre instantanément les résultats.

## <span style="color:red">2. Gestion des accès & sécurité</span>

### <span style="color:green">Gestion des utilisateurs & groupes</span>

<span style="color:yellow">Création d'un groupe "Rédacteurs" :</span>

- **Droits accordés :** Ajout (`add`) et Modification (`change`) des questions.
- **Droit retiré :** Suppression (`delete`).
- **Résultat :** Connexion avec un compte membre "Rédacteurs", le bouton rouge "Supprimer" disparaît de l'interface. Cela sécurise la base de données contre les erreurs de manipulation.

### <span style="color:green">Historique des actions</span>

L'interface d'administration permet de tracer toutes les modifications.

- En haut à droite de chaque objet (Question ou Choix), le bouton **"Historique"** permet de voir quel utilisateur a modifié quoi et à quelle heure.
- C'est un outil essentiel pour le travail en équipe (audit).

### <span style="color:green">Désactivation de compte</span>

- **Action :** Désactivation du compte "Collaborateur" via l'attribut `is_active`.
- **Vérification :** L'accès est immédiatement révoqué sans suppression des données de l'utilisateur. C'est la méthode privilégiée en entreprise pour la sécurité des données.

## <span style="color:red">3. Localisation & Personnalisation de l'interface (UX)</span>

- **Niveau Application :** Modification de `apps.py` pour renommer le module global "Polls" en **"Gestion des Sondages"**.
- **Niveau Modèles :** Utilisation de la `class Meta` pour définir les noms au singulier et au pluriel. Ainsi, "Choices" est devenu **"Choix"** dans le menu de gauche.
- **Niveau Attributs (Détails) :** L'utilisation de `verbose_name` dans `models.py` a permis de traduire chaque champ :
  - `question_text` → **"Question"**
  - `pub_date` → **"Date de publication"**
  - `choice_text` → **"Choix"**
  - `votes` → **"Nombre de votes"**

## <span style="color:red">4. Maintenance et Désactivation de compte</span>

### <span style="color:green">Procédure de départ d'un collaborateur</span>

Procédure de désactivation :

- **Action effectuée :** Dans la fiche utilisateur, décochage de la case **"Actif"** (`is_active = False`).
- **Résultat du test de connexion :** \* Tentative de connexion avec l'identifiant désactivé : **Échec**.
  - Message d'erreur : "Veuillez saisir un nom d'utilisateur et un mot de passe corrects".
- **Conclusion :** L'accès est révoqué instantanément tout en conservant les traces de l'utilisateur dans l'historique.

## <span style="color:red">5. Shell Django</span>

### <span style="color:yellow">Vérification de la désactivation</span>

**Objectif :** Vérifier si un utilisateur a été désactivé.

**Commandes :**

```python
# 1. Import du module users
from django.contrib.auth.models import User

# 2. Recherche de l'utilisateur désactivé : "Active_False"
u = User.objects.get(username='Active_False')

# 3. Check "is_active"
print(u.is_active)
```

**Résultat obtenu :**

> `False`

**Conclusion :**

Ce résultat confirme que la base de données a bien enregistré la désactivation de l'utilisateur via l'interface graphique. L'accès est verrouillé au niveau du système, ce qui garantit la sécurité de l'application.

### <span style="color:yellow">Consultation & itération des données</span>

**Objectif :** Importer les modèles.

**Commandes :**

```python
from polls.models import Question, Choice
from django.utils import timezone
```

### <span style="color:green">Lister</span>

**Objectif :** Lister toutes les questions & leurs détails.

**Commandes :**

```python
for q in Question.objects.all():
    print(f"ID: {q.id} | Texte: {q.question_text}")
```

**Résultat obtenu :**

> ID: 1 | Texte: Quel texte pour cette question ? | Date: 2026-02-23 13:37:09+00:00

> ID: 2 | Texte: Une question en plus ? | Date: 2026-02-24 07:21:01+00:00

> ID: 3 | Texte: Une question encore ? | Date: 2025-10-15 04:00:00+00:00

> ID: 4 | Texte: Une très vieille question ? | Date: 2023-07-21 10:00:00+00:00

### <span style="color:green">Filtrer</span>

**Objectif :** Filtrer les questions publiées en 2026.

**Commandes :**

```python
Question.objects.filter(pub_date__year=2026)
```

**Résultat obtenu :**

> <QuerySet [<Question: Quel texte pour cette question ?>, <Question: Une question en >plus ?>]>

### <span style="color:green">Relations</span>

**Objectif :** Cibler une question (ID=2) & voir les réponses liées.

**Commandes :**

```python
q2 = Question.objects.get(id=2)
q2.choice_set.all()
```

**Résultat obtenu :**

> <QuerySet [<Choice: Oui>, <Choice: Non>]>

### <span style="color:green">Statistiques</span>

**Objectif :** Afficher le nombre de choix par question.

**Commandes :**

```python
for q in Question.objects.all():
    print(f"{q.question_text} : {q.choice_set.count()} choix")
```

**Résultat obtenu :**

> ...

> Quel texte pour cette question ? : 3 choix

> Une question en plus ? : 2 choix

> Une question encore ? : 2 choix

> Une très vieille question ? : 2 choix

> \>>>

### <span style="color:green">Tri</span>

**Objectif :** Classer les questions de la plus récente à la plus ancienne.

**Commandes :**

```python
Question.objects.order_by('-pub_date')
```

**Résultat obtenu :**

> <QuerySet [<Question: Une question en plus ?>, <Question: Quel texte pour cette question ?>, <Question: Une question encore ?>, <Question: Une très vieille question ?>]>

### <span style="color:yellow">Création d'un objet</span>

**Objectif :** Créer une nouvelle question & s'assurer de sa persistance.

**Commandes :**

```python
# CREATION
new_q = Question(question_text="Langage préféré ?", pub_date=timezone.now())
new_q.save()

# VERIFICATION

# Rechercher la dernière question publiée
last_q = Question.objects.order_by('-pub_date')[0]
print(last_q.question_text)

# Afficher son ID
print(last_q.id)
```

**Résultat obtenu :**

> Langage préféré ?

> 5

### <span style="color:yellow">Modification d'un objet</span>

**Objectif :** Remplir la BDD avec des scores variés pour tester les fonctions de tri.

**Commandes :**

```python
import random
from polls.models import Choice

for c in Choice.objects.all():
    c.votes = random.randint(0, 100)
    c.save()
    print(f"✅ Choix '{c.choice_text}' mis à jour avec {c.votes} votes.")
```

**Résultat obtenu :**

> ...

> ✅ Choix 'pour' mis à jour avec 68 votes.

> ✅ Choix 'Un' mis à jour avec 83 votes.

> ✅ Choix 'texte' mis à jour avec 66 votes.

> ✅ Choix 'Oui' mis à jour avec 26 votes.

> ✅ Choix 'Non' mis à jour avec 67 votes.

> ✅ Choix 'Oui toujours plus' mis à jour avec 36 votes.

> ✅ Choix 'Non ça suffit' mis à jour avec 46 votes.

> ✅ Choix '2024' mis à jour avec 67 votes.

> ✅ Choix '2023' mis à jour avec 64 votes.

> > > >

### <span style="color:yellow">Recherches croisées</span>

### <code style="color:green">contains() & distinct()</code>

**Objectif :** Trouver des questions en filtrant sur leurs choix associés.

**Commandes :**

```python
# RECHERCHE
# Double underscore pour passer du modèle Question au modèle Choice
results = Question.objects.filter(choice__choice_text__contains="oui").distinct()

# AFFICHAGE
for q in results:
    print(f" \"OUI\" fait partie des choix de la question : {q.question_text} - ID : {q.id}")
```

**Résultat obtenu :**

> ...

> "OUI" fait partie des choix de la question : Une question en plus ?

> "OUI" fait partie des choix de la question : Une question encore ?

> \>>>

### <code style="color:green">orderBy() & values()</code>

**Objectif :** Classer les questions en fonction des votes.

**Commandes :**

```python
# TRI
# Double underscore 'choice__votes' pour traverser la relation

# 'choice__votes' permet de trier la table Question via une colonne de la table Choice
# order_by('-choice__votes') pour DESC
sorted_q = Question.objects.order_by('choice__votes').values('question_text', 'choice__choice_text', 'choice__votes')

# AFFICHAGE
for item in sorted_q:
    print(f"Votes: {item['choice__votes']} | Question: {item['question_text']} | Choix: {item['choice__choice_text']}")
```

**Résultat obtenu :**

> ...
> Votes: None | Question: Langage préféré ? | Choix: None

> Votes: 0 | Question: Quel texte pour cette question ? | Choix: pour

> Votes: 0 | Question: Quel texte pour cette question ? | Choix: Un

> Votes: 0 | Question: Quel texte pour cette question ? | Choix: texte

> Votes: 0 | Question: Une question en plus ? | Choix: Oui

> Votes: 0 | Question: Une question en plus ? | Choix: Non

> Votes: 0 | Question: Une question encore ? | Choix: Oui toujours plus

> Votes: 0 | Question: Une question encore ? | Choix: Non ça suffit

> Votes: 0 | Question: Une très vieille question ? | Choix: 2024

> Votes: 0 | Question: Une très vieille question ? | Choix: 2023

> \>>
