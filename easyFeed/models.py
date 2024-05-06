"""
    Ici sont définis tous les modèles de notre application.
    Les modèles permettent à l'ORM (Object-relational Mapper) django de générer nos tables
    et créer la base de données de motre application.
    Donc ces lignes de codes ont un équivalent sql
"""

from django.db import models

# class ListeIngredientsManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset()

class TypeUtilisateur(models.Model):
    titre = models.CharField(max_length=30, null=False)
    created = models.DateTimeField(auto_now_add=True)   #ajoute une date au moment de l'insertion
    updated = models.DateTimeField(auto_now=True)   #prendre la date au moment de la modification
    def __str__(self):
        return self.titre

class ListeIngredients(models.Model):
    # codeIngredient = models.CharField(primary_key=True, max_length=9)
    codeIngredient = models.CharField(unique=True, max_length=9)
    nomIngredient = models.CharField(max_length=50, null=False)
    proteineBrute = models.FloatField(null=True)
    energieMetabolisable = models.FloatField(null=True)
    matiereGrasse = models.FloatField(null=True)
    celluloseBrute = models.FloatField(null=True)
    calcium = models.FloatField(null=True)
    phosphore = models.FloatField(null=True)
    lysine = models.FloatField(null=True)
    methionine = models.FloatField(null=True)
    cysteineMethionine = models.FloatField(null=True)
    sodium = models.FloatField(null=True)
    prix = models.FloatField(null=False)
    created = models.DateTimeField(auto_now_add=True)  # ajoute une date au moment de l'insertion
    updated = models.DateTimeField(auto_now=True)  # prendre la date au moment de la modification

    objects = models.Manager()   # manager par defaut
    # liste_ingredient = ListeIngredientsManager()
    def __str__(self):
        return f"{self.codeIngredient}"

class Pays(models.Model):
    # codePays = models.CharField(primary_key=True, max_length=3)
    codePays = models.CharField(max_length=3, unique=True)
    nomPays = models.CharField(max_length=40, null=False)
    created = models.DateTimeField(auto_now_add=True)  # ajoute une date au moment de l'insertion
    updated = models.DateTimeField(auto_now=True)  # prendre la date au moment de la modification
    objects = models.Manager()  # manager par defaut
    def __str__(self):
        return self.codePays
        # return f"{self.codePays} ({self.nomPays})"

class Utilisateur(models.Model):
    codePays = models.ForeignKey(Pays, on_delete=models.CASCADE)
    idTypeUtilisateur = models.ForeignKey(TypeUtilisateur, related_name="Type_Utilisateurs", on_delete=models.CASCADE)
    # matricule = models.CharField(primary_key=True, max_length=7)
    matricule = models.CharField(unique=True, max_length=7)
    nom = models.CharField(max_length=80, null=False)
    prenom = models.CharField(max_length=80)
    dateNaissance = models.DateField(null=False)    #faire la validation au niveau du formulaire
    dateEmbauche = models.DateField(null=False)
    numeroTelephone = models.CharField(max_length=10, null=False)
    adresse = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=200, null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)  # ajoute une date au moment de l'insertion
    updated = models.DateTimeField(auto_now=True)  # prendre la date au moment de la modification

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class FormulationDisponible(models.Model):
    # codeAnimal = models.CharField(primary_key=True, max_length=3)
    codeAnimal = models.CharField(unique=True, max_length=3)
    nomAnimal = models.CharField(max_length=30, null=False)
    created = models.DateTimeField(auto_now_add=True)  # ajoute une date au moment de l'insertion
    updated = models.DateTimeField(auto_now=True)  # prendre la date au moment de la modification
    objects = models.Manager()  # manager par defaut
    def __str__(self):
        return self.nomAnimal

class Ingredient(models.Model):
    codeIngredient = models.ForeignKey(ListeIngredients, on_delete=models.CASCADE)
    codePays = models.ForeignKey(Pays, on_delete=models.CASCADE, default='CMR')
    created = models.DateTimeField(auto_now_add=True)  # ajoute une date au moment de l'insertion
    updated = models.DateTimeField(auto_now=True)  # prendre la date au moment de la modification
    objects = models.Manager()  # manager par defaut

class CategorieIngredient(models.Model):
    idIngredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    codeAnimal = models.ForeignKey(FormulationDisponible, on_delete=models.CASCADE, default='PL')
    nomCategorie = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)  # ajoute une date au moment de l'insertion
    updated = models.DateTimeField(auto_now=True)  # prendre la date au moment de la modification


class Recette(models.Model):
    # codeRecette = models.CharField(primary_key=True, max_length=4)
    codeRecette = models.CharField(unique=True, max_length=4)
    recette = models.CharField(max_length=255)
    codeAnimal = models.ForeignKey(FormulationDisponible, related_name="Recettes", on_delete=models.CASCADE)
    codePays = models.ForeignKey(Pays, on_delete=models.CASCADE)
    matricule = models.ForeignKey(Utilisateur, related_name="Recettes", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)  # ajoute une date au moment de l'insertion
    updated = models.DateTimeField(auto_now=True)  # prendre la date au moment de la modification
    def __str__(self):
        return self.codeRecette

