RespoTool
=========
Un outil de gestion et d'archivage de signalements (/mdm)
  
![Demo](http://i.imgur.com/yfeCxKx.png)


Utilisation
===========
Nouvelle session
----------------
* __Fichier__ : Importe un fichier texte avec le contenu de /sigmdm et écrase les signalements déjà présents.

* __Presse-papiers__ : Idem mais depuis le presse-papiers.

Ajouter nouveaux sigs
---------------------
* __Fichier__ : Importe un fichier texte avec le contenu de /sigmdm et ajoute les signalements en fin de liste.

* __Presse-papiers__ : Idem mais depuis le presse-papiers.

Importer / Exporter session
---------------------------
* __Importer__ : Permet de restaurer l'état du programme (signalements + statuts) depuis un fichier .sig

* __Exporter__ : Permet de stocker l'état du programme dans un fichier .sig

Commandes
---------
* __Autoriser les doublons__ : 
  Coché, garde les doublons au sein d'un lot de signalements ajoutés en même temps. Dans tous les cas si 2
  signalements sont ajoutés à des moments différents, ils seront gardés dans le cas où ils concerneraient
  2 problèmes distincts.

* __Playlist__ : 
  Génère un fichier playlist.txt contenant les maps signalées, à charger via /playlist (décocher aléatoire).
  La playlist reprend aussi les infos de chaque colonne (date, auteur, description, etc.).

* __Archiver__ : 
  Vide la liste des signalements pour les stocker à la fin d'un joli tableau dans archives/archives.txt. À ne
  faire qu'une fois les signalements entièrement traités.   
  __Note :__ Penser à exporter la liste ainsi vidée après archivage pour que le prochain respo qui importe la
  session ait une liste clean et ainsi lui éviter du travail inutile.


Raccourcis pratiques
====================
* __Double-clic sur une ligne__ : 
  Copie dans le presse-papiers le contenu de la cellule présente sous le curseur.
  Permet par exemple de copier la description d'un signalement.

* __Sélectionner une ligne -> Ctrl + C__ :
  Copie "/load @code" dans le presse-papiers où @code est le code correspondant au signalement

* __Sélectionner une ligne -> Entrée__ :
  Ouvre un champ de texte permettant d'éditer le statut du signalement. __Entrée__ pour valider,
  __Échap__ pour annuler. Voir statuts.txt pour la liste des statuts recommandés.

* __Sélectionner une ligne -> Retour / Suppr__ :
  Supprime le signalement. Marche aussi avec une multi-sélection (Ctrl+clic et/ou Shift+clic pour sélectionner plusieurs signalements
  à la fois).