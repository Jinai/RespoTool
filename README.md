RespoTool
=========
Un outil de gestion et d'archivage de signalements (/mdm)
  
![Demo](http://i.imgur.com/YgoAHrS.png)


Utilisation
===========
Nouvelle session
----------------
* __Fichier__ : Importe un fichier texte avec le contenu de /sigmdm et écrase les signalements déjà ouverts

* __Presse-papiers__ : Idem mais depuis le presse-papiers

Ajouter nouveaux sigs
---------------------
* __Fichier__ : Idem mais ajoute les signalements en fin de liste

* __Presse-papiers__ : Idem mais depuis le presse-papiers

Importer / Exporter session
---------------------------
* __Importer__ : Permet de restaurer l'état du programme (signalements + statuts) depuis un fichier .sig

* __Exporter__ : Permet de stocker l'état du programme dans un fichier .sig

Commandes
---------
* __Playlist__ : 
  Génère un fichier playlist.txt contenant les maps signalées, à charger via /playlist (décocher aléatoire).
  La playlist reprend aussi les infos de chaque colonne (date, auteur, description etc)

* __Archiver__ : 
  Ajoute, sur confirmation, les signalements à la fin d'un joli tableau dans archives/archives.txt.
  À ne faire qu'une fois les signalements entièrement traités. Ca permettra plus tard de faire des stats


Raccourcis pratiques
====================
* __Double-clic sur une ligne__ : 
  Copie dans le presse-papiers le contenu de la cellule présente sous le curseur.
  Permet par exemple de copier le code d'une map

* __Sélectionner une ligne -> Entrée__ :
  Ouvre un champ de texte permettant d'éditer le statut du signalement.
  Échap pour fermer sans enregistrer, Entrée pour valider.
  Voir statuts.txt pour la liste des statuts recommandés

* __Sélectionner une ligne -> Retour / Suppr__ :
  Supprime le signalement (captain obvious).
  Marche aussi avec une multi-sélection (Ctrl+clic et/ou Shift+clic)