# EasyFeed

EasyFeed est une application qui calcule vos formules d'alimentation pour vous. Elle vous permet également de gérer efficacement vos employés et vos animaux.

### Comment l'utiliser 



```commandline
 Cloner le projet 
 git clone https://github.com/dorian-404/easy-feed
 
 Aller dans le repetoire du projet 
 cd easy-feed
 
 Creer son environnement virtuel 
 pyhton -m venv venv 
 
 Activer votre environnemnt virtuel 
 .\venv\Scripts\activate
 
 Installer les dependances
 pip install -r requirements.txt
  
 Configurer la base de donnees (faclutatif pour le moment)
 python manage.py migrate
 
 Lancer le serveur 
 python manage.py runserver


```

### Guides des branches

Pour les branches, notre projet va structurer en 2 branches principales :   
    - La branche main   
    - La branche develop
    ![img.png](img.png)


#### Comment faire pour envoyer on code sur le depot distant ?
Assurez-vous toujours que vous disposez de la dernière version du projet en lançant la commande 
```commandline
   git pull orgin develop
```
Créez ensuite votre propre branche (la branche que vous êtes sur le point de créer est LOCALE).
```commandline
   git checkout <nomDeLaFonctionnalite>
```
Une fois que vous avez effectué les modifications souhaitées 
```commandline
   # Pour indexer les modif
   git add . 
   
   # Pour verifier que si tous les fichiers mis a jour sont present 
   git status 
   
   # Faites votre commit
   git commit -m "nomDeLaFonctionnalite: message pour decrire les changements"
   
   # Basculer vers la branche develop 
   git checkout develop 
   
   # Faites une merge de votre branche local et notre branche distante develop
   git merge <nomDeVotreBranche>
   
   # Faites une PR (Pull Request)
   Une Pull Request est un demande de fusion des modifications d'une branche a une autre.
```