class PhaseDeveloppement(models.Model):
    # codePhase = models.CharField(primary_key=True, max_length=4)
    codePhase = models.CharField(unique=True, max_length=4)
    trancheAge = models.CharField(max_length=30, null=False)
    nomPhase = models.CharField(max_length=30, null=False)
    proteineBruteMin = models.FloatField(null=False)
    proteineBruteMax = models.FloatField(null=False)
    energieMetabolisableMin = models.FloatField(null=False)
    energieMetabolisableMax = models.FloatField(null=False)
    matiereGrasseMin = models.FloatField(null=False)
    matiereGrasseMax = models.FloatField(null=False)
    calciumMin = models.FloatField(null=False)
    calciumMax = models.FloatField(null=False)
    phosphoreMin = models.FloatField(null=False)
    phosphoreMax = models.FloatField(null=False)
    lysineMin = models.FloatField(null=False)
    lysineMax = models.FloatField(null=False)
    methionineMin = models.FloatField(null=False)
    methionineMax = models.FloatField(null=False)
    cysteineMethionineMin = models.FloatField(null=False)
    cysteineMethionineMax = models.FloatField(null=False)
    sodiumMin = models.FloatField(null=False)
    sodiumMax = models.FloatField(null=False)
    ratioEnergieProteineMin = models.FloatField(null=False)
    ratioEnergieProteineMax = models.FloatField(null=False)
    ratioCalciumPhosphoreMin = models.FloatField(null=False)
    ratioCalciumPhosphoreMax = models.FloatField(null=False)
    ratioLysineMethionineMin = models.FloatField(null=False)
    ratioLysineMethionineMax = models.FloatField(null=False)
    created = models.DateTimeField(auto_now_add=True)  # ajoute une date au moment de l'insertion
    updated = models.DateTimeField(auto_now=True)  # prendre la date au moment de la modification
    objects = models.Manager()  # manager par defaut
    def __str__(self):
        return f"{self.codePhase} ({self.nomPhase})"

class PhaseActuelle(models.Model):
    codeAnimal = models.ForeignKey(FormulationDisponible, related_name="Phases", on_delete=models.CASCADE)
    codePhase = models.ForeignKey(PhaseDeveloppement, related_name="Phases", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)  # ajoute une date au moment de l'insertion
    updated = models.DateTimeField(auto_now=True)  # prendre la date au moment de la modification

class Vague(models.Model):
    # codeVague = models.CharField(primary_key=True, max_length=9)
    codeVague = models.CharField(unique=True, max_length=9)
    qte = models.IntegerField(null=False)
    age = models.CharField(max_length=20, null=False)
    masse = models.FloatField(null=False)
    nomAnimal = models.CharField(max_length=30, null=False)
    matricule = models.ForeignKey(Utilisateur, related_name="Vagues", on_delete=models.CASCADE)
    codePhase = models.ForeignKey(PhaseDeveloppement, related_name="Vagues", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)  # ajoute une date au moment de l'insertion
    updated = models.DateTimeField(auto_now=True)  # prendre la date au moment de la modification
    def __str__(self):
        return self.codeVague

class VagueRecette(models.Model):
    codeRecette = models.ForeignKey(Recette, related_name="Vagues", on_delete=models.CASCADE)
    codeVague = models.ForeignKey(Vague, related_name="Recettes", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)  # ajoute une date au moment de l'insertion
    updated = models.DateTimeField(auto_now=True)  # prendre la date au moment de la modification

class Vaccin(models.Model):
    # codeVaccin = models.CharField(primary_key=True, max_length=3)
    codeVaccin = models.CharField(unique=True, max_length=3)
    nomVaccin = models.CharField(max_length=50, null=False)
    created = models.DateTimeField(auto_now_add=True)  # ajoute une date au moment de l'insertion
    updated = models.DateTimeField(auto_now=True)  # prendre la date au moment de la modification
    def __str__(self):
        return f"{self.codeVaccin} ({self.nomVaccin})"

class VaccinAdministre(models.Model):
    codeVaccin = models.ForeignKey(Vaccin, related_name="Vagues", on_delete=models.CASCADE)
    codeVague = models.ForeignKey(Vague, related_name="Vaccins", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)  # ajoute une date au moment de l'insertion
    updated = models.DateTimeField(auto_now=True)  # prendre la date au moment de la modification

class EvolutionMasse(models.Model):
    nouvelAge = models.IntegerField(null=False)
    dateEvolution = models.DateField(null=False)
    nouvelleMasse = models.FloatField(null=False)
    codeVague = models.ForeignKey(Vague, related_name="Masses", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)  # ajoute une date au moment de l'insertion
    updated = models.DateTimeField(auto_now=True)  # prendre la date au moment de la modification

class Perte(models.Model):
    # codePerte = models.CharField(primary_key=True, max_length=14)
    codePerte = models.CharField(unique=True, max_length=14)
    qtePerte = models.IntegerField(null=False)
    dateDeces = models.DateField(null=False)
    commentaires = models.CharField(max_length=600)
    codeVague = models.ForeignKey(Vague, related_name="Pertes", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)  # ajoute une date au moment de l'insertion
    updated = models.DateTimeField(auto_now=True)  # prendre la date au moment de la modification

class Sortie(models.Model):
    # codeSortie = models.CharField(primary_key=True, max_length=14)
    codeSortie = models.CharField(unique=True, max_length=14)
    qteSortie = models.IntegerField(null=False)
    dateSortie = models.DateField(null=False)
    masseSortie = models.FloatField(null=False)
    codeVague = models.ForeignKey(Vague, related_name="Sorties", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)  # ajoute une date au moment de l'insertion
    updated = models.DateTimeField(auto_now=True)  # prendre la date au moment de la modification