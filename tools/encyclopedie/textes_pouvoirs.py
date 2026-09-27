# Pouvoirs de soutien : nom du pouvoir dans les règles -> (nom en français, lore sur 3 lignes, stratégie)
TEXTES = {
"Atom Bomb": ("Bombe atomique", """L'arme ultime, lancée depuis le silo à missiles.
Elle rase tout dans sa zone d'impact et laisse une zone irradiée.
Son lancement est annoncé à tous les joueurs.""",
"Visez la concentration de bâtiments clés de l'ennemi (chantier de construction, usines, centrales)."),
"Invulnerability": ("Invulnérabilité (Rideau de fer)", """Le Rideau de fer rend un groupe d'unités invulnérable.
Pendant ce temps, rien ne peut les endommager.
La version avancée ukrainienne couvre une zone plus large.""",
"Activez-le au moment où vos chars pénètrent dans la zone de défense ennemie."),
"Chronoshift": ("Chronoshift", """La Chronosphère téléporte un groupe d'unités.
Elles reviennent à leur point de départ après 20 secondes.
Le pouvoir de choisir le champ de bataille.""",
"Téléportez un groupe de chars au cœur de la base ennemie, sur ses bâtiments clés."),
"Advanced Chronoshift": ("Chronoshift avancé", """Version avancée du Chronoshift, qui téléporte un groupe plus large.
Elle est disponible via la Chronosphère et le centre technique allemand.
Une armée entière qui disparaît et réapparaît.""",
"Téléportez un grand groupe d'unités pour un assaut décisif."),
"GPS Satellite": ("Satellite GPS", """Satellite qui révèle toute la carte.
Il nécessite un radar actif.
Plus aucun secret sur le champ de bataille.""",
"Lancez-le dès que possible pour connaître la position de l'ennemi."),
"Spy Plane": ("Avion espion", """Avion espion qui survole une zone et la révèle.
Il fournit une vision temporaire de la base ennemie.
Connaître l'ennemi, c'est déjà le vaincre.""",
"Révélez la base ennemie avant une frappe de superarme ou un assaut."),
"Paratroopers": ("Parachutistes", """Un bombardier Badger largue une escouade d'infanterie.
Elle atterrit n'importe où sur la carte.
Une attaque par surprise.""",
"Larguez-les derrière les lignes ennemies pour frapper l'artillerie ou les bâtiments."),
"Parabombs": ("Parabombes", """Un bombardier Badger largue une série de bombes parachutées.
Elles frappent une zone précise.
Une frappe aérienne à la demande.""",
"Frappez les concentrations de bâtiments ou d'unités ennemies. Évitez les défenses antiaériennes."),
"Frappe nucléaire (SNLE)": ("Frappe nucléaire du SNLE", """Missile balistique nucléaire tiré depuis la position du SNLE.
60 % de la puissance de la bombe du silo.
La dissuasion océanique.""",
"Frappez depuis une position sûre ; la charge plus longue que le silo impose de bien choisir la cible."),
"Frappe de croisière SCALP": ("Frappe de croisière SCALP", """Les GCP désignent une cible au laser pendant 30 secondes.
Un missile de croisière tiré hors-carte la frappe alors avec 45 000 dégâts.
Sans GCP ni cible visible, pas de frappe.""",
"Infiltrez vos GCP près d'une cible clé, puis activez le pouvoir en les sélectionnant."),
"Pontage tactique rapide": ("Pontage tactique rapide", """Pont flottant en croix posé sur une rivière ou un plan d'eau.
Les chars peuvent l'emprunter pendant 90 secondes.
Chaque travée peut être détruite séparément.""",
"Franchissez une rivière défendue pour contourner les positions ennemies."),
"Brouillage électronique SAS": ("Brouillage électronique SAS", """Brouillage d'une grande zone pendant 30 secondes.
Radar ennemi coupé, pouvoirs de soutien suspendus, vision réduite de moitié.
Aucun dégât, mais un aveuglement total.""",
"Brouillez juste avant votre assaut, ou pour bloquer une superarme ennemie."),
"Renseignement OTAN (AWACS)": ("Renseignement OTAN (AWACS)", """Révèle une très grande zone pendant 15 secondes.
Il détecte les unités furtives et marque les blindés chenillés.
L'information comme arme.""",
"Révélez la position de l'ennemi avant une frappe d'artillerie ou de FPV."),
"Frappe thermobarique TOS-1A": ("Frappe thermobarique TOS-1A", """Salve thermobarique sur une zone explorée.
Elle dévaste l'infanterie et démoralise pendant 10 secondes toutes les unités présentes.
Amies comme ennemies.""",
"Frappez les concentrations d'infanterie ennemie, en évitant vos propres unités."),
"Stealth Shield": ("Bouclier furtif", """Rend un groupe d'unités invisible pendant 30 secondes.
Elles peuvent s'approcher de l'ennemi sans être vues.
Une armée fantôme.""",
"Approchez un groupe d'unités de la base ennemie pour un assaut surprise."),
"Ion Cannon": ("Canon à ions", """Frappe du canon à ions orbital américain.
Des dégâts instantanés sur une petite zone.
La puissance spatiale américaine.""",
"Frappez un bâtiment clé ou une unité isolée de grande valeur."),
"Sonar Pulse": ("Impulsion sonar", """Révèle tous les sous-marins dans une zone.
Elle permet de chasser les sous-marins ennemis.
La mer n'a plus de secrets.""",
"Révélez les sous-marins ennemis avant d'engager vos destroyers."),
"Hostile Takeover": ("Prise de contrôle hostile", """Un avion largue une escouade de Conquistadors et d'ingénieurs.
Ils atterrissent n'importe où sur la carte.
Une conquête espagnole moderne.""",
"Larguez-les près d'un bâtiment clé ennemi pour le capturer."),
"Sniper Drop": ("Largage de snipers", """Un avion largue une escouade de snipers.
Ils atterrissent n'importe où sur la carte.
La précision américaine derrière les lignes.""",
"Larguez-les près de l'infanterie ennemie pour l'éliminer à distance."),
"Airstrike": ("Frappe aérienne", """Une escouade de B-2 Spirit largue des bombes incendiaires.
La frappe la plus destructrice de l'aviation américaine.
Rien ne résiste à un bombardement furtif.""",
"Frappez les concentrations de bâtiments ou d'unités ennemies."),
"TankDrop": ("Largage de chars", """Des bombardiers Badger larguent trois chars.
Ils atterrissent n'importe où sur la carte.
Une percée blindée tombée du ciel.""",
"Larguez-les derrière les lignes ennemies pour frapper l'artillerie ou les bâtiments."),
"Insurgants": ("Insurgés", """Une foule d'insurgés apparaît dans la zone.
Ils submergent l'ennemi par le nombre.
La subversion turque.""",
"Faites apparaître les insurgés au cœur de la base ennemie pour semer le chaos."),
"Spartan Drop": ("Largage de Spartan", """Un avion largue des armures Spartan.
Elles atterrissent n'importe où sur la carte.
L'élite grecque tombée du ciel.""",
"Larguez-les derrière les lignes ennemies pour une percée."),
"Industrialisation": ("Industrialisation", """L'industrie chinoise produit un flux de chars lourds.
Des chars supplémentaires apparaissent régulièrement.
La production de masse comme arme.""",
"Utilisez-la dès que possible pour renforcer votre armée."),
"Brouillage électronique japonais": ("Brouillage électronique japonais", """Brouille une zone de 7 cases pendant 20 secondes.
Portée ennemie -40 %, tirs moins précis, zone et furtifs révélés.
Un outil défensif, pas un bouton « je gagne ».""",
"Brouillez un assaut ennemi pour le combattre hors de sa portée, avec vos Type 10 à longue distance."),
"Barrage Pinaka": ("Barrage Pinaka", """Dix roquettes s'abattent au hasard sur une large zone.
Excellent contre l'infanterie, bon contre les bâtiments légers.
Limité contre les blindés lourds.""",
"Saturez les concentrations d'infanterie ou les bases légères ; la zone devient dangereuse pendant quelques secondes."),
}
