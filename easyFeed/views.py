from datetime import date, timedelta

import numpy as np
from dateutil.relativedelta import relativedelta
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from .models import ListeIngredients, FormulationDisponible, PhaseDeveloppement, Pays, Ingredient, Client, \
    TypeAbonnement, Abonnement, TypeUtilisateur, Utilisateur
from django.http import Http404, JsonResponse, HttpResponse
import pandas as pd
import json
import logging
from scipy.optimize import minimize

pd.options.display.float_format = '{:,.2f}'.format

# cree un logger (journal d'erreur pour enregistrer les erreurs)
logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'html/home.html', context={})


#
#   Acheter un abonnement
#

def signup(request):
    if request.method == 'POST':
        logger.info('Signup view triggered with POST method')

        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        # telephone = request.POST.get('telephone')
        # ville = request.POST.get('ville')
        # pays = request.POST.get('pays')
        # adresse = request.POST.get('adresse')
        # code_postal = request.POST.get('code_postal')
        password = request.POST['password']

        # Créer une nouvelle instance de Client

        def create_client(nom, prenom, email, password):
            if Client.objects.filter(email=email).exists():
                logger.warning(f'Tentative de création d\'un client avec un email existant : {email}')
                raise ValidationError("Email already exists")
            else:
                client = Client(nom=nom, prenom=prenom, email=email, password=password)
                client.save()

        try:
            client = create_client(nom, prenom, email, password)
            id_client = Client.objects.get(email=email).id
            client = Client.objects.get(id=id_client)

            # Récupérer les données de l'abonnement
            nomAbonnement = request.POST.get('titre')
            type_abonnement = TypeAbonnement.objects.get(titre=nomAbonnement)

            if nomAbonnement == "Mensuel":
                date_fin = date.today() + timedelta(days=30)
            else:
                date_fin = date.today() + timedelta(days=365)

            # Créer une nouvelle instance d'Abonnement
            abonnement = Abonnement(client=client, type_abonnement=type_abonnement, date_debut=date.today(),
                                    date_fin=date_fin)
            abonnement.save()

            result = {'result': 'ok', 'message': 'Inscription réussie'}
            logger.info('Client successfully created and saved')
            return JsonResponse(result, safe=False)
        except ValidationError as ve:
            logger.error(f'ValidationError: {str(ve)}')
            return JsonResponse({'result': 'error', 'message': str(ve)}, safe=False)
        except ObjectDoesNotExist as ode:
            logger.error(f'ObjectDoesNotExist: {str(ode)}')
            return JsonResponse({'result': 'error', 'message': 'Object does not exist: ' + str(ode)}, safe=False)
        except Exception as e:
            logger.error(f'An unexpected error occurred: {str(e)}')
            return JsonResponse({'result': 'error', 'message': 'An unexpected error occurred: ' + str(e)}, safe=False)
    else:
        logger.info('Signup view triggered with GET method')
        return render(request, 'html/signup.html')


#
#   Creer administrateur
#


def create_account(request):
    # print("je suis dans create_account")
    # print(request.POST.get('floating_last_name'))
    if request.method == 'POST':
        # print(request.POST)
        logger.info('Création de compte administrateur view triggered with POST method')
        global counter
        try:
            # print("je suis dans le post")
            # Récupérer les données du formulaire
            code_pays = Pays.objects.get(id=request.POST.get('pays'))
            print(code_pays)
            # id_type_utilisateur = TypeUtilisateur.objects.get(id=request.POST['id_type_utilisateur'])
            id_type_utilisateur = TypeUtilisateur.objects.get(id=1)
            # matricule = request.POST['matricule']
            matricule = 'A1324'
            nom = request.POST['floating_last_name']
            prenom = request.POST['floating_first_name']
            date_naissance = request.POST['floating_birthdate']
            date_embauche = date.today()
            numero_telephone = request.POST['floating_phone']
            adresse = request.POST['floating_company']
            email = request.POST['floating_email']
            # password = request.POST['password']
            password = '1234'

            counter = Utilisateur.objects.count()

            def increment():
                global counter
                counter += 1
                return str(counter).zfill(2)

            matricule += increment()
            print(matricule)

            # Créer une nouvelle instance de Utilisateur
            utilisateur = Utilisateur(
                codePays=code_pays,
                idTypeUtilisateur=id_type_utilisateur,
                matricule=matricule,
                nom=nom,
                prenom=prenom,
                dateNaissance=date_naissance,
                dateEmbauche=date_embauche,
                numeroTelephone=numero_telephone,
                adresse=adresse,
                email=email,
                password=password
            )

            # Sauvegarder l'instance dans la base de données
            utilisateur.save()

            logger.info('Création de compte administrateur réussie')

            result = {'result': 'ok', 'message': 'Création de compte administrateur réussie'}
            # return JsonResponse(result, safe=False)
            return redirect('/login')

        except Exception as e:
            logger.error('Erreur lors de la création du compte administrateur : %s' % e)
            result = {'result': 'error', 'message': 'Erreur lors de la création du compte administrateur : %s' % e}
            return JsonResponse(result, safe=False)

    else:
        logger.info('Affichage du formulaire de création de compte administrateur')
        pays = Pays.objects.all()
        print(pays)
        return render(request, 'html/create_account.html', context={'pays': pays})


def login(request):
    return render(request, 'html/login.html', context={})


def connexion(request):
    logger.info('Connexion view triggered')
    email = request.GET.get('email')
    password = request.GET.get('password')
    utilisateurs = Utilisateur.objects.all()

    # Fonction pour vérifier si le mot de passe en clair correspond au mot de passe haché
    def verify_password(plain_password, hashed_password):
        return check_password(plain_password, hashed_password)

    result = {}

    try:
        utilisateur = Utilisateur.objects.get(email=email)
        password_correspondant = utilisateur.password

        prenomUser = utilisateur.prenom
        nomUser = utilisateur.nom
        request.session['prenom'] = prenomUser
        request.session['nom'] = nomUser

        # is_password_correct = verify_password(password, password_correspondant)°°

        is_password_correct = True
        if is_password_correct:
            result = {'result': 'ok', 'message': 'Connexion réussie','prenom': prenomUser, 'nom': nomUser}
        else:
            result = {'result': 'error', 'message': 'Mot de passe incorrect'}
        logger.info(json.dumps(result))
        return JsonResponse(result, safe=False)
    except ObjectDoesNotExist:
        result = {'result': 'error', 'message': 'Email non trouvé'}
        logger.info(json.dumps(result))
        return JsonResponse(result, safe=False)


