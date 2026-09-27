# Infanterie : clé de l'acteur -> (nom en français, lore sur 3 lignes, stratégie)
TEXTES = {
"Ant": ("Fourmi géante", """Insecte irradié devenu monstrueux dans les laboratoires biologiques.
Ses mandibules broient l'acier comme la chair.
Personne ne sait vraiment ce qui s'est passé dans ces laboratoires.""",
"Disponible seulement après capture d'un laboratoire biologique. Envoyez-la en masse : très résistante (75 000 PV) mais au corps à corps uniquement."),
"CQ": ("Conquistador", """Fantassin d'élite espagnol armé d'un fusil prisme portatif.
Il combat à distance et peut capturer les bâtiments ennemis.
Il perpétue la tradition des conquérants, en version haute technologie.""",
"Combinez attaque et capture : éliminez les défenseurs puis capturez les bâtiments. Fragile contre les chars."),
"DOG": ("Chien d'attaque", """Chien dressé par les Soviétiques pour traquer l'infanterie.
Une morsure suffit à neutraliser un fantassin ; il flaire aussi les espions.
Les meilleurs gardes du corps d'une base soviétique.""",
"Protégez votre base contre les espions et l'infanterie infiltrée. Inutile contre les véhicules."),
"E1": ("Fusilier", """Fantassin de base, l'âme de toutes les armées.
Bon marché et remplaçable, il tient les positions et nettoie l'infanterie.
Des millions d'entre eux ont gagné des guerres que les chars ont prises en photo.""",
"Utilisez-le en masse pour tenir des positions et éliminer l'infanterie adverse. Garnissez les pillbox et les tranchées."),
"E1.Greece": ("Fusilier grec", """Fusilier grec des premières phases, avant l'arrivée des armures.
Il ajoute des grenades antibâtiment à l'équipement standard.
Il laisse sa place aux hoplites dès que le centre technique est construit.""",
"Infanterie de base grecque : tenez les positions en attendant les hoplites. Les grenades aident contre les bâtiments."),
"E13": ("Soldat Chrono", """Fantassin d'élite allemand de la carte WW3, armé d'un canon chronosphérique portatif.
Il efface littéralement ses cibles du temps.
Efficace contre l'infanterie comme contre les véhicules.""",
"Infanterie polyvalente de haut niveau : utilisez-le contre infanterie et véhicules légers. Protégez-le de l'aviation."),
"E1CH": ("Conscrit chinois", """Fantassin chinois conscrit, produit en masse à bas prix.
Moins résistant que les fusiliers étrangers, il compense par le nombre.
Il arme aussi l'Overlord s'il est embarqué.""",
"Produisez-en beaucoup : il est moins cher que les autres fusiliers. Placez-en dans l'Overlord pour lui donner une mitrailleuse."),
"E1GI": ("GI", """Fantassin américain de la carte WW3, bien équipé et entraîné.
Il porte des grenades antibâtiment en plus de son fusil.
Le GI est la base de la puissance terrestre américaine.""",
"Fusilier polyvalent américain : tenez les positions et harcelez les bâtiments avec les grenades."),
"E2": ("Grenadier", """Fantassin soviétique armé de grenades.
Ses grenades frappent l'infanterie groupée et les bâtiments.
Il faut une bonne dose de courage pour les lancer au bon moment.""",
"Nettoyez l'infanterie groupée et endommagez les bâtiments. Évitez les chars."),
"E3": ("Lance-roquettes", """Fantassin antichar et antiaérien, commun à toutes les armées.
Ses roquettes frappent les chars comme les hélicoptères.
Aucun blindé ne se sent en sécurité face à un groupe de lance-roquettes.""",
"Escortez vos chars contre les blindés et l'aviation ennemis. Protégez-les de l'infanterie ennemie, qu'ils gèrent mal."),
"E3.Greece": ("Lance-roquettes grec", """Lance-roquettes grec des premières phases.
Identique au soldat roquette standard.
Il reste utile tant que les armures grecques ne sont pas disponibles.""",
"Antichar et antiaérien de base pour la Grèce : couvrez vos hoplites contre les chars et l'aviation."),
"E4": ("Lance-flammes", """Fantassin soviétique équipé d'un lance-flammes.
Il incendie infanterie et bâtiments à courte portée.
L'ennemi préfère souvent fuir que de l'affronter.""",
"Attaquez les bâtiments et l'infanterie retranchée. Courte portée : approchez sous couverture."),
"E4.Greece": ("Lance-flammes grec", """Lance-flammes grec des premières phases.
Identique au lance-flammes soviétique.
Il cède ensuite sa place à l'hoplite lance-flammes.""",
"Même emploi que le lance-flammes : bâtiments et infanterie retranchée."),
"E6": ("Ingénieur", """Spécialiste capable de capturer les bâtiments ennemis ou de réparer les vôtres.
Sans arme, il vaut pourtant plus que dix soldats au bon endroit.
Une raffinerie capturée change le cours d'une partie.""",
"Transportez-le jusqu'à un bâtiment ennemi clé (usine, raffinerie, centre technique) pour le capturer. Réparez aussi les ponts et bâtiments amis."),
"E7": ("Tanya", """Commando d'élite des Alliés, armée de deux pistolets et de charges C4.
Elle détruit les bâtiments d'une charge et élimine l'infanterie d'une balle.
Une seule Tanya a changé plus d'une guerre.""",
"Infiltrez-la via un transport pour poser du C4 sur les bâtiments clés. Évitez les chars et les chiens ; une seule peut exister."),
"FPVOP": ("Opérateur de drone FPV", """Opérateur ukrainien de drones kamikazes à vue immersive.
Couché, il verrouille sa cible et lance un drone qui fonce sur elle.
Bon marché, il change la valeur des blindés sur le champ de bataille.""",
"Déployez-le derrière une ligne défensive : ses drones à 9 cases frappent le toit des blindés (ignorent l'ERA). Un drone toutes les 10 s : groupez plusieurs opérateurs pour tuer un char lourd."),
"GCP": ("Commando parachutiste (GCP)", """Groupement des commandos parachutistes français, forces spéciales d'élite.
Furtifs, ils voient loin et désignent au laser les cibles des frappes SCALP.
Là où ils passent, les missiles de croisière suivent.""",
"Infiltrez-les près des cibles clés, puis activez la frappe SCALP pour guider un missile dévastateur. Ils activent aussi la liaison SCORPION des Leclerc proches."),
"GENIE": ("Ingénieur militaire", """Ingénieur du génie français, spécialiste des fortifications de campagne.
Déployé, il ouvre une zone de construction pour défenses et tranchées.
Il transforme n'importe quelle position en bastion.""",
"Déployez-le sur une position avancée pour y construire des défenses et des tranchées, loin de la base. Protégez-le : il est non armé."),
"GENMEDI": ("Infirmier soviétique", """Infirmier des armées soviétiques, disponible après la capture d'un hôpital.
Il soigne l'infanterie blessée sur le champ de bataille.
Chaque soldat sauvé est un soldat de plus sur le front.""",
"Accompagnez vos groupes d'infanterie pour soigner les blessés entre deux combats."),
"HACKER": ("Hacker", """Pirate informatique chinois.
Il pirate les bâtiments ennemis et vole des ressources sur Internet.
La guerre de l'information, version Pékin.""",
"Piratez les bâtiments ennemis pour les neutraliser. Placez-le dans un Internet Centre pour générer des crédits, ou dans l'Overlord pour la propagande."),
"HIP": ("Hippeis", """Cavalerie moderne grecque de la carte WW3, armée de roquettes.
Rapide, elle frappe à la fois au sol et dans les airs.
Les cavaliers de l'Antiquité ont trouvé de dignes héritiers.""",
"Unité de harcèlement rapide : frappez les véhicules et les aéronefs, puis repliez-vous."),
"HOP": ("Hoplite", """Fantassin grec en armure de puissance légère.
Il résiste deux fois mieux qu'un fusilier et tire en rafales.
La phalange moderne de la Grèce.""",
"Tenez les positions en ligne compacte : sa résistance lui permet de tenir face à l'infanterie ennemie."),
"HOPF": ("Hoplite lance-flammes", """Hoplite grec en armure moyenne, armé d'un lance-flammes lourd.
Il incendie l'infanterie et les bâtiments tout en résistant aux tirs.
Il n'avance pas vite, mais il n'a pas besoin de courir.""",
"Nettoyez l'infanterie retranchée et les bâtiments, en première ligne grâce à son blindage."),
"IVAN": ("Crazy Ivan", """Spécialiste de la démolition turc de la carte WW3.
Il colle des charges explosives sur les bâtiments et les véhicules.
Sa réputation de folie n'est plus à faire.""",
"Posez des explosifs sur les défenses et bâtiments ennemis. Il vise mal les cibles mobiles : attaquez les structures."),
"JJET": ("Soldat à réacteur dorsal", """Fantassin américain équipé d'un réacteur dorsal.
Il survole les obstacles et frappe l'infanterie comme les aéronefs.
Les murs et les rivières ne l'arrêtent plus.""",
"Franchissez les obstacles pour frapper l'infanterie et les unités de soutien derrière les lignes."),
"MECH": ("Mécanicien", """Mécanicien des Alliés, spécialiste de la réparation de véhicules.
Il répare les blindés sur le terrain et remet en état les épaves.
Il transforme une défaite en une armée prête à repartir.""",
"Suivez vos colonnes pour réparer les chars entre deux combats et capturez les épaves pour les remettre en service."),
"MEDI": ("Infirmier", """Infirmier des Alliés, soigne l'infanterie blessée.
Il ne tire pas, mais il maintient une escouade en vie bien plus longtemps.
Chaque soldat soigné est un soldat qui ne coûte rien.""",
"Accompagnez vos groupes d'infanterie pour les soigner entre les engagements."),
"MORT": ("Mortier", """Fantassin ukrainien armé d'un mortier.
Il tire au-dessus des obstacles sur l'infanterie et les bâtiments.
Discret et efficace, il est le soutien de feu de l'infanterie.""",
"Pilonnez l'infanterie et les bâtiments à 7 cases, derrière votre ligne. Il est vulnérable aux chars."),
"NLAW": ("Équipe NLAW", """Équipe antichar d'élite britannique armée de missiles à attaque par le toit.
Ses missiles ignorent le blindage réactif.
En pillbox, elle devient une embuscade mortelle.""",
"Placez-la en garnison dans un pillbox pour un tir d'embuscade dévastateur. Excellente contre le T-90M et le BMPT, dont l'ERA ne la gêne pas."),
"RMBO": ("Commando", """Commando d'élite américain de la carte WW3.
Il est armé d'une mitrailleuse lourde, de grenades et de roquettes.
Seul, il peut tenir une position face à une escouade.""",
"Infiltrez-le pour nettoyer l'infanterie et les bâtiments. Déployé, il gagne en résistance."),
"SAB": ("Saboteur", """Agent turc de la carte WW3, porteur d'une mini-bombe nucléaire.
Il se déguise pour s'infiltrer dans la base ennemie.
Il ne revient jamais, mais son passage non plus ne s'oublie pas.""",
"Déguisez-le et infiltrez-le au cœur de la base ennemie pour détruire un bâtiment clé."),
"SHOK": ("Soldat de choc", """Fantassin d'élite russe équipé d'une bobine Tesla portable.
Ses arcs électriques frappent l'infanterie et les véhicules.
Une bobine Tesla qui marche.""",
"Unité polyvalente contre infanterie et véhicules : accompagnez vos chars Tesla."),
"SNIPER": ("Sniper", """Tireur d'élite français de la carte WW3.
Son fusil longue portée élimine l'infanterie à 10 cases.
Il ne manque jamais sa cible.""",
"Éliminez l'infanterie ennemie de très loin. Protégez-le des véhicules et des chiens."),
"SPART": ("Armure Spartan", """Armure de puissance lourde grecque de la carte WW3.
Elle combine une mitrailleuse et un canon à grenades.
Presque un véhicule, mais avec l'agilité d'un fantassin.""",
"Unité de percée : avancez en tête contre l'infanterie et les véhicules légers."),
"SPECOP": ("Royal Marine", """Fusilier d'élite britannique.
Armé d'un fusil et de grenades, il est redoutable contre l'infanterie et les bâtiments.
L'élite de l'infanterie de la Couronne.""",
"Infanterie d'élite polyvalente : attaquez l'infanterie et les bâtiments."),
"SPY": ("Espion", """Agent de renseignement déguisé.
Il s'infiltre dans les bâtiments ennemis pour voler des informations ou saboter.
Le résultat dépend du bâtiment infiltré.""",
"Infiltrez les bâtiments ennemis : centrale (coupure de courant), raffinerie (vol d'argent), usine (technologie), radar (vision). Méfiez-vous des chiens."),
"SPY.England": ("Espion britannique", """Espion des services britanniques, moins cher que ses homologues.
Même rôle : infiltration et sabotage.
Le MI6 a toujours eu le goût de l'efficacité.""",
"Même emploi que l'espion, pour moitié prix : multipliez les infiltrations."),
"THF": ("Voleur", """Voleur furtif capable de dérober les crédits ennemis.
Il détourne aussi les véhicules ennemis.
La guerre économique à l'état pur.""",
"Volez les crédits des raffineries et silos ennemis, ou détournez un véhicule précieux."),
"TRENCH": ("Fantassin de tranchée", """Fantassin ukrainien spécialiste de la défense retranchée.
Déployé, il creuse une tranchée qui le protège et augmente sa portée.
Il transforme chaque position en ligne de défense.""",
"Déployez-le en ligne pour tenir une position : dégâts reçus -50 %, portée +15 %, immunisé à l'écrasement et à la suppression."),
"Zombie": ("Zombie", """Créature mort-vivante issue des laboratoires biologiques.
Lente mais très résistante, elle attaque au corps à corps.
Personne ne veut vraiment savoir comment elle est apparue.""",
"Disponible après capture d'un laboratoire biologique. Envoyez-les en masse pour submerger l'ennemi."),
}
