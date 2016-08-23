RespoTool
=========
Un outil de gestion et d'archivage de signalements de cartes sur [Aaaah !](http://www.extinction.fr/minijeux/)
  
![Demo](http://i.imgur.com/PW8No6S.png)


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
* __Importer__ : Permet de restaurer l'état du programme (signalements + statuts) depuis un fichier session
  _.sig_.

* __Exporter__ : Permet de stocker l'état du programme dans un fichier session _.sig_.  
  __Note__ : Les sessions sont enregistrées au format JSON. Elles sont lisibles et peut éventuellement être
  modifiées à la main.

Actions
-------
* __Archiver__ : 
  Vide la liste des signalements pour les stocker à la fin d'un joli tableau dans archives/archives.txt. À ne
  faire qu'une fois les signalements entièrement traités.  
  __Note__ : Penser à exporter la liste ainsi vidée après archivage pour que le prochain respo qui importe la
  session ait une liste clean et ainsi lui éviter du travail inutile.

* __Archiver sélection__ : 
  Archive uniquement les signalements sélectionnés. La sélection doit obligatoirement être d'un seul bloc (pas
  de trous) et doit commencer par le premier signalement afin de conserver l'ordre des archives.

* __Playlist__ : 
  Génère un fichier playlist.txt contenant les maps signalées, à charger via /playlist (décocher aléatoire).
  La playlist reprend aussi les infos de chaque colonne (date, auteur, description, etc.).  
  __Note__ : Cette fonction est obsolète, il est préférable d'utiliser les raccourcis clavier pour load
  rapidement une carte.

* __Obtenir sigmdm__ :
  Copie dans le presse-papiers l'équivalent /sigmdm des signalements se trouvant dans la liste. Les statuts
  sont perdus lors de la conversion.

Raccourcis pratiques
====================
* __Double-clic sur une ligne__ : 
  Copie dans le presse-papiers le contenu de la cellule présente sous le curseur.
  Permet par exemple de copier la description d'un signalement.

* __Sélectionner une ligne -> Ctrl + C__ :
  Copie "/load @code" dans le presse-papiers où @code est le code correspondant au signalement

* __Sélectionner une ligne -> Entrée__ :
  Ouvre une nouvelle fenêtre permettant d'éditer le statut du signalement. __Entrée__ pour valider,
  __Échap__ pour annuler. Voir statuts.txt pour la liste des statuts recommandés.

* __Sélectionner une ligne -> Retour / Suppr__ :
  Supprime le signalement. Marche aussi avec une multi-sélection (Ctrl+clic et/ou Shift+clic pour sélectionner
  plusieurs signalements à la fois).