def dashboard(request):
    prenom = request.session['prenom']
    nom = request.session['nom']
    return render(request, 'html/dashboard.html', {'prenom': prenom, 'nom': nom})


def formulation(request):
    prenom = request.session['prenom']
    nom = request.session['nom']

    return render(request, 'html/formulation.html', {'prenom': prenom, 'nom': nom})


def formulation_form(request):
    prenom = request.session['prenom']
    nom = request.session['nom']
    return render(request, 'html/formulation_form.html', {'prenom': 'ange', 'nom': nom})


def ingredients(request):
    prenom = request.session['prenom']
    nom = request.session['nom']
    # ListeIngredient
    ingred = ListeIngredients.objects.all()

    print(ingred)
    # liste des ingredients avec leurs nutriments
    liste = {}
    for ingredient in ingred:
        liste = {'ingredient': ingredient.nomIngredient,
                 'proteine': ingredient.proteineBrute,
                 'energie': ingredient.energieMetabolisable,
                 'cellulose': ingredient.celluloseBrute,
                 'phosphore': ingredient.phosphore,
                 'lysine': ingredient.lysine,
                 'calcium': ingredient.calcium,
                 'cysMethionine': ingredient.cysteineMethionine,
                 'methionine': ingredient.methionine,
                 'sodium': ingredient.sodium,
                 'prix': ingredient.prix}

        print(ingredient.nomIngredient)
    return render(request, 'html/ingredients.html', {'liste': ingred, 'prenom': prenom, 'nom': nom})


def formulation_form(request):
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
    return render(request, 'html/formulation_form.html',
                  {'ingredients': ingredients, 'animaux': animaux, 'ages': ages, 'countries': countries, })


# requete pour recuperer tous les ingredients


# def ingredient_test(request):
#     # ListeIngredient
#     ingredients = ListeIngredients.objects.all()
#
#     # FormulationDisponible
#     animaux = FormulationDisponible.objects.all()
#     animaux_data = FormulationDisponible.objects.values('id', 'codeAnimal', 'nomAnimal')
#
#     # PhaseDeveloppement
#     ages = PhaseDeveloppement.objects.all()
#
#     # Pays
#     countries = Pays.objects.all()
#
#     ingredients_df = ListeIngredients.objects.values('proteineBrute', 'energieMetabolisable',
#                                                      'matiereGrasse', 'celluloseBrute', 'calcium',
#                                                      'phosphore',
#                                                      'lysine', 'methionine',
#                                                      'cysteineMethionine',
#                                                      'sodium', 'prix')
#
#     # exemple de conversion en dataFrame
#     # Methode #1 (consomme beaucoup de memoire)
#     df = pd.DataFrame(list(ingredients_df))  # caster ingredient_df en dataFrame
#     # print(df)
#
#     # Methode #2
#     df2 = pd.DataFrame.from_records(ingredients_df)
#     # print(df2)
#
#     return render(request,
#                   'html/test/ingredient_test.html',
#                   {'ingredients': ingredients, 'animaux': animaux, 'ages': ages, 'countries': countries, })


# def details_ingredient(request):
#     ingredient = request.GET.get('ingredient')
#     print(ingredient)
#     try:
#         nutriments = ListeIngredients.objects.get(id=ingredient)
#         print(nutriments.proteineBrute)
#         nutriments = {'proteineBrute': nutriments.proteineBrute,
#                       'energieMetabolisable': nutriments.energieMetabolisable,
#                       'matiereGrasse': nutriments.matiereGrasse,
#                       'celluloseBrute': nutriments.celluloseBrute, 'calcium': nutriments.calcium,
#                       'phosphore': nutriments.phosphore,
#                       'lysine': nutriments.lysine, 'methionine': nutriments.methionine,
#                       'cysteineMethionine': nutriments.cysteineMethionine,
#                       'sodium': nutriments.sodium}
#         print(nutriments)
#     except ListeIngredients.DoesNotExist:
#         raise Http404("L'ingredient spécifié n'existe pas.")
#     except Exception as e:
#         raise Http404("Une erreur s'est produite lors de la récupération des nutriments.")
#
#     return JsonResponse(nutriments, safe=False)


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
        # print(contraintes.lysineMin)

        #
        #   convertion des contraintes en dataFrame
        #

        phase = contraintes

        # Initialiser les dictionnaires pour min et max
        min_dict = {}
        max_dict = {}

        # Remplir les dictionnaires avec les valeurs des contraintes
        min_dict = {
            'proteineBrute': phase.proteineBruteMin,
            'energieMetabolisable': phase.energieMetabolisableMin,
            'matiereGrasse': phase.matiereGrasseMin,
            'calcium': phase.calciumMin,
            'phosphore': phase.phosphoreMin,
            'lysine': phase.lysineMin,
            'methionine': phase.methionineMin,
            'cysteineMethionine': phase.cysteineMethionineMin,
            'sodium': phase.sodiumMin,
        }

        max_dict = {
            'proteineBrute': phase.proteineBruteMax,
            'energieMetabolisable': phase.energieMetabolisableMax,
            'matiereGrasse': phase.matiereGrasseMax,
            'calcium': phase.calciumMax,
            'phosphore': phase.phosphoreMax,
            'lysine': phase.lysineMax,
            'methionine': phase.methionineMax,
            'cysteineMethionine': phase.cysteineMethionineMax,
            'sodium': phase.sodiumMax,
        }

        # Convertir les dictionnaires en DataFrames
        min_df = pd.DataFrame(min_dict, index=['min'])
        max_df = pd.DataFrame(max_dict, index=['max'])

        # Concaténer les deux DataFrames
        contraintes_df = pd.concat([min_df, max_df])

        # Initialiser les dictionnaires pour min et max pour les ratios
        min_ratio_dict = {}
        max_ratio_dict = {}

        # Remplir les dictionnaires avec les valeurs des contraintes
        min_ratio_dict = {
            'ratioEnergieProteine': phase.ratioEnergieProteineMin,
            'ratioCalciumPhosphore': phase.ratioCalciumPhosphoreMin,
            'ratioLysineMethionine': phase.ratioLysineMethionineMin
        }

        max_ratio_dict = {
            'ratioEnergieProteine': phase.ratioEnergieProteineMax,
            'ratioCalciumPhosphore': phase.ratioCalciumPhosphoreMax,
            'ratioLysineMethionine': phase.ratioLysineMethionineMax
        }

        # Convertir les dictionnaires en DataFrames
        min_ratio_df = pd.DataFrame(min_ratio_dict, index=['min'])
        max_ratio_df = pd.DataFrame(max_ratio_dict, index=['max'])

        # Concaténer les deux DataFrames
        contraintes_ratio_df = pd.concat([min_ratio_df, max_ratio_df])

        # Ajouter des instructions d'impression et de journalisation après avoir obtenu les contraintes
        # print(f"Contraintes obtenues : {contraintes}")
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
        # print(f"Contraintes obtenues 2 : {contraintes}")
        logger.info(f"Contraintes obtenues 2 : {contraintes}")
    except PhaseDeveloppement.DoesNotExist:
        raise Http404("La tranche d'age spécifiée n'existe pas.")
    except Exception as e:
        print(f"Erreur lors de la récupération des contraintes : {e}")
        logger.error(f"Erreur lors de la récupération des contraintes : {e}")
        raise Http404("Une erreur s'est produite lors de la récupération de la phase de developpement et ses "
                      "contraintes.")
    return JsonResponse(contraintes, safe=False)


