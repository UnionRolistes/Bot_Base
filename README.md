[![forthebadge](https://forthebadge.com/images/badges/cc-nc-sa.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) 
## Bot Python (UR-Bot)

[TOCM]

[TOC]


```
├── Description du projet 
├── Languages utilisés
├── Credit , participant, organisation
|
├── 1) Bot Base
│	├── - But
│	├── -Installation
│	└── - Usage
|
├── 2.1) Bot-Prez
│ 	├── - But
│	├── - Installation
│	└── - Usage
|
├── 2.2) WebPrez
|
├── 3.1) Bot-planning
|   ├── - But
|   ├── - Installation
|   └── - Usage
|
├── 3.2) Web-Planning
├── - But
├── - Installation
└── - Usage
```



## Description
> Le BotPresentation(Python3.7) permet à un utilisateur d'accéder à un formulaire de présentation via la commande $prez. Les informations saisies sont ensuite mises en forme et postées sur le discord de l'union des Rôlistes via un Webhook dans la section #presentation

## Languages utilisés
 - Py ( Python )
 - XML (  eXtensible Markup Language )
 - HTML (  eXtensible Markup Language )
 - CSS (  eXtensible Markup Language )
 - sh (  Bash )


Credits -> [credits.md](https://github.com/UnionRolistes/Bot_Base/blob/main/credits.md)

  
#  1) Bot Base

######  https://github.com/UnionRolistes/Bot_Base
 Bot_Base est un repo commun aux autres projet.
Il permet de simplifier l'installation d'un ou plusieurs éléments.
  ### Installation         
   **Pour une 1ère installation** : ``` "cd /usr/local/src && sudo git clone https://github.com/UnionRolistes/Bot_Base && cd Bot_Base && sudo bash updateBot.sh" ``` 
			
   **Pour une mise à jour** : ``` "cd /usr/local/src/Bot_Base && sudo git checkout . && sudo git pull && sudo bash updateBot.sh" ```	 
   
 How to setup URbot - The discord bot for managing servers dedicated to rpgs 
 ---
  ##### - 1 )   Install a linux based OS (we'll be using Debian as a reference)

  ##### - 2 )  Install git

 ##### - 3 )  ``` "cd /usr/local/src && sudo git clone  https://github.com/UnionRolistes/Bot_Base  && cd Bot_Base && sudo bash updateBot.sh" ```

  **It installs the bot and the 2 sub features** : 

   1. Bot_Planning and Web_Planning 
   2. Bot_Presentation and Web_Presentation
				 
   ##### - 4 )  If you want to choose the features to install --> ```"cd /usr/local/src/Bot_Base && sudo git pull && sudo bash install.sh" Then "sudo bash " ```

   ##### - 5 )  Start the bot and the web sites with "cd/usr/local/src/Bot_Base && sudo bash start.sh && sudo service apache2 restart "

#  2.1) Bot-Prez

  ######  https://github.com/UnionRolistes/Bot_Presentation
  Le BotPresentation(Python3.7) permet à un utilisateur d'accéder à un formulaire de présentation via la commande $prez. Les informations saisies sont ensuite mises en forme et postées sur le discord de l'union des Rôlistes via un Webhook dans la section #presentation
  
   ![](https://github.com/UnionRolistes/Bot_Base/blob/main/img/BotPresentation_Grafcet-page-002.jpg?raw=true)
   ![](https://github.com/UnionRolistes/Bot_Base/blob/main/img/BotPresentation_Grafcet-page-001.jpg?raw=true)
 
   ### Installation
            
  **Pour une 1ère installation** : ``` "cd /usr/local/src && sudo git clone      https://github.com/UnionRolistes/Bot_Base && cd Bot_Base && sudo bash updateBot.sh" ```
			
---
			
- **Pour une mise à jour** : ``` "cd /usr/local/src/Bot_Base && sudo git checkout . && sudo git pull && sudo bash updateBot.sh" ```

#  2.2) WebPrez

#  3.1) Bot-planning
   >  - ###### https://github.com/UnionRolistes/Bot_Planning_python
   
   >  - Le BotPlanning(Python3.7) et FormulaireJdR (HTML CSS PHP) est un projet lancé a l'initiative de l'Union des Rôlistes (**http://unionrolistes.fr**) un bot discord capable de générer des messages correctement mis en forme, annoncant de prochaine partie de JdR, quel soit physique ou a distance. actuellement les message finaux sont visible sur le discord de l'union des Rôlistes via un Webhook dans la section #Planning-JdR .
   
 ### Installation
	    
   **Pour une 1ère installation** : "cd /usr/local/src && sudo git clone **https://github.com/UnionRolistes/Bot_Base** && cd Bot_Base && sudo bash updateBot.sh"

**Pour une mise à jour** : "cd /usr/local/src/Bot_Base && sudo git checkout . && sudo git pull && sudo bash updateBot.sh"

**how to use (in discord)** une fois sur votre serveur discord, et apres avoir vérifier que le bot (ou role des bot) pouvais ecrire dans le canal où vous vous trouvez ecrivez $cal la commande s'effacera, puis vous receverez un message privé avec les instruction.

#  3.2) Web-Planning

   ###### https://github.com/UnionRolistes/Web_Planning
   #### Web_Planning : Formulaire de création de partie
   Le formulaire permet a un animateur (MJ) de proposer une session de JdR sur un serveur discord. Via la commande $jdr, il recoit un lien vers un formulaire, avec diverses entrées. Une fois le formulaire completé et validé, celui ci est envoyé vers le discord, et l'annonce mise en forme est alors disponible sur le discord dans le canal #planning-jdr, les joueurs potentiels peuvent alors lire et réagir pour s'y inscrire. Ensuite le MJ peut les contacter pour les informations supplémentaires, telles que la creation de personnage. 
	 
   #### Web_Planning : Calendrier
   Calendrier web affichant les parties prévues. Via la commande $cal l'utilisateur reçoit le lien du calendrier Ce calendrier affiche horizontalement les parties prévues, par semaine ou par mois. Cliquer sur un événement donnera accès à plus de détails sur la partie, ainsi qu'un lien vers le message discord pour pouvoir s'y inscrire. Les administrateurs ont accès à une section permettant de pré remplir le formulaire avec les données d'une partie déjà existante, afin de la dupliquer. Ils peuvent aussi afficher tous les détails d'une partie selon une mise en forme leur permettant de copier facilement le texte pour une exportation sur les réseaux sociaux
	 
   ### Installation
   **Pour une 1ère installation** : ``` "cd /usr/local/src && sudo git clone https://github.com/UnionRolistes/Bot_Base && cd Bot_Base && sudo bash updateBot.sh" sudo nano /var/www/html/Web_Planning/php/config.php.default" ``` --> Remplir ce fichier avec le Client ID, Secret ID et Redirect_URI du Bot, trouvable sur Discord developer (**https://discord.com/developers/applications**)

``` sudo nano /etc/apache2/sites-available/100-UR_Planning.conf``` --> Remplacer "serverName planning.unionrolistes.fr" (ligne 9) par la redirection saisie sur votre hébergeur en ligne

**Pour une mise à jour** :  ``` "cd /usr/local/src/Bot_Base && sudo git checkout . && sudo git pull && sudo bash updateBot.sh"```

