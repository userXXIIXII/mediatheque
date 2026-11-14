from django.db import models
from django.utils import timezone
from datetime import timedelta

# 1. Modèles de médias (POO)

class Media(models.Model):
    titre = models.CharField(max_length=100, verbose_name="Titre")
    date_publication = models.IntegerField(verbose_name="Année de publication")

    class Meta:
        #abstract = True, indique que c'est une classe de base orientée objet
        #Aucune table Media n'est créée directement en base MySQL, seulement les modeles enfants auront une table
        abstract = True

    #__str__: méthode spéciale Python qui définit la représentation textuelle de l'objet
    #C'est ce qui s'affiche proprement dans l'interface d'administration Django
    def __str__(self):
        return self.titre

class Livre(Media):
    auteur = models.CharField(max_length=150, verbose_name="Auteur")
    nombre_pages = models.IntegerField(verbose_name="Nombre de pages")

class Dvd(Media):
    realisateur = models.CharField(max_length=150, verbose_name="Réalisateur")
    duree_minutes = models.IntegerField(verbose_name="Durée (en minutes)")

class Cd(Media):
    artiste = models.CharField(max_length=150, verbose_name="Artiste / Groupe")
    nombre_pistes = models.IntegerField(verbose_name="Nombre de pistes")

class JeuDePlateau(Media):
    createur = models.CharField(max_length=150, verbose_name="Créateur du plateau")
    nombre_joueurs_min = models.IntegerField(verbose_name="Nombre de joueurs min")
    nombre_joueurs_max = models.IntegerField(verbose_name="Nombre de joueurs max")

    def __str__(self):
        return f"{self.titre} (Jeu de plateau)"

# 2. Modèle Membre

class Membre(models.Model):
    nom = models.CharField(max_length=150, verbose_name="Nom")
    prenom = models.CharField(max_length=150, verbose_name="Prenom")
    email = models.EmailField(verbose_name="Email")
    date_inscription = models.DateField(auto_now_add=True, verbose_name="Date inscription")
    est_penalise = models.BooleanField(default=False, verbose_name="Est pénalisé (bloqué)")

    def __str__(self):
        return f"{self.prenom} ({self.nom})"

# 3. Modèle Emprunt

class Emprunt(models.Model):
    #ForeignKey : Crée une relation (clé étrangère) entre la table Emprunt et la table Membre
    #on_delete=models.CASCADE : Si le membre est supprimé de la base, tous ses emprunts sont supprimés automatiquement
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, verbose_name="Membre")

    #On lie l'emprunt uniquement aux types de médias autorisés (Livre, Cd, Dvd).
    #null=True, blank=True : Permet de laisser ces champs vides (car un emprunt concerne un seul média à la fois)
    #on_delete=models.SET_NULL : Si le média est supprimé, l'emprunt ne plante pas, le champ passe simplement à NULL
    livre = models.ForeignKey(Livre, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Livre")
    cd = models.ForeignKey(Cd, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="CD")
    dvd = models.ForeignKey(Dvd, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="DVD")

    #timezone.now : Récupère la date et l'heure actuelles de manière sécurisée (gestion des fuseaux horaires)
    date_emprunt = models.DateField(default=timezone.now, verbose_name="Date d'emprunt")

    #Stocke la date limite de restitution du média
    date_retour_prevue = models.DateField(verbose_name="Date de retour prévue")

    # Date réelle à laquelle l'adhérent a ramené le média (reste vide / NULL tant qu'il ne l'a pas rendu)
    date_retour_effective = models.DateField(null=True, blank=True, verbose_name="Date de retour effective")

    def save(self, *args, **kwargs):
        #Surcharge de la méthode save() : On intercepte l'enregistrement pour appliquer une logique métier automatique
        #Si aucune date de retour n'a été spécifiée manuellement :
        if not self.date_retour_prevue:
            # timedelta(days=7) : Permet d'ajouter exactement 7 jours (1 semaine) à la date actuelle du jour.
            self.date_retour_prevue = timezone.now().date() + timedelta(days=7)

        # Appel de la méthode save() d'origine de Django pour finaliser l'écriture effective dans la base MySQL
        super().save(*args, **kwargs)

    def __str__(self):
        #Récupère le média concerné parmi les trois types possibles (celui qui n'est pas vide)
        media_concerne = self.livre or self.cd or self.dvd
        return f"Emprunt de [{media_concerne}] par {self.membre}"