#
#   Algoritthme de formulation
#

def optimize(request):
    global ingredients_utilises_bool, quantite, ing_utilises, total_nutriments, nom_nutriments, valeur_nutriments, valeur_ratio_em_p, valeur_ratio_ca_p, valeur_ratio_lys_meth, min_ratio_list, max_ratio_list, nom_ratio_list, min_list, max_list, nom_list
    id_phase = request.GET.get('id_phase')
    mode = request.GET.get('mode')
    if not id_phase:
        return JsonResponse({"error": "id_phase parameter is missing"}, status=400)
    logger.info(f"ID de phase reçu : {id_phase}")
    if (mode == 'auto'):

        try:
            contraintes = PhaseDeveloppement.objects.get(id=id_phase)
            print(id_phase)

            #
            #   convertion des contraintes en dataFrame
            #

            phase = contraintes

            # Initialiser les dictionnaires pour min et max
            min_dict = {}
            max_dict = {}

            # Remplir les dictionnaires avec les valeurs des contraintes
            min_dict = {
                'proteineBrute': phase.proteineBruteMin,
                'energieMetabolisable': phase.energieMetabolisableMin,
                'matiereGrasse': phase.matiereGrasseMin,
                'calcium': phase.calciumMin,
                'phosphore': phase.phosphoreMin,
                'lysine': phase.lysineMin,
                'methionine': phase.methionineMin,
                'cysteineMethionine': phase.cysteineMethionineMin,
                'sodium': phase.sodiumMin,
            }

            max_dict = {
                'proteineBrute': phase.proteineBruteMax,
                'energieMetabolisable': phase.energieMetabolisableMax,
                'matiereGrasse': phase.matiereGrasseMax,
                'calcium': phase.calciumMax,
                'phosphore': phase.phosphoreMax,
                'lysine': phase.lysineMax,
                'methionine': phase.methionineMax,
                'cysteineMethionine': phase.cysteineMethionineMax,
                'sodium': phase.sodiumMax,
            }

            # Convertir les dictionnaires en DataFrames
            min_df = pd.DataFrame(min_dict, index=['min'])
            max_df = pd.DataFrame(max_dict, index=['max'])

            # Concaténer les deux DataFrames
            contraintes_df = pd.concat([min_df, max_df])
            print(f"Contraintes obtenues : {contraintes_df}")

            # Initialiser les dictionnaires pour min et max pour les ratios
            min_ratio_dict = {}
            max_ratio_dict = {}

            # Remplir les dictionnaires avec les valeurs des contraintes
            min_ratio_dict = {
                'ratioEnergieProteine': phase.ratioEnergieProteineMin,
                'ratioCalciumPhosphore': phase.ratioCalciumPhosphoreMin,
                'ratioLysineMethionine': phase.ratioLysineMethionineMin
            }

            max_ratio_dict = {
                'ratioEnergieProteine': phase.ratioEnergieProteineMax,
                'ratioCalciumPhosphore': phase.ratioCalciumPhosphoreMax,
                'ratioLysineMethionine': phase.ratioLysineMethionineMax
            }

            # Convertir les dictionnaires en DataFrames
            min_ratio_df = pd.DataFrame(min_ratio_dict, index=['min'])
            max_ratio_df = pd.DataFrame(max_ratio_dict, index=['max'])

            # Concaténer les deux DataFrames
            contraintes_ratio_df = pd.concat([min_ratio_df, max_ratio_df])

            # Ajouter des instructions d'impression et de journalisation après avoir obtenu les contraintes
            print(f"Contraintes obtenues : {contraintes_df}")
            print(f"Contraintes_ratio obtenues : {contraintes_ratio_df}")
            logger.info(f"Contraintes obtenues : {contraintes}")

            code_pays = request.GET.get('code_pays')
            if not code_pays:
                return JsonResponse({"error": "code_pays parameter is missing"}, status=400)
            logger.info(f"Code pays reçu : {code_pays}")
        except PhaseDeveloppement.DoesNotExist:
            logger.error("La tranche d'age spécifiée n'existe pas.")
            raise Http404("La tranche d'age spécifiée n'existe pas.")
        except Exception as e:
            print(f"Erreur lors de la récupération des contraintes : {e}")
            logger.error(f"Erreur lors de la récupération des contraintes : {e}")
            raise Http404("Une erreur s'est produite lors de la récupération de la phase de developpement et ses "
                          "contraintes.")

        try:
            ing_pays = Ingredient.objects.filter(codePays__codePays=code_pays)
            ingredients = []
            for ing in ing_pays:
                ingredient_dict = {
                    'nomIngredient': ing.codeIngredient.nomIngredient,
                    'proteineBrute': ing.codeIngredient.proteineBrute,
                    'energieMetabolisable': ing.codeIngredient.energieMetabolisable,
                    'matiereGrasse': ing.codeIngredient.matiereGrasse,
                    'celluloseBrute': ing.codeIngredient.celluloseBrute,
                    'calcium': ing.codeIngredient.calcium,
                    'phosphore': ing.codeIngredient.phosphore,
                    'lysine': ing.codeIngredient.lysine,
                    'methionine': ing.codeIngredient.methionine,
                    'cysteineMethionine': ing.codeIngredient.cysteineMethionine,
                    'sodium': ing.codeIngredient.sodium,
                    'prix': ing.codeIngredient.prix
                }
                ingredients.append(ingredient_dict)

            # Convertir la liste de dictionnaires en DataFrame
            data_df = pd.DataFrame(ingredients)
            print(f"liste_data: {data_df}")
            data_df.set_index('nomIngredient', inplace=True)

            # Obtenir l'index de l'ingrédient 'Sel iodé'
            index_sel_iode = data_df.index.get_loc('Sel iodé')
            index_premix_05 = data_df.index.get_loc('Prémix 0.5%')
            index_premix_25 = data_df.index.get_loc('prémix 2.5%')
            index_premix_2 = data_df.index.get_loc('Prémix 2 %')
            index_ble = data_df.index.get_loc('Blé')
            print(f"Index de l'ingrédient 'Sel iodé' : {index_sel_iode}")

            # liste des ingredients
            ingredient_list = data_df.index.tolist()

            # extraire le prix de chaque ingredient
            prix = data_df['prix']

            # enlever la colonne du prix
            ingredients_df = data_df.drop("prix", axis=1)

            print(f"liste_data: {data_df}")
            print(f" {prix}")
        except Ingredient.DoesNotExist:
            logger.error("Le pays spécifié n'existe pas ou n'a pas d'ingrédients associés.")
            raise Http404("Le pays spécifié n'existe pas ou n'a pas d'ingrédients associés.")
        except Exception as e:
            logger.error(f"Une erreur s'est produite lors de la récupération des ingrédients : {e}")
            raise Http404("Une erreur s'est produite lors de la récupération des ingrédients.")

        # Définir les contraintes d'inéquations
        try:
            n = len(ingredients_df)
            X0 = np.array([1] * n)

            df = data_df

            def objectif(X):
                return (np.sum(X * df["prix"]))

            def cons_Prot_inf(X):
                return np.sum(X * df["proteineBrute"]) - contraintes_df.loc["min", "proteineBrute"]

            def cons_Prot_sup(X):
                return contraintes_df.loc["max", "proteineBrute"] - np.sum(X * df["proteineBrute"])

            def cons_EM_inf(X):
                return np.sum(X * df["energieMetabolisable"]) - contraintes_df.loc["min", "energieMetabolisable"]

            def cons_EM_sup(X):
                return contraintes_df.loc["max", "energieMetabolisable"] - np.sum(X * df["energieMetabolisable"])

            def cons_Ca_inf(X):
                return np.sum(X * df["calcium"]) - contraintes_df.loc["min", "calcium"]

            def cons_Ca_sup(X):
                return contraintes_df.loc["max", "calcium"] - np.sum(X * df["calcium"])

            def cons_P_inf(X):
                return np.sum(X * df["phosphore"]) - contraintes_df.loc["min", "phosphore"]

            def cons_P_sup(X):
                return contraintes_df.loc["max", "phosphore"] - np.sum(X * df["phosphore"])

            def cons_Lys_inf(X):
                return np.sum(X * df["lysine"]) - contraintes_df.loc["min", "lysine"]

            def cons_Lys_sup(X):
                return contraintes_df.loc["max", "lysine"] - np.sum(X * df["lysine"])

            def cons_Meth_inf(X):
                return np.sum(X * df["methionine"]) - contraintes_df.loc["min", "lysine"]

            def cons_Meth_sup(X):
                return contraintes_df.loc["max", "methionine"] - np.sum(X * df["methionine"])

            def cons_Cys_Meth_inf(X):
                return np.sum(X * df["cysteineMethionine"]) - contraintes_df.loc["min", "cysteineMethionine"]

            def cons_Cys_Meth_sup(X):
                return contraintes_df.loc["max", "cysteineMethionine"] - np.sum(X * df["cysteineMethionine"])

            def cons_Na_inf(X):
                return np.sum(X * df["sodium"]) - contraintes_df.loc["min", "sodium"]

            def cons_Na_sup(X):
                return contraintes_df.loc["max", "sodium"] - np.sum(X * df["sodium"])

            def cons_ratio_EM_Prot_inf(X):
                return np.sum(X * df["energieMetabolisable"]) - contraintes_ratio_df.loc[
                    "min", "ratioEnergieProteine"] * np.sum(X * df["proteineBrute"])

            def cons_ratio_EM_Prot_sup(X):
                return contraintes_ratio_df.loc["max", "ratioEnergieProteine"] * np.sum(
                    X * df["proteineBrute"]) - np.sum(
                    X * df["energieMetabolisable"])

            def cons_ratio_Ca_Prot_inf(X):
                return np.sum(X * df["calcium"]) - contraintes_ratio_df.loc["min", "ratioCalciumPhosphore"] * np.sum(
                    X * df["phosphore"])

            def cons_ratio_Ca_Prot_sup(X):
                return contraintes_ratio_df.loc["max", "ratioCalciumPhosphore"] * np.sum(X * df["phosphore"]) - np.sum(
                    X * df["calcium"])

            def cons_ratio_Lys_Meth_inf(X):
                return np.sum(X * df["lysine"]) - contraintes_ratio_df.loc["min", "ratioLysineMethionine"] * np.sum(
                    X * df["methionine"])

            def cons_ratio_Lys_Meth_sup(X):
                return contraintes_ratio_df.loc["max", "ratioLysineMethionine"] * np.sum(X * df["methionine"]) - np.sum(
                    X * df["lysine"])

            # Define the constraint for 'sel iode'
            def cons_Sel_Iode(X):
                return 0.01 - X[index_sel_iode]

            # Define the constraint for 'premix 0.5%'
            def cons_premix_05(X):
                return 0.5 - X[index_premix_05]

            # Define the constraint for 'premix 2.5%'
            def cons_premix_25(X):
                return 2.5 - X[index_premix_25]

            # Define the constraint for 'premix 2%'
            def cons_premix_2(X):
                return 2 - X[index_premix_2]

            # Define the constraint for 'ble'
            def cons_ble(X):
                return 0 - X[index_ble]

            qte_ingredients = 2

            def cons_total(X):
                return np.sum(X) - qte_ingredients  # definir la quantité totale de mélange souhaitée

            cons1 = {"type": "ineq", "fun": cons_Prot_inf}
            cons2 = {"type": "ineq", "fun": cons_Prot_sup}
            cons3 = {"type": "ineq", "fun": cons_EM_inf}
            cons4 = {"type": "ineq", "fun": cons_EM_sup}
            cons5 = {"type": "ineq", "fun": cons_ratio_EM_Prot_inf}
            cons6 = {"type": "ineq", "fun": cons_ratio_EM_Prot_sup}
            cons7 = {"type": "ineq", "fun": cons_Ca_inf}
            cons8 = {"type": "ineq", "fun": cons_Ca_sup}
            cons9 = {"type": "ineq", "fun": cons_ratio_Ca_Prot_inf}
            cons10 = {"type": "ineq", "fun": cons_ratio_Ca_Prot_sup}
            cons11 = {"type": "ineq", "fun": cons_P_inf}
            cons12 = {"type": "ineq", "fun": cons_P_sup}
            cons13 = {"type": "ineq", "fun": cons_Lys_inf}
            cons14 = {"type": "ineq", "fun": cons_Lys_sup}
            cons15 = {"type": "ineq", "fun": cons_Meth_inf}
            cons16 = {"type": "ineq", "fun": cons_Meth_sup}
            cons17 = {"type": "ineq", "fun": cons_Cys_Meth_inf}
            cons18 = {"type": "ineq", "fun": cons_Cys_Meth_sup}
            cons19 = {"type": "ineq", "fun": cons_Na_inf}
            cons20 = {"type": "ineq", "fun": cons_Na_sup}
            cons21 = {"type": "ineq", "fun": cons_ratio_Lys_Meth_inf}
            cons22 = {"type": "ineq", "fun": cons_ratio_Lys_Meth_sup}
            cons23 = {"type": "eq", "fun": cons_total}
            cons24 = {"type": "ineq", "fun": cons_Sel_Iode}
            cons25 = {"type": "ineq", "fun": cons_premix_05}
            cons26 = {"type": "ineq", "fun": cons_premix_25}
            cons27 = {"type": "ineq", "fun": cons_premix_2}
            cons28 = {"type": "eq", "fun": cons_ble}

            b = (0, None)
            bnds = [b] * n

            contraintes_list = [cons1, cons2, cons3, cons4, cons5, cons6, cons7, cons8, cons9, cons10, cons11, cons12,
                                cons13, cons14, cons15, cons16, cons17, cons18, cons19, cons20, cons21, cons22, cons23,
                                cons24, cons25, cons26, cons27, cons28]

            # Appel de la fonction minimize pour l'optimisation
            solution = minimize(objectif, X0, bounds=bnds, constraints=contraintes_list, method='SLSQP')

            # Calculer la somme des quantités des ingrédients
            s_t = np.sum(solution.x)

            # Vérifier si la somme est égale à 1
            if s_t != 1:
                solution.x = solution.x / s_t

            # Maintenant, la somme des valeurs dans x devrait être égale à 1
            assert np.isclose(np.sum(solution.x), 1), "La somme des quantités des ingrédients doit être égale à 1"

            # Parcourir le vecteur de solution et mettre à zéro les quantités inférieures à 0.001 kg (1g)
            solution.x = [x if x >= 0.001 else 0 for x in solution.x]
            # Filtrer les valeurs de solution.x qui ne sont pas égales à zéro
            filtered_solution_x = [x for x in solution.x if x != 0]

            # Afficher filtered_solution_x
            print(filtered_solution_x)
            # solution.x = [i for i, x in enumerate(solution.x) if x >= 0.001]
            #
            # # Obtenir les indices des éléments de solution.x qui sont égaux à zéro
            # zero_indices = [i for i, x in enumerate(solution.x) if x == 0]
            #
            # # Filtrer les ingrédients correspondant aux indices zéro
            # filtered_ingredients = [ingredient for i, ingredient in enumerate(ingredients_df) if i not in zero_indices]

            # Recalculer le coût total
            total_cost = sum(x * p for x, p in zip(solution.x, prix))
            print(f"Coût total : {total_cost}")

            # Vérification de la réussite de l'optimisation
            if solution.success:
                print(f"L'optimisation a réussi. Message : {solution.message}")
                print(f"Valeur minimale de la fonction objectif : {solution.fun}")
                print(f"Point qui minimise la fonction objectif : {solution.x}")
            else:
                print(f"L'optimisation a échoué. Message : {solution.message}")
                print(f"Point qui minimise la fonction objectif : {solution.x}")
                print(f"Valeur minimale de la fonction objectif : {solution.fun}")
                quantite = pd.Series(solution.x)
                quantite.index = ingredients_df.index
                ingredients_utilises_bool = quantite > 0

                # utilisation de la comprehension de liste pour obtenir les ingrédients utilisés
                ing_utilises = [x for x in quantite[ingredients_utilises_bool].index]
                print("Quantité des ingrédients en kg pour 100 kg de mélange :")
                print(quantite[ingredients_utilises_bool])
                print()

                # total_nutriments = np.matmul(np.transpose(ingredients_df), quantite)
                valeur_nutriments = [x for x in np.matmul(np.transpose(ingredients_df), quantite)]
                nom_nutriments = [x for x in np.matmul(np.transpose(ingredients_df), quantite).index]

                valeur_ratio_em_p = np.sum(ingredients_df["energieMetabolisable"] * quantite) / np.sum(
                    ingredients_df["proteineBrute"] * quantite)
                valeur_ratio_ca_p = np.sum(ingredients_df["calcium"] * quantite) / np.sum(
                    ingredients_df["phosphore"] * quantite)
                valeur_ratio_lys_meth = np.sum(ingredients_df["lysine"] * quantite) / np.sum(
                    ingredients_df["methionine"] * quantite)

                # print("Valeur des ratios")
                # print("Ratio EM/Protéine: {:.2f}".format(valeur_ratio_em_p))
                # print("Ratio Ca/P: {:.2f}".format(valeur_ratio_ca_p))
                # print("Ratio Lys/Meth: {:.2f}".format(valeur_ratio_lys_meth))
                # print()

                min_ratio_list = list(min_ratio_dict.values())
                max_ratio_list = list(max_ratio_dict.values())
                nom_ratio_list = list(min_ratio_dict)

                min_list = list(min_dict.values())
                max_list = list(max_dict.values())
                nom_list = list(min_dict)

                # print()
                # print("resultat")
                # print(quantite[ingredients_utilises_bool].index)
                # print([x for x in quantite[ingredients_utilises_bool].index])
                # print()

            # Créer un dictionnaire pour stocker les informations de la solution
            solution_dict = {
                'success': bool(solution.success),  # Convertir en booléen (python natif) pour la sérialisation JSON
                'message': solution.message,
                'fun': solution.fun,
                'x': filtered_solution_x,  # Convertir le tableau numpy en liste pour la sérialisation JSON
                'ing': ing_utilises,
                'pt': total_cost,
                'nutri': nom_nutriments,
                'v_nutri': valeur_nutriments,
                'ratioEMProt': valeur_ratio_em_p,
                'ratioCaP': valeur_ratio_ca_p,
                'ratioLysMeth': valeur_ratio_lys_meth,
                'min_ratio': min_ratio_list,
                'max_ratio': max_ratio_list,
                'nom_ratio': nom_ratio_list,
                'min_nutri': min_list,
                'max_nutri': max_list,
                'nom_nutri': nom_list
            }
            logger.info(f"optimisation : {solution_dict}")
            # Renvoyer la solution sous forme de réponse JSON
            return JsonResponse(solution_dict, safe=False)
        except Exception as e:
            logger.error(f"Une erreur s'est produite lors du calcul d'optimisation : {e}")
            raise Http404("Une erreur s'est produite lors du calcul d'optimisation.")
    else:
        ############################ MODE MANUEL ##########################################################
        try:
            contraintes = PhaseDeveloppement.objects.get(id=id_phase)
            print(id_phase)

            #
            #   convertion des contraintes en dataFrame
            #

            phase = contraintes

            # Initialiser les dictionnaires pour min et max
            min_dict = {}
            max_dict = {}

            # Remplir les dictionnaires avec les valeurs des contraintes
            min_dict = {
                'proteineBrute': phase.proteineBruteMin,
                'energieMetabolisable': phase.energieMetabolisableMin,
                'matiereGrasse': phase.matiereGrasseMin,
                'calcium': phase.calciumMin,
                'phosphore': phase.phosphoreMin,
                'lysine': phase.lysineMin,
                'methionine': phase.methionineMin,
                'cysteineMethionine': phase.cysteineMethionineMin,
                'sodium': phase.sodiumMin,
            }

            max_dict = {
                'proteineBrute': phase.proteineBruteMax,
                'energieMetabolisable': phase.energieMetabolisableMax,
                'matiereGrasse': phase.matiereGrasseMax,
                'calcium': phase.calciumMax,
                'phosphore': phase.phosphoreMax,
                'lysine': phase.lysineMax,
                'methionine': phase.methionineMax,
                'cysteineMethionine': phase.cysteineMethionineMax,
                'sodium': phase.sodiumMax,
            }

            # Convertir les dictionnaires en DataFrames
            min_df = pd.DataFrame(min_dict, index=['min'])
            max_df = pd.DataFrame(max_dict, index=['max'])

            # Concaténer les deux DataFrames
            contraintes_df = pd.concat([min_df, max_df])
            print(f"Contraintes obtenues : {contraintes_df}")

            # Initialiser les dictionnaires pour min et max pour les ratios
            min_ratio_dict = {}
            max_ratio_dict = {}

            # Remplir les dictionnaires avec les valeurs des contraintes
            min_ratio_dict = {
                'ratioEnergieProteine': phase.ratioEnergieProteineMin,
                'ratioCalciumPhosphore': phase.ratioCalciumPhosphoreMin,
                'ratioLysineMethionine': phase.ratioLysineMethionineMin
            }

            max_ratio_dict = {
                'ratioEnergieProteine': phase.ratioEnergieProteineMax,
                'ratioCalciumPhosphore': phase.ratioCalciumPhosphoreMax,
                'ratioLysineMethionine': phase.ratioLysineMethionineMax
            }

            # Convertir les dictionnaires en DataFrames
            min_ratio_df = pd.DataFrame(min_ratio_dict, index=['min'])
            max_ratio_df = pd.DataFrame(max_ratio_dict, index=['max'])

            # Concaténer les deux DataFrames
            contraintes_ratio_df = pd.concat([min_ratio_df, max_ratio_df])

            # Ajouter des instructions d'impression et de journalisation après avoir obtenu les contraintes
            print(f"Contraintes obtenues : {contraintes_df}")
            print(f"Contraintes_ratio obtenues : {contraintes_ratio_df}")
            logger.info(f"Contraintes obtenues : {contraintes}")

            code_pays = request.GET.get('code_pays')
            if not code_pays:
                return JsonResponse({"error": "code_pays parameter is missing"}, status=400)
            logger.info(f"Code pays reçu : {code_pays}")
        except PhaseDeveloppement.DoesNotExist:
            logger.error("La tranche d'age spécifiée n'existe pas.")
            raise Http404("La tranche d'age spécifiée n'existe pas.")
        except Exception as e:
            print(f"Erreur lors de la récupération des contraintes : {e}")
            logger.error(f"Erreur lors de la récupération des contraintes : {e}")
            raise Http404("Une erreur s'est produite lors de la récupération de la phase de developpement et ses "
                          "contraintes.")

        try:
            ing_pays = Ingredient.objects.filter(codePays__codePays=code_pays)
            ingredients = []
            for ing in ing_pays:
                ingredient_dict = {
                    'nomIngredient': ing.codeIngredient.nomIngredient,
                    'proteineBrute': ing.codeIngredient.proteineBrute,
                    'energieMetabolisable': ing.codeIngredient.energieMetabolisable,
                    'matiereGrasse': ing.codeIngredient.matiereGrasse,
                    'celluloseBrute': ing.codeIngredient.celluloseBrute,
                    'calcium': ing.codeIngredient.calcium,
                    'phosphore': ing.codeIngredient.phosphore,
                    'lysine': ing.codeIngredient.lysine,
                    'methionine': ing.codeIngredient.methionine,
                    'cysteineMethionine': ing.codeIngredient.cysteineMethionine,
                    'sodium': ing.codeIngredient.sodium,
                    'prix': ing.codeIngredient.prix
                }
                ingredients.append(ingredient_dict)

            # Convertir la liste de dictionnaires en DataFrame
            data_df = pd.DataFrame(ingredients)
            data_df.set_index('nomIngredient', inplace=True)

            # liste des ingredients
            ingredient_list = data_df.index.tolist()

            # extraire le prix de chaque ingredient
            prix = data_df['prix']

            # enlever la colonne du prix
            ingredients_df = data_df.drop("prix", axis=1)

            print(f"liste_data: {data_df}")
            print(f" {prix}")
        except Ingredient.DoesNotExist:
            logger.error("Le pays spécifié n'existe pas ou n'a pas d'ingrédients associés.")
            raise Http404("Le pays spécifié n'existe pas ou n'a pas d'ingrédients associés.")
        except Exception as e:
            logger.error(f"Une erreur s'est produite lors de la récupération des ingrédients : {e}")
            raise Http404("Une erreur s'est produite lors de la récupération des ingrédients.")

        # Définir les contraintes d'inéquations
        try:
            # n = len(ingredients_df)
            # X0 = np.array([1] * n)
            #
            # df = data_df

            def objectif(X):
                return (np.sum(X * df["prix"]))

            def cons_Prot_inf(X):
                return np.sum(X * df["proteineBrute"]) - contraintes_df.loc["min", "proteineBrute"]

            def cons_Prot_sup(X):
                return contraintes_df.loc["max", "proteineBrute"] - np.sum(X * df["proteineBrute"])

            def cons_EM_inf(X):
                return np.sum(X * df["energieMetabolisable"]) - contraintes_df.loc["min", "energieMetabolisable"]

            def cons_EM_sup(X):
                return contraintes_df.loc["max", "energieMetabolisable"] - np.sum(X * df["energieMetabolisable"])

            def cons_Ca_inf(X):
                return np.sum(X * df["calcium"]) - contraintes_df.loc["min", "calcium"]

            def cons_Ca_sup(X):
                return contraintes_df.loc["max", "calcium"] - np.sum(X * df["calcium"])

            def cons_P_inf(X):
                return np.sum(X * df["phosphore"]) - contraintes_df.loc["min", "phosphore"]

            def cons_P_sup(X):
                return contraintes_df.loc["max", "phosphore"] - np.sum(X * df["phosphore"])

            def cons_Lys_inf(X):
                return np.sum(X * df["lysine"]) - contraintes_df.loc["min", "lysine"]

            def cons_Lys_sup(X):
                return contraintes_df.loc["max", "lysine"] - np.sum(X * df["lysine"])

            def cons_Meth_inf(X):
                return np.sum(X * df["methionine"]) - contraintes_df.loc["min", "lysine"]

            def cons_Meth_sup(X):
                return contraintes_df.loc["max", "methionine"] - np.sum(X * df["methionine"])

            def cons_Cys_Meth_inf(X):
                return np.sum(X * df["cysteineMethionine"]) - contraintes_df.loc["min", "cysteineMethionine"]

            def cons_Cys_Meth_sup(X):
                return contraintes_df.loc["max", "cysteineMethionine"] - np.sum(X * df["cysteineMethionine"])

            def cons_Na_inf(X):
                return np.sum(X * df["sodium"]) - contraintes_df.loc["min", "sodium"]

            def cons_Na_sup(X):
                return contraintes_df.loc["max", "sodium"] - np.sum(X * df["sodium"])

            def cons_ratio_EM_Prot_inf(X):
                return np.sum(X * df["energieMetabolisable"]) - contraintes_ratio_df.loc[
                    "min", "ratioEnergieProteine"] * np.sum(X * df["proteineBrute"])

            def cons_ratio_EM_Prot_sup(X):
                return contraintes_ratio_df.loc["max", "ratioEnergieProteine"] * np.sum(
                    X * df["proteineBrute"]) - np.sum(
                    X * df["energieMetabolisable"])

            def cons_ratio_Ca_Prot_inf(X):
                return np.sum(X * df["calcium"]) - contraintes_ratio_df.loc[
                    "min", "ratioCalciumPhosphore"] * np.sum(
                    X * df["phosphore"])

            def cons_ratio_Ca_Prot_sup(X):
                return contraintes_ratio_df.loc["max", "ratioCalciumPhosphore"] * np.sum(
                    X * df["phosphore"]) - np.sum(
                    X * df["calcium"])

            def cons_ratio_Lys_Meth_inf(X):
                return np.sum(X * df["lysine"]) - contraintes_ratio_df.loc["min", "ratioLysineMethionine"] * np.sum(
                    X * df["methionine"])

            def cons_ratio_Lys_Meth_sup(X):
                return contraintes_ratio_df.loc["max", "ratioLysineMethionine"] * np.sum(
                    X * df["methionine"]) - np.sum(
                    X * df["lysine"])

            qte_ingredients = 1

            def cons_total(X):
                return np.sum(X) - qte_ingredients  # definir la quantité totale de mélange souhaitée

            cons1 = {"type": "ineq", "fun": cons_Prot_inf}
            cons2 = {"type": "ineq", "fun": cons_Prot_sup}
            cons3 = {"type": "ineq", "fun": cons_EM_inf}
            cons4 = {"type": "ineq", "fun": cons_EM_sup}
            cons5 = {"type": "ineq", "fun": cons_ratio_EM_Prot_inf}
            cons6 = {"type": "ineq", "fun": cons_ratio_EM_Prot_sup}
            cons7 = {"type": "ineq", "fun": cons_Ca_inf}
            cons8 = {"type": "ineq", "fun": cons_Ca_sup}
            cons9 = {"type": "ineq", "fun": cons_ratio_Ca_Prot_inf}
            cons10 = {"type": "ineq", "fun": cons_ratio_Ca_Prot_sup}
            cons11 = {"type": "ineq", "fun": cons_P_inf}
            cons12 = {"type": "ineq", "fun": cons_P_sup}
            cons13 = {"type": "ineq", "fun": cons_Lys_inf}
            cons14 = {"type": "ineq", "fun": cons_Lys_sup}
            cons15 = {"type": "ineq", "fun": cons_Meth_inf}
            cons16 = {"type": "ineq", "fun": cons_Meth_sup}
            cons17 = {"type": "ineq", "fun": cons_Cys_Meth_inf}
            cons18 = {"type": "ineq", "fun": cons_Cys_Meth_sup}
            cons19 = {"type": "ineq", "fun": cons_Na_inf}
            cons20 = {"type": "ineq", "fun": cons_Na_sup}
            cons21 = {"type": "ineq", "fun": cons_ratio_Lys_Meth_inf}
            cons22 = {"type": "ineq", "fun": cons_ratio_Lys_Meth_sup}
            cons23 = {"type": "eq", "fun": cons_total}

            b = (0, None)
            bnds = [b] * n

            contraintes_list = [cons1, cons2, cons3, cons4, cons5, cons6, cons7, cons8, cons9, cons10, cons11,
                                cons12,
                                cons13, cons14, cons15, cons16, cons17, cons18, cons19, cons20, cons21, cons22,
                                cons23]

            # Appel de la fonction minimize pour l'optimisation
            solution = minimize(objectif, X0, bounds=bnds, constraints=contraintes_list, method='SLSQP')

            # Parcourir le vecteur de solution et mettre à zéro les quantités inférieures à 0.001 kg (1g)
            solution.x = [x if x >= 0.001 else 0 for x in solution.x]
            # Filtrer les valeurs de solution.x qui ne sont pas égales à zéro
            filtered_solution_x = [x for x in solution.x if x != 0]

            # Afficher filtered_solution_x
            print(filtered_solution_x)
            # solution.x = [i for i, x in enumerate(solution.x) if x >= 0.001]

            # Obtenir les indices des éléments de solution.x qui sont égaux à zéro
            # zero_indices = [i for i, x in enumerate(solution.x) if x == 0]

            # Filtrer les ingrédients correspondant aux indices zéro
            # filtered_ingredients = [ingredient for i, ingredient in enumerate(ingredients_df) if i not in zero_indices]

            # Recalculer le coût total
            total_cost = sum(x * p for x, p in zip(solution.x, prix))

            # Vérification de la réussite de l'optimisation
            if solution.success:
                print(f"L'optimisation a réussi. Message : {solution.message}")
                print(f"Valeur minimale de la fonction objectif : {solution.fun}")
                print(f"Point qui minimise la fonction objectif : {solution.x}")
            else:
                print(f"L'optimisation a échoué. Message : {solution.message}")
                print(f"Point qui minimise la fonction objectif : {solution.x}")
                print(f"Valeur minimale de la fonction objectif : {solution.fun}")
                quantite = pd.Series(solution.x)
                quantite.index = ingredients_df.index

                ingredients_utilises_bool = quantite > 0
                print("Quantité des ingrédients en kg pour 100 kg de mélange :")
                print(quantite[ingredients_utilises_bool])
                print()

            # Créer un dictionnaire pour stocker les informations de la solution
            solution_dict = {
                'success': bool(solution.success),  # Convertir en booléen (python natif) pour la sérialisation JSON
                'message': solution.message,
                'fun': solution.fun,
                'x': filtered_solution_x  # Convertir le tableau numpy en liste pour la sérialisation JSON
            }
            logger.info(f"optimisation : {solution_dict}")
            # Renvoyer la solution sous forme de réponse JSON
            return JsonResponse(solution_dict, safe=False)
        except Exception as e:
            logger.error(f"Une erreur s'est produite lors du calcul d'optimisation : {e}")
            raise Http404("Une erreur s'est produite lors du calcul d'optimisation.")


