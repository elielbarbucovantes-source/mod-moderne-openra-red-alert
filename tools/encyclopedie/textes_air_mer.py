# Aviation et marine : clé de l'acteur -> (nom en français, lore sur 3 lignes, stratégie)
TEXTES = {
# ------------------------------------------------------------------ AVIATION
"A10": ("A-10 Warthog", """Avion d'appui rapproché américain, construit autour de son canon de 30 mm.
Il chasse les chars comme personne, en rase-mottes.
Son grondement fait fuir des colonnes entières.""",
"Frappez les colonnes blindées ennemies, après avoir neutralisé leur défense antiaérienne. Il revient se réarmer à la base aérienne."),
"ALADIN": ("ALADIN (guerre électronique)", """Mini-drone allemand équipé de brouilleurs.
Il dégrade la précision, le verrouillage et la vision des ennemis proches.
Invisible dans ses effets, redoutable dans ses conséquences.""",
"Faites-le planer au-dessus de l'armée ennemie pendant votre assaut pour dégrader leurs tirs. Inutile contre une armée sans armes guidées."),
"ANT40": ("Bombardier tactique", """Bombardier ukrainien de la carte WW3, chargé de bombes incendiaires.
Il incendie l'infanterie et les véhicules légers sur son passage.
Il vole haut et frappe fort.""",
"Frappez les concentrations d'infanterie et de véhicules légers. Évitez les défenses antiaériennes."),
"BLACKHORNET": ("Black Hornet", """Nano-drone britannique de reconnaissance, pas plus grand qu'une main.
Invisible sauf à courte portée, il explore les lignes ennemies.
L'œil qu'on ne voit jamais.""",
"Explorez derrière les lignes ennemies sans être vu. Ne le laissez pas s'approcher des détecteurs."),
"COLIBRI": ("Munition rôdeuse Colibri", """Munition rôdeuse française qui tourne au-dessus de la zone avant de frapper.
Elle fonce sur sa cible et explose, frappant le blindage par le dessus.
Deux minutes de vol, une seule attaque.""",
"Lancez-la contre l'artillerie, les véhicules légers ou les bâtiments. Elle ignore le blindage réactif : excellente contre le T-90M."),
"F22": ("F-22 Raptor", """Chasseur furtif américain de supériorité aérienne.
Il frappe au sol comme dans les airs avec ses missiles.
Le prédateur le plus rapide du ciel.""",
"Dominez le ciel et frappez les cibles au sol. Il peut apponter sur le porte-avions américain."),
"HARRIER": ("Harrier", """Avion d'attaque britannique à décollage vertical.
Il se pose n'importe où et fait du vol stationnaire.
Missiles air-sol et torpilles : il frappe la terre comme la mer.""",
"Frappez les véhicules, navires et sous-marins. Il peut apponter sur le porte-avions britannique."),
"HELI": ("Longbow", """Hélicoptère d'attaque allié armé de missiles polyvalents.
Il frappe les blindés, les bâtiments et même les aéronefs.
La plateforme de combat la plus polyvalente des Alliés.""",
"Frappez les blindés et les bâtiments. Évitez l'infanterie antiaérienne et les SAM."),
"KIROV": ("Dirigeable Kirov", """Dirigeable blindé turc de la carte WW3, chargé de bombes massives.
Lent, il avance comme une menace inévitable vers la base ennemie.
Quand il arrive, il est souvent trop tard.""",
"Escortez-le vers la base ennemie en neutralisant les défenses antiaériennes. Très résistant, mais très lent."),
"KZO": ("KZO", """Drone de reconnaissance allemand à longue portée.
Très rapide, il peut rester stationnaire au-dessus d'une zone.
L'œil du PzH 2000.""",
"Fournissez la vision au PzH 2000 et à l'artillerie allemande. Très fragile : gardez-le loin des défenses antiaériennes."),
"LANCET": ("ZALA Lancet", """Munition rôdeuse russe qui fonce sur sa cible et explose.
Elle est spécialisée contre l'artillerie et les véhicules légers.
Un char lourd survit à un Lancet ; une artillerie, rarement.""",
"Chassez l'artillerie et les véhicules de soutien ennemis. Contre les chars lourds, utilisez-en plusieurs."),
"LUNA": ("LUNA X-2000", """Drone allemand de désignation laser.
Tant qu'il garde une cible en vue, celle-ci subit +25 % de dégâts.
Il ne tue pas, il fait tuer.""",
"Désignez la cible prioritaire (char lourd, défense) pendant que vos Leopard et PzH la frappent."),
"MH60": ("Black Hawk", """Hélicoptère d'attaque allié armé de mitrailleuses.
Il déchire l'infanterie et les véhicules légers.
Un classique des guerres modernes.""",
"Chassez l'infanterie et les véhicules légers. Évitez les chars et l'antiaérien."),
"MI24": ("Mi-24", """Hélicoptère d'attaque ukrainien à deux mitrailleuses.
Il peut apponter sur le porte-hélicoptères.
Le « char volant » de la guerre froide.""",
"Chassez l'infanterie et les blindés légers. Utilisez le porte-hélicoptères comme base flottante."),
"MI26": ("Halo", """Hélicoptère de transport lourd américain de la carte WW3.
Il transporte des véhicules entiers au-dessus des obstacles.
Furtif, il se glisse derrière les lignes.""",
"Transportez des véhicules derrière les lignes ennemies. Il n'est pas armé : évitez l'antiaérien."),
"MIG": ("MiG", """Avion d'attaque soviétique rapide, armé de missiles air-sol.
Il frappe les bâtiments et les véhicules avant de rentrer se réarmer.
Il peut apponter sur les porte-avions russe et chinois.""",
"Frappez les bâtiments et véhicules isolés. Évitez les zones couvertes d'antiaérien."),
"NHAW": ("Chrono Nighthawk", """Hélicoptère de transport allemand de la carte WW3, équipé d'un canon chronosphérique.
Il transporte de l'infanterie et saute d'un point à l'autre.
Le transport le plus surprenant du jeu.""",
"Téléportez de l'infanterie derrière les lignes ennemies pour des raids surprises."),
"ORION": ("Orion", """Drone lourd russe armé de missiles air-sol.
Il lui faut plusieurs passages pour détruire un char lourd.
Le premier grand drone armé russe.""",
"Frappez les véhicules, l'artillerie et les bâtiments légers. Évitez l'antiaérien : il est lent et cher."),
"ORLAN10": ("Orlan-10", """Drone de reconnaissance russe bon marché.
Il guide l'artillerie : les véhicules alliés proches gagnent 15 % de portée.
L'œil omniprésent du front russe.""",
"Placez-le au-dessus de votre artillerie pour augmenter sa portée. Bon marché : remplaçable."),
"PATROLLER": ("Patroller", """Drone tactique français d'appui aux blindés.
Ses roquettes guidées laser frappent par paires ; il étend la portée des véhicules alliés.
L'escorte aérienne des blindés français.""",
"Accompagnez vos blindés : +15 % de portée pour les véhicules proches et liaison SCORPION pour les Leclerc."),
"PROTECTOR": ("Protector RG Mk1", """Drone armé britannique de harcèlement.
Il tire des salves de deux missiles légers guidés.
Il use l'ennemi à distance, lentement mais sûrement.""",
"Harcelez les véhicules légers et l'infanterie. Évitez l'antiaérien."),
"RAFALE": ("Rafale", """Avion de combat multirôle français.
Il porte des missiles air-air, air-sol et des torpilles.
Il peut apponter sur le porte-avions nucléaire.""",
"Frappez les véhicules, navires et sous-marins, et combattez l'aviation ennemie. Réarmez-le sur le porte-avions."),
"RAH": ("Comanche", """Hélicoptère d'attaque furtif français de la carte WW3.
Il approche sans être vu et frappe avec des roquettes puissantes.
L'arme idéale pour les frappes surprises.""",
"Frappez les cibles clés par surprise grâce à sa furtivité."),
"REAPER": ("MQ-9 Reaper", """Drone MALE français armé de bombes guidées et de missiles.
Sa caméra thermique détecte les unités furtives.
Il frappe loin et haut, là où l'ennemi ne le voit pas.""",
"Frappez les véhicules et bâtiments à distance, détectez les unités furtives. Limité à 2 exemplaires."),
"SEAGUARDIAN": ("MQ-9B SeaGuardian", """Drone japonais de patrouille maritime et terrestre.
Il désigne les cibles au laser et détecte les sous-marins.
L'œil qui voit à travers la mer.""",
"Désignez la cible prioritaire (+25 % de dégâts) et détectez les sous-marins. Non armé."),
"SHARK": ("Shark", """Drone de reconnaissance stratégique ukrainien.
Sa vision énorme marque les blindés chenillés ennemis pour toute l'armée.
Il transforme chaque char ennemi en cible visible.""",
"Survolez les concentrations blindées ennemies pour les marquer, puis frappez avec l'artillerie et les FPV."),
"SUK": ("Sukhoï", """Chasseur russe de la carte WW3, spécialisé dans la chasse aux hélicoptères.
Ses missiles air-air ne laissent aucune chance aux aéronefs ennemis.
Il ne frappe pas le sol.""",
"Chassez l'aviation ennemie, en particulier les hélicoptères. Inutile contre les unités au sol."),
"TAPAS": ("TAPAS BH-201", """Drone de reconnaissance indien à longue endurance.
Sa vision énorme guide l'artillerie : +15 % de portée pour les véhicules proches.
L'œil de l'artillerie indienne.""",
"Placez-le au-dessus de vos Dhanush et NAMICA pour augmenter leur portée. Très fragile."),
"TRAN": ("Chinook", """Hélicoptère de transport lourd des Alliés.
Il transporte huit fantassins au-dessus des obstacles.
L'outil des débarquements rapides.""",
"Transportez l'infanterie derrière les lignes ennemies ou vers des positions isolées."),
"UAV": ("Drone de reconnaissance", """Drone de reconnaissance français de la carte WW3.
Il survole le champ de bataille sans être vu.
Un œil dans le ciel, très résistant.""",
"Explorez le champ de bataille et détectez les mouvements ennemis."),
"UDRN": ("Leleka-100", """Drone de reconnaissance ukrainien bon marché.
Excellente vision : il guide l'artillerie, notamment le M777.
Il a changé la guerre de l'artillerie.""",
"Fournissez la vision au M777 pour ses tirs de précision. Bon marché : remplaçable."),
"WATCHKEEPER": ("Watchkeeper WK450", """Drone de surveillance britannique.
Il transmet les coordonnées : +15 % de portée pour les véhicules proches.
Il orbite au-dessus de la zone sans relâche.""",
"Placez-le au-dessus de votre artillerie et de vos chars pour augmenter leur portée."),
"YAK": ("Yak", """Avion d'attaque soviétique armé de mitrailleuses.
Il déchire l'infanterie et les véhicules légers.
Rapide et bon marché, il vit dangereusement.""",
"Chassez l'infanterie et les véhicules légers. Évitez les chars et l'antiaérien."),
"apache": ("Apache", """Hélicoptère d'attaque américain, l'un des plus redoutés au monde.
Missiles Hellfire, canon et missiles antiaériens : il frappe tout.
Aucune cible ne lui échappe vraiment.""",
"Unité polyvalente : frappez blindés, infanterie et aéronefs. Évitez l'antiaérien lourd."),
# ------------------------------------------------------------------ MARINE
"CA": ("Croiseur", """Croiseur lourd des Alliés, armé de canons de 8 pouces à très longue portée.
Il pilonne les côtes et les bases à 20 cases.
Lent, il est la cible favorite des sous-marins.""",
"Pilonnez les bases côtières à distance. Escortez-le avec des destroyers contre les sous-marins."),
"CA.Prism": ("Croiseur prisme", """Croiseur espagnol de la carte WW3, armé d'un canon prisme.
Il frappe les cibles terrestres avec un rayon puissant.
Lent, il domine pourtant les côtes.""",
"Pilonnez les côtes et les bases ennemies. Escortez-le contre les sous-marins."),
"DD": ("Destroyer", """Destroyer polyvalent des Alliés.
Il détecte les sous-marins et frappe les navires, les véhicules et les aéronefs.
L'escorte indispensable de toute flotte.""",
"Protégez votre flotte contre les sous-marins et l'aviation. Détectez les sous-marins ennemis."),
"DD2": ("Frégate", """Frégate britannique de la carte WW3, armée d'un canon, de flak et de grenades anti-sous-marines.
Elle combat sur mer, sur terre et dans les airs.
La frégate la plus polyvalente des mers.""",
"Escortez votre flotte : elle gère navires, sous-marins et aéronefs."),
"LST": ("Navire de débarquement", """Navire de transport polyvalent, capable de transporter infanterie et véhicules.
Il débarque des armées entières sur les plages ennemies.
Sa capacité a été portée à 25 places.""",
"Débarquez des troupes sur les côtes ennemies, loin des défenses. Escortez-le."),
"MSUB": ("Sous-marin lance-missiles", """Sous-marin soviétique armé de missiles de siège à longue portée.
Il frappe les bases ennemies depuis la mer.
Il détecte aussi les autres sous-marins.""",
"Pilonnez les bases côtières ennemies. Évitez les destroyers."),
"NGG": ("Navire générateur de brouillard", """Navire britannique générateur de brouillard.
Il cache la flotte ennemie dans le brouillard de guerre.
La mer devient aveugle.""",
"Cachez votre flotte à l'approche des côtes ennemies."),
"PACN": ("Porte-avions Shandong", """Porte-avions chinois dérivé de la classe Kouznetsov.
Il embarque cinq MiG et les réarme en mer.
La Chine peut en aligner jusqu'à quatre.""",
"Projetez la puissance aérienne loin de vos bases. Escortez-le contre les sous-marins."),
"PAN": ("Porte-avions nucléaire", """Porte-avions français à propulsion nucléaire.
Il embarque huit Rafale et les réarme en mer.
Sa destruction provoque une grande explosion du réacteur.""",
"Projetez vos Rafale partout sur la carte. Escortez-le absolument contre les sous-marins."),
"PARU": ("Porte-avions Amiral Kouznetsov", """Porte-avions russe.
Il embarque cinq MiG et les réarme en mer.
La puissance aérienne russe à la mer.""",
"Projetez vos MiG loin des aérodromes. Escortez-le contre les sous-marins."),
"PAUK": ("Porte-avions classe Queen Elizabeth", """Porte-avions britannique.
Il embarque cinq Harrier et les réarme en mer.
La Royal Navy retrouve sa puissance aérienne.""",
"Projetez vos Harrier loin de vos bases. Escortez-le contre les sous-marins."),
"PAUS": ("Porte-avions classe Gerald R. Ford", """Supercarrier américain à propulsion nucléaire.
Il embarque huit F-22 et les réarme en mer.
Les USA peuvent en aligner jusqu'à cinq.""",
"Projetez vos F-22 partout sur la carte. Escortez-le contre les sous-marins."),
"PHUA": ("Porte-hélicoptères", """Porte-hélicoptères ukrainien, moins cher et moins résistant qu'un porte-avions.
Il embarque quatre Mi-24 et les réarme en mer.
Une base flottante pour les hélicoptères.""",
"Utilisez vos Mi-24 depuis la mer contre l'infanterie côtière. Escortez-le."),
"PT": ("Vedette", """Vedette rapide des Alliés.
Elle détecte les sous-marins et frappe les navires légers.
Rapide et bon marché, elle patrouille les côtes.""",
"Patrouillez les côtes et détectez les sous-marins."),
"SEAM": ("Mammouth des mers", """Grand sous-marin russe de la carte WW3, armé de torpilles et de missiles.
Il combine la puissance d'un sous-marin et d'un Mammouth.
Lent, mais très dangereux.""",
"Frappez les flottes et les cibles côtières ennemies depuis les profondeurs."),
"SMNLY": ("Poseur de mines naval", """Navire poseur de mines marines.
Il détecte les sous-marins et les mines.
Il transforme la mer en champ de mines.""",
"Minez les accès maritimes à votre base et les routes des flottes ennemies."),
"SNLE": ("Sous-marin nucléaire lanceur d'engins", """Sous-marin nucléaire capable de tirer une frappe nucléaire depuis sa position.
Il est armé de torpilles lourdes pour se défendre.
La dissuasion qui ne dort jamais.""",
"Gardez-le furtif et loin des destroyers ; utilisez sa frappe nucléaire depuis une position sûre. Limité à 3 exemplaires."),
"SNLE.FRANCE": ("Sous-marin nucléaire lanceur d'engins (France)", """Version française du SNLE, la dissuasion française.
Identique aux autres, mais la France peut en aligner cinq.
La force de frappe océanique française.""",
"Même emploi que le SNLE ; la France peut en aligner 5 pour multiplier les frappes nucléaires."),
"SS": ("Sous-marin", """Sous-marin d'attaque soviétique armé de torpilles.
Il frappe les navires ennemis depuis les profondeurs.
Il détecte aussi les autres sous-marins.""",
"Chassez les navires ennemis, en particulier les porte-avions et croiseurs. Évitez les destroyers."),
}
