RespoTool
=========
L'outil de gestion et d'archivage des signalements de cartes sur [Aaaah !](http://www.extinction.fr/minijeux/)
  
![Demo](https://i.imgur.com/iWnOkzX.png)


Utilisation
===========
Nouvelle session
----------------
* __Fichier__ : Importe un fichier texte avec le contenu de `/sigmdm` et écrase les signalements déjà présents.

* __Presse-papiers__ : Idem mais depuis le presse-papiers.

Ajouter nouveaux sigs
---------------------
* __Fichier__ : Importe un fichier texte avec le contenu de `/sigmdm` et ajoute les signalements en fin de liste.

* __Presse-papiers__ : Idem mais depuis le presse-papiers. Accessible directement via <kbd>Ctrl</kbd>+<kbd>V</kbd>.

Importer / Exporter session
---------------------------
* __Importer__ : Permet de restaurer l'état du programme (signalements + statuts) depuis un fichier session _.sig_.

* __Exporter__ : Permet de stocker l'état du programme dans un fichier session _.sig_.  
  __Note__ : Les sessions sont enregistrées au format JSON. Elles sont lisibles et peuvent être modifiées à la main.

Actions
-------
* __Respomap__ : Menu déroulant servant d'identifiant. Le pseudo choisi dans ce menu sera repris dans la colonne Respomap (il s'ajoutera aux autres s'il y en a déjà).

* __Rechercher__ : La recherche est effectuée sur tous les champs d'un signalement (code, auteur, description, etc.) et est insensible à la casse. Accessible directement via <kbd>Ctrl</kbd>+<kbd>F</kbd>.

* __Archiver__ : Vide la liste des signalements pour les stocker à la fin d'un joli tableau. À ne faire qu'une fois les signalements entièrement traités.  
  __Note__ : La session n'est pas sauvegardée automatiquement après archivage.

* __Archiver sélection__ : Archive uniquement les signalements sélectionnés. La sélection doit obligatoirement être d'un seul bloc (pas de trous) et doit commencer par le premier signalement afin de conserver l'ordre des archives.  
  __Note__ : La session n'est pas sauvegardée automatiquement après archivage.

* __Playlist__ : Génère un fichier _playlist.txt_ contenant les maps signalées, à charger via `/playlist` (décocher aléatoire). La playlist reprend aussi les infos de chaque colonne (date, auteur, description, etc.).  
  __Note__ : Cette fonction est obsolète, il est préférable d'utiliser les raccourcis clavier pour load rapidement une carte.

* __Obtenir sigmdm__ : Copie dans le presse-papiers l'équivalent `/sigmdm` des signalements se trouvant dans la liste.  
  __Note__ : Les statuts/respomaps sont perdus lors de la conversion. Cette fonction est utile pour débugger mais ne devrait pas être utilisée en temps normal.

Raccourcis pratiques
====================
* <kbd>Ctrl</kbd>+<kbd>C</kbd> : Copie dans le presse-papiers la commande `/load @code` correspondant au signalement sélectionné.

* <kbd>Ctrl</kbd>+<kbd>X</kbd> : Idem que <kbd>Ctrl</kbd>+<kbd>C</kbd> mais sans le `/load`.

* <kbd>Ctrl</kbd>+<kbd>F</kbd> : Met le focus sur la barre de recherche.

* <kbd>Ctrl</kbd>+<kbd>V</kbd> : Ajoute les signalements du presse-papiers en fin de liste.

* __Double-clic sur une ligne__ : Copie dans le presse-papiers le contenu de la cellule présente sous le curseur. Permet par exemple de copier la description d'un signalement.

* __Clic droit sur une ligne__ : Affiche le contenu complet de la cellule présente sous le curseur. Permet par exemple d'afficher une description trop longue sans devoir la copier-coller ailleurs.

* __Sélectionner une ligne →__ <kbd>⏎ Entrée</kbd> : Ouvre une nouvelle fenêtre permettant d'éditer le statut du signalement. <kbd>⏎ Entrée</kbd> pour valider, <kbd>Échap</kbd> pour annuler. Voir _Utilisation des statuts.txt_ pour la syntaxe des statuts.

* __Sélectionner une ligne →__ <kbd>⌫ Arrière</kbd> / <kbd>Suppr</kbd> : Supprime le signalement. Marche aussi avec une multi-sélection (<kbd>Ctrl</kbd>+clic et/ou <kbd>⇧ Maj</kbd>+clic pour sélectionner plusieurs signalements à la fois).  
  __Note__ : Normalement jamais utilisé car tous les signalements doivent être considérés. Un troll doit être marqué comme `ignoré` et non être supprimé.

* __Sélectionner une ligne →__ <kbd>Espace</kbd> : Affiche les signalements des archives ou de la session courante qui correspondent à la même map. Permet de retracer l'historique d'une map et d'identifier les doublons.