#
#   Mode manuel
#

def manual_optimize(request):
    ingredients = ListeIngredients.objects.all()
    full_liste_ingredients = []
    ingredient_dict = {}
    for ing in ingredients:
        ingredient_dict = {
            'nomIngredient': ing.nomIngredient
        }
        full_liste_ingredients.append(ingredient_dict)

    return JsonResponse(ingredient_dict, safe=False)

    # try:
    #     # Liste des nutriments et des ratios
    #     nutriments = contraintes_df.columns
    #     ratios = contraintes_ratio_df.columns
    #
    #     # Liste pour stocker les contraintes
    #     contraintes_list = []
    #
    #     # Solution initiale
    #     n = len(data_df)
    #     X0 = np.array([1] * n)
    #
    #     # Fonction objective
    #     objectif = lambda X: (X * prix).sum()
    #
    #     # Créer des contraintes pour chaque nutriment
    #     def create_min_constraint(nom):
    #         return lambda X: np.sum(X * data_df[nom]) - contraintes_df.loc["min", nom]
    #
    #     def create_max_constraint(nom):
    #         return lambda X: contraintes_df.loc["max", nom] - np.sum(X * data_df[nom])
    #
    #     for nom in nutriments:
    #         contraintes_list.append({"type": "ineq", "fun": create_min_constraint(nom)})
    #         contraintes_list.append({"type": "ineq", "fun": create_max_constraint(nom)})
    #
    #     # Créer des contraintes pour chaque ratio
    #     def create_ratio_min_constraint(num, den, i):
    #         return lambda X: np.sum(X * data_df[num]) - contraintes_ratio_df.iloc[0, i] * np.sum(X * data_df[den])
    #
    #     def create_ratio_max_constraint(num, den, i):
    #         return lambda X: np.sum(contraintes_ratio_df.iloc[1, i] * X * data_df[den]) - np.sum(X * data_df[num])
    #
    #     print(f"contenu de ratio : {ratios}")
    #     for ratio in ratios:
    #         if len(ratio.split()) != 2:  # Supposant que les éléments de ratios sont des chaînes de caractères
    #             raise ValueError(f"Le ratio '{ratio}' ne contient pas exactement deux éléments.")
    #         else:
    #             print("success")
    #             num, den = ratio.split()
    #             contraintes_list.append({"type": "ineq", "fun": create_ratio_min_constraint(num, den)})
    #             contraintes_list.append({"type": "ineq", "fun": create_ratio_max_constraint(num, den)})
    #     # for i, (num, den) in enumerate(ratios):
    #     #     contraintes_list.append({"type": "ineq", "fun": create_ratio_min_constraint(num, den, i)})
    #     #     contraintes_list.append({"type": "ineq", "fun": create_ratio_max_constraint(num, den, i)})
    #     # Bornes
    #     b = (0, None)
    #     bnds = [b] * len(data_df)
    #
    #     # Appel de la fonction minimize
    #     solution = minimize(objectif, X0, bounds=bnds, constraints=contraintes_list, method='SLSQP')
    #
    #     # Vérification de la réussite de l'optimisation
    #     if solution.success:
    #         print(f"L'optimisation a réussi. Message : {solution.message}")
    #         print(f"Valeur minimale de la fonction objectif : {solution.fun}")
    #         print(f"Point qui minimise la fonction objectif : {solution.x}")
    #     else:
    #         print(f"L'optimisation a échoué. Message : {solution.message}")
    #
    #     # Créer un dictionnaire pour stocker les informations de la solution
    #     solution_dict = {
    #         'success': solution.success,
    #         'message': solution.message,
    #         'fun': solution.fun,
    #         'x': solution.x.tolist()  # Convertir le tableau numpy en liste pour la sérialisation JSON
    #     }
    #     logger.info(f"optimisation : {solution_dict}")
    #     # Renvoyer la solution sous forme de réponse JSON
    #     return JsonResponse(solution_dict)
    # except Exception as e:
    #     logger.error(f"Une erreur s'est produite lors du calcul d'optimisation : {e}")
    #     raise Http404("Une erreur s'est produite lors du calcul d'optimisation.")

    #     # print(f"Contraintes obtenues 2 : {contraintes}")
    #     logger.info(f"Contraintes obtenues 2 : {contraintes}")
    # except PhaseDeveloppement.DoesNotExist:
    #     raise Http404("La tranche d'age spécifiée n'existe pas.")
    # except Exception as e:
    #     print(f"Erreur lors de la récupération des contraintes : {e}")
    #     logger.error(f"Erreur lors de la récupération des contraintes : {e}")
    #     raise Http404("Une erreur s'est produite lors de la récupération de la phase de developpement et ses "
    #                   "contraintes.")
    # return JsonResponse(contraintes, safe=False)

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
