from django.urls import path
from . import views

app_name = 'easyFeed'

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('login/connexion', views.connexion, name="connexion"),
    path('signup/', views.signup, name="signup"),
    path('dashboard/', views.dashboard, name="dashboard"),
    # path('ingredient_test/details_ingredient/', views.details_ingredient, name='details_ingredient'),
    path('formulation_form/pays_ingredients/', views.pays_ingredients, name='pays_ingredients'),
    path('formulation_form/obtenir_contraintes/', views.obtenir_contraintes, name='obtenir_contraintes'),
    # path('ingredient_test/', views.ingredient_test, name='ingredient_test'),
    path('formulation/', views.formulation, name="formulation"),
    path('formulation_form/optimize', views.optimize, name="optimize"),
    path('formulation_form/', views.formulation_form, name="formulation_form"),
    path('ingredients/', views.ingredients, name="ingredients"),
    path('create_account/', views.create_account, name="create_account"),
    path('formulation_form/manual_optimize/', views.manual_optimize, name="manual_optimize"),
]
