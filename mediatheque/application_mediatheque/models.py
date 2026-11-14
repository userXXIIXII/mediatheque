from django.db import models

# Create your models here.
from django.db import models

class Media(models.Model):
    titre = models.CharField(max_length=100, verbose_name="Titre")
    date_publication = models.IntegerField(verbose_name="Année de publication")

    class Meta:
        abstract = True

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