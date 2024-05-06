from django.shortcuts import render, get_object_or_404
from .models import ListeIngredients, FormulationDisponible, PhaseDeveloppement, Pays, Ingredient
from django.http import Http404, JsonResponse
import pandas as pd
import json
import logging

# cree un logger (journal d'erreur pour enregistrer les erreurs)
logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'html/home.html', context={})


def login(request):
    return render(request, 'html/login.html', context={})


def dashboard(request):
    return render(request, 'html/dashboard.html', context={})


def formulation(request):
    return render(request, 'html/formulation.html', context={})


# requete pour recuperer tous les ingredients

def ingredient_test(request):
    # ListeIngredient
    ingredients = ListeIngredients.objects.all()

    # FormulationDisponible
    animaux = FormulationDisponible.objects.all()
    animaux_data = FormulationDisponible.objects.values('id', 'codeAnimal', 'nomAnimal')

    # PhaseDeveloppement
    ages = PhaseDeveloppement.objects.all()

    # Pays
    countries = Pays.objects.all()

    ingredients_df = ListeIngredients.objects.values('proteineBrute', 'energieMetabolisable',
                                                     'matiereGrasse', 'celluloseBrute', 'calcium',
                                                     'phosphore',
                                                     'lysine', 'methionine',
                                                     'cysteineMethionine',
                                                     'sodium', 'prix')

    # exemple de conversion en dataFrame
    # Methode #1 (consomme beaucoup de memoire)
    df = pd.DataFrame(list(ingredients_df))  # caster ingredient_df en dataFrame
    print(df)

    # Methode #2
    df2 = pd.DataFrame.from_records(ingredients_df)
    print(df2)

    return render(request,
                  'html/test/ingredient_test.html',
                  {'ingredients': ingredients, 'animaux': animaux, 'ages': ages, 'countries': countries, })


def details_ingredient(request):
    ingredient = request.GET.get('ingredient')
    print(ingredient)
    try:
        nutriments = ListeIngredients.objects.get(id=ingredient)
        print(nutriments.proteineBrute)
        nutriments = {'proteineBrute': nutriments.proteineBrute,
                      'energieMetabolisable': nutriments.energieMetabolisable,
                      'matiereGrasse': nutriments.matiereGrasse,
                      'celluloseBrute': nutriments.celluloseBrute, 'calcium': nutriments.calcium,
                      'phosphore': nutriments.phosphore,
                      'lysine': nutriments.lysine, 'methionine': nutriments.methionine,
                      'cysteineMethionine': nutriments.cysteineMethionine,
                      'sodium': nutriments.sodium}
        print(nutriments)
    except ListeIngredients.DoesNotExist:
        raise Http404("L'ingredient spécifié n'existe pas.")
    except Exception as e:
        raise Http404("Une erreur s'est produite lors de la récupération des nutriments.")

    return JsonResponse(nutriments, safe=False)


def pays_ingredients(request):
    code_pays = request.GET.get('code_pays')
    print(code_pays)
    try:
        ing_pays = Ingredient.objects.filter(codePays__codePays=code_pays)
        ingredients = []
        for ing in ing_pays:
            ingredients.append(ing.codeIngredient.nomIngredient)
    except Ingredient.DoesNotExist:
        raise Http404("Le pays spécifié n'existe pas ou n'a pas d'ingrédients associés.")
    except Exception as e:
        raise Http404("Une erreur s'est produite lors de la récupération des ingrédients.")

    return JsonResponse(ingredients, safe=False)


"""
    les deux ecritures suivantes du for sont equivalentes:

    for ing in ing_pays:
        ingredients = [ing.codeIngredient.nomIngredient]     
        
        OU
        
    ingredients = [ing.codeIngredient.nomIngredient for ing in ing_pays]  
"""


def obtenir_contraintes(request):
    id_phase = request.GET.get('id_phase')
    print(f"ID de phase reçu : {id_phase}")  # Instruction d'impression
    logger.info(f"ID de phase reçu : {id_phase}")  # Instruction de journalisation
    try:
        contraintes = PhaseDeveloppement.objects.get(id=id_phase)
        print(contraintes.lysineMin)

        # Ajouter des instructions d'impression et de journalisation après avoir obtenu les contraintes
        print(f"Contraintes obtenues : {contraintes}")
        logger.info(f"Contraintes obtenues : {contraintes}")

        contraintes = {'nomPhase': contraintes.nomPhase,
                       'proteineBruteMin': contraintes.proteineBruteMin,
                       'proteineBruteMax': contraintes.proteineBruteMax,
                       'energieMetabolisableMin': contraintes.energieMetabolisableMin,
                       'energieMetabolisableMax': contraintes.energieMetabolisableMax,
                       'matiereGrasseMin': contraintes.matiereGrasseMin,
                       'matiereGrasseMax': contraintes.matiereGrasseMax,
                       'calciumMin': contraintes.calciumMin,
                       'calciumMax': contraintes.calciumMax,
                       'phosphoreMin': contraintes.phosphoreMin,
                       'phosphoreMax': contraintes.phosphoreMax,
                       'lysineMin': contraintes.lysineMin,
                       'lysineMax': contraintes.lysineMax,
                       'methionineMin': contraintes.methionineMin,
                       'methionineMax': contraintes.methionineMax,
                       'cysteineMethionineMin': contraintes.cysteineMethionineMin,
                       'cysteineMethionineMax': contraintes.cysteineMethionineMax,
                       'sodiumMin': contraintes.sodiumMin,
                       'sodiumMax': contraintes.sodiumMax,
                       'ratioEnergieProteineMin': contraintes.ratioEnergieProteineMin,
                       'ratioEnergieProteineMax': contraintes.ratioEnergieProteineMax,
                       'ratioCalciumPhosphoreMin': contraintes.ratioCalciumPhosphoreMin,
                       'ratioCalciumPhosphoreMax': contraintes.ratioCalciumPhosphoreMax,
                       'ratioLysineMethionineMin': contraintes.ratioLysineMethionineMin,
                       'ratioLysineMethionineMax': contraintes.ratioLysineMethionineMax}
        print(f"Contraintes obtenues 2 : {contraintes}")
        logger.info(f"Contraintes obtenues 2 : {contraintes}")
    except PhaseDeveloppement.DoesNotExist:
        raise Http404("La tranche d'age spécifiée n'existe pas.")
    except Exception as e:
        print(f"Erreur lors de la récupération des contraintes : {e}")
        logger.error(f"Erreur lors de la récupération des contraintes : {e}")
        raise Http404("Une erreur s'est produite lors de la récupération de la phase de developpement et ses "
                      "contraintes.")
    return JsonResponse(contraintes, safe=False)

# requete pour afficher ingredient

# def ingredient_detail(request, id):
# try:
#     ingredient = ListeIngredients.objects.get(id=id)
# except ListeIngredients.DoesNotExist:
#     raise Http404("Ingredient indisponible")

# ingredient = get_object_or_404(ListeIngredients,
#                                id=id,
#                                ingredient=ListeIngredients.objects.all())
#
# return render(request,
#               'html/test/ingredient_detail.html',
#               {'ingredient_detail': ingredient})
