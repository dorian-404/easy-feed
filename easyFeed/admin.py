import csv
import io

from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path

from .models import TypeUtilisateur, Utilisateur, Pays, FormulationDisponible, Ingredient, CategorieIngredient, Recette, \
    PhaseDeveloppement, PhaseActuelle, Vague, VagueRecette, Vaccin, VaccinAdministre, EvolutionMasse, Perte, Sortie, \
    ListeIngredients, Client, TypeAbonnement, Abonnement

from .forms import ListeIngredientsImport


# appel du decorateur admin
@admin.register(TypeUtilisateur)
class TypeUtilisateurAdmin(admin.ModelAdmin):
    list_display = ["id", "titre", "created", "updated"]
    search_fields = ["titre"]
    list_filter = ["titre"]

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ["matricule", "codePays", "nom", "prenom", "dateNaissance", "numeroTelephone", "adresse", "email", "dateEmbauche", "created", "updated"]
    search_fields = ["codePays"]
    list_filter = ["nom"]

@admin.register(Pays)
class PaysAdmin(admin.ModelAdmin):
    list_display = ["nomPays", "codePays"]
    search_fields = ["nomPays"]
    list_filter = ["nomPays"]

@admin.register(FormulationDisponible)
class FormulationDisponibleAdmin(admin.ModelAdmin):
    list_display = ["codeAnimal", "nomAnimal"]
    search_fields = ["nomAnimal"]
    list_filter = ["nomAnimal"]

@admin.register(ListeIngredients)
class ListeIngredientsAdmin(admin.ModelAdmin):
    list_display = ["codeIngredient", "nomIngredient", "proteineBrute", "energieMetabolisable",
                     "matiereGrasse", "celluloseBrute", "calcium", "phosphore", "lysine", "methionine",
                    "cysteineMethionine", "sodium", "prix"]
    change_list_template = "entities/listIngredients_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import_csv/', self.import_csv)
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["file"]    # request.POST['Pays'] (pour une variable)
            content = io.StringIO(csv_file.read().decode('latin-1'))
            csv_reader = csv.reader(content, delimiter=";")

            for line in csv_reader:
                liste_ingredients = ListeIngredients()
                liste_ingredients.codeIngredient = line[0]
                liste_ingredients.nomIngredient = line[1]
                liste_ingredients.proteineBrute = line[2]
                liste_ingredients.energieMetabolisable = line[3]
                liste_ingredients.matiereGrasse = line[4]
                liste_ingredients.celluloseBrute = line[5]
                liste_ingredients.calcium = line[6]
                liste_ingredients.phosphore = line[7]
                liste_ingredients.lysine = line[8]
                liste_ingredients.methionine = line[9]
                liste_ingredients.cysteineMethionine = line[10]
                liste_ingredients.sodium = line[11]
                liste_ingredients.prix = line[12]
                liste_ingredients.save()

            self.message_user(request, "Your csv file has been imported succesfully")
            return redirect("..")

        form = ListeIngredientsImport()
        return render(request, "admin/csv_form.html", {'form': form})

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["id","codeIngredient"]

@admin.register(CategorieIngredient)
class CategorieIngredientAdmin(admin.ModelAdmin):
    list_display = ["id", "codeAnimal", "nomCategorie"]

@admin.register(Recette)
class RecetteAdmin(admin.ModelAdmin):
    list_display = ["codeRecette", "recette", "codeAnimal", "codePays", "matricule"]

@admin.register(PhaseDeveloppement)
class PhaseDeveloppementAdmin(admin.ModelAdmin):
    list_display = ["codePhase", "trancheAge", "nomPhase", "proteineBruteMin", "proteineBruteMax", "energieMetabolisableMin",
                    "energieMetabolisableMax", "matiereGrasseMin", "matiereGrasseMax","calciumMin", "calciumMax", "phosphoreMin",
                    "phosphoreMax", "lysineMin", "lysineMax", "methionineMin", "methionineMax", "cysteineMethionineMin", "cysteineMethionineMax",
                    "sodiumMin", "sodiumMax", "ratioEnergieProteineMin", "ratioEnergieProteineMax", "ratioCalciumPhosphoreMin",
                    "ratioCalciumPhosphoreMax", "ratioLysineMethionineMin", "ratioLysineMethionineMax"]

@admin.register(PhaseActuelle)
class PhaseActuelleAdmin(admin.ModelAdmin):
    list_display = ["id", "codeAnimal", "codePhase"]

@admin.register(Vague)
class VagueAdmin(admin.ModelAdmin):
    list_display = ["codeVague", "qte", "age", "masse", "nomAnimal", "matricule", "codePhase"]

@admin.register(VagueRecette)
class VagueRecetteAdmin(admin.ModelAdmin):
    list_display = ["id", "codeVague", "codeRecette"]

@admin.register(Vaccin)
class VaccinAdmin(admin.ModelAdmin):
    list_display = ["codeVaccin", "nomVaccin"]

@admin.register(VaccinAdministre)
class VaccinAdministreAdmin(admin.ModelAdmin):
    list_display = ["id", "codeVaccin", "codeVague"]

@admin.register(EvolutionMasse)
class EvolutionMasseAdmin(admin.ModelAdmin):
    list_display = ["id", "nouvelAge", "dateEvolution", "nouvelleMasse", "codeVague"]

@admin.register(Perte)
class PerteAdmin(admin.ModelAdmin):
    list_display = ["codePerte", "qtePerte", "dateDeces", "codeVague", "commentaires"]

@admin.register(Sortie)
class SortieAdmin(admin.ModelAdmin):
    list_display = ["codeSortie", "qteSortie", "dateSortie", "masseSortie", "codeVague"]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["id", "nom", "prenom", "email", "password"]
    search_fields = ["nom"]
    list_filter = ["nom"]

@admin.register(TypeAbonnement)
class TypeAbonnementAdmin(admin.ModelAdmin):
    list_display = ["id", "titre", "prix", "duree"]
    search_fields = ["titre"]
    list_filter = ["titre"]

@admin.register(Abonnement)
class AbonnementAdmin(admin.ModelAdmin):
    list_display = ["id", "client", "type_abonnement", "date_debut", "date_fin"]
    search_fields = ["client"]
    list_filter = ["client"]