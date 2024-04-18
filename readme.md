# EasyFeed

EasyFeed est une application qui calcule votre formulation d'aliments d'animaux pour vous. Et elle ne fait pas que elle permet aussi de gerer votre ferme de facon efficace.


### Comment l'utiliser 



```commandline
 Cloner le projet 
 git clone https://github.com/dorian-404/easy-feed
 
 Aller dans le repetoire du projet 
 cd easy-feed
 
 Installer les dependances
 pip install -r requirements.txt
  
 Configurer la base de donnees 
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
Assurer vous toujours d'avoir la derniere version du projet en faisant la commande 
```commandline
   git pull nomDuProjet 
```