# Bâtiments et défenses : clé de l'acteur -> (nom en français, lore sur 3 lignes, stratégie)
TEXTES = {
# ------------------------------------------------------------------ BÂTIMENTS
"ABASE": ("Base aérienne", """Base aérienne américaine de la carte WW3.
Elle produit et réarme les avions ; elle ouvre aussi les largages de snipers et les frappes aériennes.
Le cœur de la puissance aérienne américaine.""",
"Construisez-la tôt pour débloquer l'A-10 et le F-22. Protégez-la avec des défenses antiaériennes."),
"AFLD": ("Aérodrome", """Aérodrome soviétique qui produit et réarme les avions.
Il débloque l'avion espion, les parachutistes et les parabombes.
Le ciel soviétique commence ici.""",
"Construisez-le pour les MiG et Yak et pour ses pouvoirs de soutien. Protégez-le avec des SAM."),
"AFLD.Ukraine": ("Aérodrome ukrainien", """Aérodrome ukrainien, identique à l'aérodrome soviétique.
Il produit les aéronefs ukrainiens, dont le Mi-24.
La base de l'aviation ukrainienne.""",
"Même emploi que l'aérodrome soviétique ; il produit les Mi-24 et les drones ukrainiens."),
"APWR": ("Centrale avancée", """Centrale électrique produisant le double d'une centrale standard.
Elle alimente les bâtiments avancés et les superarmes.
Une cible de choix pour les espions ennemis.""",
"Remplacez vos centrales standard pour économiser de la place. Protégez-les : sans courant, défenses et pouvoirs s'arrêtent."),
"ATEK": ("Centre technique allié", """Centre de recherche des Alliés.
Il débloque les unités avancées et le satellite GPS.
Le cerveau de l'armée alliée.""",
"Construisez-le pour débloquer les unités de haut niveau et le satellite GPS."),
"BARR": ("Caserne soviétique", """Caserne où sont formés les fantassins soviétiques.
Elle forme l'infanterie de base et les spécialistes.
Le point de départ de toute armée soviétique.""",
"Construisez-la tôt ; plusieurs casernes accélèrent la production d'infanterie."),
"CTEK": ("Centre technique chinois", """Centre de recherche chinois de la carte WW3.
Il débloque les unités avancées chinoises et le largage de chars.
L'industrie chinoise au service de la guerre.""",
"Construisez-le pour l'Overlord, le hacker et le largage de chars."),
"DOME": ("Radar Dome", """Radar qui fournit une vue d'ensemble du champ de bataille.
Il débloque les unités avancées et les bâtiments nationaux.
Sans radar, une armée combat à l'aveugle.""",
"Indispensable : il débloque la minicarte et la plupart des unités avancées. Protégez-le du brouillage SAS."),
"ETEK": ("Centre technique britannique", """Centre de recherche britannique de la carte WW3.
Il débloque les unités avancées britanniques, le GPS et l'impulsion sonar.
La science au service de la Couronne.""",
"Construisez-le pour le Royal Marine, la forteresse de bataille et l'impulsion sonar."),
"FIX": ("Service Depot", """Atelier de réparation des véhicules.
Il répare les véhicules contre des crédits.
Une armée réparée vaut deux armées.""",
"Placez-le près du front pour réparer rapidement vos chars (et recharger l'ERA des T-90M)."),
"FTEK": ("Centre technique français", """Centre de recherche français de la carte WW3, camouflé.
Il débloque les unités avancées françaises et le GPS.
Il est invisible aux yeux de l'ennemi.""",
"Construisez-le pour le char Mirage, le Comanche, le Grand Canon et le générateur de phase."),
"GCHQ": ("Station SIGINT (GCHQ Forward)", """Station britannique d'interception et de guerre électronique.
Elle porte le brouillage SAS, qui aveugle radar et pouvoirs ennemis.
Cible stratégique : détruite ou hors tension, le brouillage est suspendu.""",
"Construisez-la pour le brouillage SAS, à utiliser juste avant un assaut. Protégez-la : sans elle, pas de brouillage."),
"GRTEK": ("Centre technique grec", """Centre de recherche grec de la carte WW3.
Il débloque les hoplites, les armures Spartan et le Titan.
La technologie des armures de puissance.""",
"Construisez-le pour les unités d'élite grecques et le largage de Spartan."),
"GTEK": ("Centre technique allemand", """Centre de recherche allemand de la carte WW3.
Il débloque les unités avancées allemandes, le GPS et le chronoshift avancé.
L'ingénierie allemande dans toute sa splendeur.""",
"Construisez-le pour le soldat Chrono, le Chrono Nighthawk et le chasseur de chars."),
"HPAD": ("Héliport", """Héliport qui produit et réarme les hélicoptères.
Il débloque les hélicoptères alliés.
La base de l'aviation légère alliée.""",
"Construisez-le pour les hélicoptères et les drones. Protégez-le avec des défenses antiaériennes."),
"INDP": ("Usine industrielle", """Usine chinoise qui accélère et réduit le coût de production des véhicules.
Elle débloque l'industrialisation, un flux de chars lourds.
L'industrie comme arme de guerre.""",
"Construisez-la pour produire vos véhicules 15 % plus vite et 10 % moins cher."),
"INTERNET": ("Centre Internet", """Centre chinois où les hackers volent de l'argent.
Plus il contient de hackers, plus il rapporte.
La guerre économique à l'ère numérique.""",
"Placez-y des hackers pour générer des crédits. Protégez-le."),
"JPEW": ("Centre de guerre électronique", """Centre japonais de guerre électronique.
Il porte le brouillage japonais, qui réduit la portée ennemie.
Cible stratégique : détruit ou hors tension, le brouillage est suspendu.""",
"Construisez-le pour le brouillage japonais, à utiliser pour casser un assaut ennemi. Protégez-le."),
"KENN": ("Chenil", """Chenil où sont dressés les chiens d'attaque soviétiques.
Il forme les chiens qui traquent l'infanterie et les espions.
La sécurité de la base soviétique.""",
"Construisez-le tôt pour protéger votre base contre les espions."),
"PCAWACS": ("PC de liaison ISR et AWACS", """Poste de commandement ukrainien relié aux flux AWACS et drones.
Il porte le renseignement OTAN (AWACS).
Cible stratégique : détruit ou hors tension, l'AWACS est suspendu.""",
"Construisez-le pour l'AWACS, à utiliser avant une frappe d'artillerie ou de FPV. Protégez-le."),
"PCSCALP": ("Centre de commandement SCALP", """Bunker français de guidage des frappes de croisière.
Il reçoit les désignations laser des commandos GCP.
Cible stratégique : détruit ou hors tension, la frappe SCALP est suspendue.""",
"Construisez-le pour la frappe SCALP. Son blindage béton le rend résistant ; protégez-le quand même."),
"PCTOS": ("PC d'appui thermobarique", """Casemate russe d'état-major et dépôt de munitions thermobariques.
Elle porte la frappe thermobarique TOS-1A.
Cible stratégique : détruite ou hors tension, la frappe TOS-1A est suspendue.""",
"Construisez-le pour la frappe TOS-1A. Très résistant (béton, 150 000 PV)."),
"PINAKA": ("PC du régiment Pinaka", """PC et parc du régiment de lance-roquettes Pinaka indien.
Il porte le barrage Pinaka.
Cible stratégique : détruit ou hors tension, le barrage est suspendu.""",
"Construisez-le pour le barrage Pinaka, à utiliser contre l'infanterie groupée. Protégez-le."),
"PIONIER": ("Pionierzentrum", """Centre allemand de génie lourd et de franchissement.
Il porte le pontage tactique rapide.
Cible stratégique : détruit ou hors tension, le pontage est suspendu.""",
"Construisez-le pour le pontage tactique, qui permet de franchir une rivière défendue."),
"POWR": ("Centrale", """Centrale électrique de base.
Elle alimente les bâtiments et les défenses.
Sans elle, rien ne fonctionne.""",
"Construisez-en plusieurs en début de partie ; remplacez-les ensuite par des centrales avancées."),
"PROC": ("Raffinerie", """Raffinerie qui transforme le minerai et les gemmes en crédits.
Elle est livrée avec un camion de minerai.
Le cœur de l'économie.""",
"Construisez-en deux ou trois près des champs de minerai. Protégez-les : elles sont la cible favorite des raids."),
"RTEK": ("Centre technique russe", """Centre de recherche russe de la carte WW3.
Il produit de l'énergie et débloque les unités avancées russes.
La puissance russe dans toute sa splendeur.""",
"Construisez-le pour le Mammouth Tesla, le Sukhoï et le Tesla avancé. Il produit aussi de l'énergie."),
"SHPAD": ("Héliport soviétique", """Héliport soviétique de la carte WW3.
Il produit et réarme les hélicoptères et le dirigeable Kirov.
La base de l'aviation turque.""",
"Construisez-le pour le dirigeable Kirov."),
"SOVPWR": ("Centrale nucléaire", """Centrale nucléaire soviétique de la carte WW3.
Elle produit quatre fois plus qu'une centrale avancée, mais explose violemment.
Une source d'énergie à double tranchant.""",
"Construisez-la loin des bâtiments importants : sa destruction provoque une grosse explosion."),
"SPEN": ("Base sous-marine", """Base sous-marine soviétique.
Elle produit et répare les sous-marins et les transports.
La marine soviétique commence ici.""",
"Construisez-la pour les sous-marins, qui dominent les flottes alliées."),
"SPTEK": ("Centre technique espagnol", """Centre de recherche espagnol de la carte WW3.
Il débloque les unités prisme et la prise de contrôle hostile.
La technologie espagnole au service de la guerre.""",
"Construisez-le pour le Conquistador, les unités à coussin d'air et la prise de contrôle hostile."),
"STEK": ("Centre technique soviétique", """Centre de recherche soviétique.
Il débloque les unités avancées soviétiques.
Le cerveau de l'armée soviétique.""",
"Construisez-le pour le Mammouth, le char Tesla et le Rideau de fer."),
"SYRD": ("Chantier naval", """Chantier naval allié.
Il produit et répare les navires et les transports.
La marine alliée commence ici.""",
"Construisez-le pour les destroyers, croiseurs et porte-avions."),
"TENT": ("Caserne alliée", """Caserne où sont formés les fantassins alliés.
Elle forme l'infanterie de base et les spécialistes.
Le point de départ de toute armée alliée.""",
"Construisez-la tôt ; plusieurs casernes accélèrent la production d'infanterie."),
"TTEK": ("Centre technique turc", """Centre de recherche turc de la carte WW3.
Il débloque les unités avancées turques et les insurgés.
La subversion comme arme.""",
"Construisez-le pour le Kirov, le camion toxique et les insurgés."),
"USTEK": ("Centre technique américain", """Centre de recherche américain de la carte WW3.
Il débloque les unités avancées américaines, le GPS et le canon à ions.
La puissance technologique américaine.""",
"Construisez-le pour l'Apache, le commando, le Patriot et le canon à ions."),
"UTEK": ("Centre technique ukrainien", """Centre de recherche ukrainien de la carte WW3.
Il débloque les unités avancées ukrainiennes et le Rideau de fer avancé.
La technologie soviétique ukrainienne.""",
"Construisez-le pour le char Apocalypse, le char de siège et le Rideau de fer avancé."),
"WEAP": ("Usine d'armement", """Usine qui produit tous les véhicules.
Elle est au cœur de toute armée mécanisée.
Une usine détruite, c'est une armée qui cesse de grandir.""",
"Construisez-en plusieurs pour accélérer la production de véhicules. Protégez-les."),
# ------------------------------------------------------------------ DÉFENSES
"AGUN": ("Canon antiaérien", """Défense antiaérienne des Alliés.
Elle crible le ciel d'obus explosifs.
Elle ne tire que sur les aéronefs.""",
"Placez-en près de vos bâtiments clés contre les raids aériens."),
"BRIK": ("Mur en béton", """Mur en béton qui bloque les unités et les tirs ennemis.
Seuls les chars les plus lourds peuvent l'écraser.
Le mur le plus solide du jeu.""",
"Protégez vos défenses et bâtiments clés, canalisez les assauts ennemis."),
"CRAM": ("Canon Gatling", """Défense antiaérienne chinoise à canon rotatif.
Sa cadence infernale déchire les aéronefs.
La réponse chinoise à l'aviation ennemie.""",
"Placez-en près de vos bâtiments clés contre l'aviation et les drones."),
"FENC": ("Clôture barbelée", """Clôture en fil barbelé.
Elle arrête l'infanterie et les véhicules légers, mais les chars l'écrasent.
Bon marché, elle ralentit l'ennemi.""",
"Canalisez l'infanterie ennemie vers vos défenses."),
"FTUR": ("Tour lance-flammes", """Tour défensive soviétique équipée d'un lance-flammes.
Elle incendie l'infanterie et les véhicules légers ; elle détecte les unités furtives.
La terreur de l'infanterie.""",
"Placez-en aux accès de votre base contre l'infanterie."),
"GAP": ("Générateur de brouillard", """Générateur qui cache la base alliée dans le brouillard de guerre.
L'ennemi ne voit plus ce qui s'y passe.
La discrétion comme défense.""",
"Cachez vos bâtiments clés et vos mouvements de troupes."),
"GUN": ("Tourelle", """Tourelle antichar des Alliés.
Elle frappe les véhicules et détecte les unités furtives.
La défense antichar de base.""",
"Placez-en aux accès de votre base contre les véhicules."),
"HBOX": ("Pillbox camouflé", """Pillbox camouflé, invisible à distance.
Il abrite un fantassin qui tire depuis l'intérieur ; il détecte les unités furtives.
Une embuscade permanente.""",
"Placez-y une équipe NLAW pour un tir d'embuscade dévastateur, invisible."),
"HGATE": ("Porte horizontale", """Porte qui s'ouvre automatiquement pour les unités amies.
Elle bloque l'accès ennemi à votre base.
La porte d'entrée de votre forteresse.""",
"Placez-la dans vos murs pour laisser passer vos troupes."),
"HTUR": ("Grand Canon", """Artillerie défensive française de la carte WW3, aux proportions épiques.
Elle frappe les véhicules et l'infanterie à 10 cases.
La défense la plus impressionnante du jeu.""",
"Placez-le au centre de votre base pour couvrir une large zone."),
"IRON": ("Rideau de fer", """Superarme soviétique qui rend un groupe d'unités invulnérable.
Pendant 20 secondes, rien ne peut les toucher.
La peur de l'ennemi est sa meilleure alliée.""",
"Utilisez-le sur un groupe de chars pour un assaut décisif. Limité à 1."),
"MSLO": ("Silo à missiles", """Silo qui abrite une bombe atomique.
La superarme la plus destructrice du jeu.
Un silo construit, c'est une menace qui pèse sur toute la partie.""",
"Frappez la base ennemie, idéalement ses bâtiments clés. Protégez-le : il est la cible prioritaire de l'ennemi. Limité à 1."),
"MTSLA": ("Tesla avancée", """Défense Tesla avancée russe de la carte WW3.
Ses arcs électriques frappent tout ce qui s'approche, à cadence très élevée.
La défense la plus puissante de la Russie.""",
"Placez-en aux accès de votre base. Très gourmande en énergie (-300)."),
"PATRIOT": ("Missiles Patriot", """Défense américaine de la carte WW3, qui tire par-dessus les murs.
Elle frappe les véhicules et l'infanterie à 10 cases.
La défense américaine par excellence.""",
"Placez-en derrière vos murs pour couvrir une large zone."),
"PBOX": ("Pillbox", """Pillbox en béton.
Il abrite un fantassin qui tire depuis l'intérieur ; il détecte les unités furtives.
La défense de base de l'infanterie.""",
"Placez-y une équipe NLAW pour un tir d'embuscade dévastateur."),
"PDOX": ("Chronosphère", """Superarme alliée qui téléporte un groupe d'unités.
Pendant 20 secondes, les unités sont transportées n'importe où.
Le pouvoir de choisir le lieu de la bataille.""",
"Téléportez un groupe de chars au cœur de la base ennemie. Limité à 1."),
"PRIS": ("Tour prisme", """Défense prisme espagnole de la carte WW3.
Son rayon frappe tout ce qui s'approche.
La défense la plus avancée de l'Espagne.""",
"Placez-en aux accès de votre base ; elles couvrent une large zone."),
"PROP": ("Tour de propagande", """Tour de propagande chinoise de la carte WW3.
Elle améliore les capacités des troupes amies à portée.
La propagande comme multiplicateur de force.""",
"Placez-la près de vos défenses pour les renforcer."),
"RAILTURR": ("Tourelle à rail", """Tourelle antichar allemande de la carte WW3, armée d'un canon à rail.
Elle tire par-dessus les murs.
La défense antichar la plus puissante.""",
"Placez-en derrière vos murs contre les chars."),
"SAM": ("Site SAM", """Défense antiaérienne soviétique.
Ses missiles abattent les aéronefs à longue distance.
Le ciel soviétique est gardé.""",
"Placez-en près de vos bâtiments clés contre l'aviation."),
"SBAG": ("Mur de sacs de sable", """Mur de sacs de sable.
Il arrête l'infanterie et les véhicules légers, mais les chars l'écrasent.
Bon marché, il ralentit l'ennemi.""",
"Canalisez l'infanterie ennemie vers vos défenses."),
"SILO": ("Silo de stockage", """Silo qui stocke le minerai raffiné en excès.
Sans silos, les raffineries s'arrêtent quand leur capacité est pleine.
Le coffre-fort de votre économie.""",
"Construisez-en quand vos raffineries sont pleines. Protégez-les des voleurs."),
"STHGEN": ("Générateur de phase", """Superarme française de la carte WW3.
Elle rend un groupe d'unités invisible pendant 30 secondes.
Une armée invisible frappe là où elle veut.""",
"Rendez invisible un groupe d'unités pour un assaut surprise. Limité à 1."),
"TRANCHEE": ("Tranchée (est-ouest)", """Tranchée creusée par le génie français.
Elle abrite quatre fantassins qui tirent à couvert.
Elle se construit n'importe où, près d'un ingénieur militaire déployé.""",
"Construisez-en sur les positions avancées avec un ingénieur militaire déployé. Pas besoin d'électricité."),
"TRANCHEEV": ("Tranchée (nord-sud)", """Même tranchée, orientée nord-sud.
Elle abrite quatre fantassins qui tirent à couvert.
Elle se construit près d'un ingénieur militaire déployé.""",
"Même emploi que la tranchée est-ouest ; choisissez l'orientation selon le terrain."),
"TSLA": ("Bobine Tesla", """Défense Tesla soviétique.
Ses arcs électriques frappent les véhicules et l'infanterie ; elle détecte les unités furtives.
La défense emblématique des Soviétiques.""",
"Placez-en aux accès de votre base. Elle consomme beaucoup d'énergie (-100)."),
"VGATE": ("Porte verticale", """Porte qui s'ouvre automatiquement pour les unités amies.
Elle bloque l'accès ennemi à votre base.
La porte d'entrée de votre forteresse.""",
"Placez-la dans vos murs pour laisser passer vos troupes."),
# ------------------------------------------------------------------ LEURRES
"ATEF": ("Faux centre technique allié", """Leurre qui ressemble à un centre technique allié.
Il attire le feu ennemi loin de vos vrais bâtiments.
L'art de la tromperie.""",
"Placez-le pour attirer les frappes ennemies (espions, superarmes) loin de votre vrai centre technique."),
"DOMF": ("Faux Radar Dome", """Leurre qui ressemble à un Radar Dome.
Il attire le feu ennemi loin de vos vrais bâtiments.
L'art de la tromperie.""",
"Attirez les frappes ennemies loin de votre vrai radar."),
"FACF": ("Faux chantier de construction", """Leurre qui ressemble à un chantier de construction.
Il attire le feu ennemi loin de vos vrais bâtiments.
L'art de la tromperie.""",
"Attirez les frappes ennemies loin de votre vrai chantier de construction."),
"FAPW": ("Fausse centrale avancée", """Leurre qui ressemble à une centrale avancée.
Il attire le feu ennemi loin de vos vrais bâtiments.
L'art de la tromperie.""",
"Attirez les frappes ennemies loin de vos vraies centrales."),
"FIXF": ("Faux Service Depot", """Leurre qui ressemble à un Service Depot.
Il attire le feu ennemi loin de vos vrais bâtiments.
L'art de la tromperie.""",
"Attirez les frappes ennemies loin de votre vrai Service Depot."),
"FPWR": ("Fausse centrale", """Leurre qui ressemble à une centrale.
Il attire le feu ennemi loin de vos vrais bâtiments.
L'art de la tromperie.""",
"Attirez les frappes ennemies loin de vos vraies centrales."),
"MSLF": ("Faux silo à missiles", """Leurre qui ressemble à un silo à missiles.
Il attire le feu ennemi loin de vos vrais bâtiments.
Il fait craindre une frappe nucléaire qui n'existe pas.""",
"Faites croire à l'ennemi que vous avez une bombe atomique, pour qu'il gaspille ses ressources à la chercher."),
"PDOF": ("Fausse Chronosphère", """Leurre qui ressemble à une Chronosphère.
Il attire le feu ennemi loin de vos vrais bâtiments.
L'art de la tromperie.""",
"Attirez les frappes ennemies loin de votre vraie Chronosphère."),
"SYRF": ("Faux chantier naval", """Leurre qui ressemble à un chantier naval.
Il attire le feu ennemi loin de vos vrais bâtiments.
L'art de la tromperie.""",
"Attirez les frappes ennemies loin de votre vrai chantier naval."),
"TENF": ("Fausse caserne alliée", """Leurre qui ressemble à une caserne alliée.
Il attire le feu ennemi loin de vos vrais bâtiments.
L'art de la tromperie.""",
"Attirez les frappes ennemies loin de votre vraie caserne."),
"WEAF": ("Fausse usine d'armement", """Leurre qui ressemble à une usine d'armement.
Il attire le feu ennemi loin de vos vrais bâtiments.
L'art de la tromperie.""",
"Attirez les frappes ennemies loin de votre vraie usine d'armement."),
}
