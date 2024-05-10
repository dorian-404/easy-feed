from django.urls import path
from . import views

app_name = 'easyFeed'

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('ingredient_test/details_ingredient/', views.details_ingredient, name='details_ingredient'),
    path('ingredient_test/pays_ingredients/', views.pays_ingredients, name='pays_ingredients'),
    path('ingredient_test/obtenir_contraintes/', views.obtenir_contraintes, name='obtenir_contraintes'),
    path('ingredient_test/', views.ingredient_test, name='ingredient_test'),
    path('formulation/', views.formulation, name="formulation"),
    path('ingredient_test/optimize', views.optimize, name="optimize"),
    path('ingredients/', views.ingredients, name="ingredients"),
]
