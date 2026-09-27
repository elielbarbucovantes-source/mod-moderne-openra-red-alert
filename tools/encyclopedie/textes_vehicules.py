# Véhicules : clé de l'acteur -> (nom en français, lore sur 3 lignes, stratégie)
TEXTES = {
"1TNK": ("Char léger", """Premier blindé des Alliés, conçu pour la reconnaissance rapide des années 50.
Son canon de 25 mm n'impressionne plus personne, mais sa vitesse reste précieuse.
Les équipages disent qu'on ne le voit passer qu'une fois : à l'aller.""",
"Éclaireur et chasseur de blindés légers en début de partie. Harcelez les camions de minerai et fuyez tout char moyen ; ne l'engagez jamais contre l'infanterie antichar."),
"2TNK": ("Char moyen", """Char de bataille standard des Alliés, fiable et facile à produire en série.
Son canon de 90 mm a gagné plus de batailles que n'importe quelle superarme.
Le Leclerc et le Leopard lui doivent leur doctrine d'emploi.""",
"Colonne vertébrale d'une armée alliée à bas niveau technologique. Groupez-le par 6 à 8 avec quelques lance-roquettes pour tenir face aux chars lourds soviétiques."),
"2TNK.HOV": ("Char à coussin d'air", """Version espagnole du char moyen, soulevée par un coussin antigravité.
Il franchit l'eau comme la terre ferme et embarque un lanceur antiaérien.
La doctrine espagnole en fait le premier maillon de ses assauts amphibies.""",
"Attaquez par la mer ou par les rivières là où l'ennemi n'attend pas de blindés. Son antiaérien lui permet d'escorter seul une tête de pont contre les hélicoptères."),
"3TNK": ("Char lourd", """Char de bataille soviétique à double canon, héritier des grandes plaines d'Ukraine.
Plus lent que ses rivaux alliés, il encaisse et rend chaque coup deux fois.
Sa silhouette massive reste le symbole de la puissance blindée de l'Est.""",
"Char de ligne des Soviétiques : avancez en masse, laissez l'ennemi s'épuiser sur son blindage, et réparez entre deux vagues. Protégez-le de l'infanterie antichar avec des lance-flammes ou des chiens."),
"3TNK.china": ("Char lourd chinois", """Copie chinoise du char lourd soviétique, simplifiée pour la production de masse.
Moins résistant que l'original, il gagne un lance-flammes de caisse contre l'infanterie.
Pékin compte sur le nombre plus que sur la qualité de chaque exemplaire.""",
"Produisez-le en très grand nombre : il est moins cher que le char lourd soviétique et gère mieux l'infanterie. Noyez les défenses ennemies sous les vagues."),
"4TNK": ("Char Mammouth", """Monstre à double tube de 120 mm et lance-missiles, le plus lourd des blindés soviétiques.
Il écrase les murs de béton et abat les hélicoptères qui s'approchent trop.
Aucune armée ne l'arrête seul ; toutes les armées le craignent en groupe.""",
"Fer de lance d'un assaut final. Lent : accompagnez-le de réparations (mécaniciens, Service Depot proche) et d'unités rapides pour couvrir ses flancs contre l'artillerie."),
"4TNK.Hov": ("Mammouth à coussin d'air", """Le Mammouth adapté à la technologie antigravité espagnole.
Il garde son blindage colossal mais traverse désormais rivières et bras de mer.
Un débarquement de Mammouths flottants a de quoi glacer n'importe quel état-major.""",
"Utilisez les rivières et la côte pour frapper là où l'ennemi n'a pas de défenses lourdes. Plus rapide que le Mammouth classique, il pardonne un peu mieux les mauvais placements."),
"6TNK": ("Canon Inferno", """Artillerie chinoise à très longue portée, montée sur un châssis rapide.
Ses obus incendiaires transforment les quartiers ennemis en brasiers.
Fragile, elle n'existe que tant que personne ne la trouve.""",
"Tirez depuis l'arrière, sous couverture antiaérienne, sur les bases et l'infanterie. Déplacez-la après chaque salve : 11 000 PV ne survivent pas à une contre-attaque."),
"APC": ("Transport de troupes blindé", """Véhicule soviétique conçu pour amener cinq fantassins au contact sous le feu.
Sa mitrailleuse couvre le débarquement, son blindage fait le reste.
Les vétérans l'appellent « le cercueil qui roule », avec une certaine affection.""",
"Transportez ingénieurs, lance-flammes ou Tanya jusqu'aux bâtiments ennemis. Sa mitrailleuse ne sert qu'à nettoyer l'infanterie légère autour du point de débarquement."),
"APOC": ("Char Apocalypse", """Le blindé ultime de l'arsenal ukrainien de la carte WW3 : obus à l'uranium et missiles antiaériens.
Il est si lourd que les ponts le redoutent davantage que l'ennemi.
Sa simple apparition sur le radar suffit à faire reculer une offensive.""",
"Unité de percée tardive. Accompagnez-le d'artillerie et de drones de reconnaissance : sa lenteur en fait une cible pour l'aviation et les missiles à longue portée."),
"ARJUN": ("Arjun Mk1A", """Char de combat indien, fruit de décennies de développement national.
Lourd, fiable et robuste, il privilégie la solidité sur la sophistication.
C'est le char des longues campagnes, qui revient toujours du front.""",
"Char de ligne de l'Inde : formez des lignes compactes appuyées par les NAMICA à l'arrière. Lent, il doit être déplacé tôt vers les points chauds ; ne le lancez pas à la poursuite d'unités rapides."),
"ARTY": ("Artillerie", """Obusier automoteur allié de 155 mm, la pièce d'artillerie standard des années 50.
Ses obus portent à 12 cases et font trembler les bases soviétiques.
Mais il est aussi fragile qu'une jeep et le sait.""",
"Pilonnez défenses et infanterie depuis l'arrière, avec une vision fournie par des éclaireurs. Ne la laissez jamais sans escorte : n'importe quel char la détruit en deux tirs."),
"AS90": ("AS-90", """Obusier automoteur britannique, héritier de la tradition d'artillerie royale.
Portée, puissance et mobilité y sont dosées sans excès, à l'anglaise.
Ses équipages le considèrent comme le couteau suisse de la brigade.""",
"Artillerie polyvalente : placez-la derrière une ligne de Challenger et des NLAW en pillbox. Elle porte à 10 cases, ce qui suffit à pilonner les défenses sans s'exposer."),
"BATF": ("Forteresse de bataille", """Forteresse roulante britannique de la carte WW3, hérissée de tourelles.
Elle doit être équipée de fantassins pour tirer à pleine puissance.
Elle écrase les murs de béton et ne connaît aucun faible.""",
"Remplissez-la d'infanterie d'élite pour démultiplier sa puissance de feu. Utilisez-la comme bélier contre les défenses, en la faisant suivre par des unités de réparation."),
"BMPT": ("BMPT Terminator", """Véhicule russe d'appui aux chars, né des leçons du combat urbain.
Ses deux canons de 30 mm clouent l'infanterie au sol, ses missiles Ataka percent les blindés.
Il protège les T-90 de l'ennemi qu'ils redoutent le plus : le fantassin antichar.""",
"Placez-le au contact de vos chars : il neutralise l'infanterie antichar qui les menace. Son blindage réactif encaisse le premier missile ; réparez-le entre deux engagements."),
"BTR": ("BTR", """Transport de troupes russe à roues, amphibie et rapide.
Il amène huit fantassins là où la route s'arrête et où la rivière commence.
Son canon de 25 mm suffit à tenir à distance les véhicules légers.""",
"Transportez l'infanterie à travers les rivières pour des raids surprises. Évitez les chars : son rôle est le transport et la chasse aux blindés légers, pas le combat de ligne."),
"CHALLENGER": ("Challenger 3", """Char de combat britannique, spécialiste du combat urbain.
Ses obus à effet de souffle clouent l'infanterie sans raser les bâtiments qu'il doit tenir.
Son système de maintenance embarqué le remet en état quand il est gravement touché.""",
"Tenez les villes et les passages étroits : il encaisse, se répare seul sous 50 % et plaque l'infanterie ennemie. Laissez l'AS-90 s'occuper des bâtiments, qu'il endommage mal."),
"CSAR": ("Canon César", """Artillerie automotrice française sur camion, célèbre pour sa mobilité.
Elle tire trois obus en rafale puis quitte sa position avant la riposte.
La doctrine « tirer et disparaître » a été écrite pour elle.""",
"Tirez une salve puis déplacez-la : elle est très rapide (164) mais fragile. Idéale pour le harcèlement de bases, guidée par des GCP ou des drones."),
"CTNK": ("Char Chrono", """Char allemand de la carte WW3, équipé d'un téléporteur chronosphérique.
Il saute d'un point à l'autre du champ de bataille pour frapper là où on l'attend le moins.
Ses missiles antichar achèvent ce que la surprise a commencé.""",
"Téléportez-le derrière les lignes pour détruire l'artillerie ou les bâtiments clés, puis repliez-vous. Il est léger : évitez les combats prolongés."),
"DHANUSH": ("Dhanush", """Obusier indien de 155 mm, dérivé d'un canon suédois et produit localement.
Rustique et économique, il offre beaucoup de puissance pour son prix.
L'Inde en aligne des batteries entières là où d'autres en alignent deux.""",
"Achetez-en plusieurs et groupez-les en batterie, guidées par un TAPAS pour gagner en portée. Contre-batterie facile : changez de position si l'ennemi vous repère."),
"DTRK": ("Camion de démolition", """Camion bourré d'explosifs nucléaires, piloté par un conducteur qui ne reviendra pas.
Son blindage est ridicule ; sa charge ne l'est pas.
En Ukraine, on murmure qu'il s'agit plus d'une arme de dissuasion que d'un véhicule.""",
"Frappez les concentrations ennemies ou un bâtiment clé en profitant d'une diversion. Il meurt au moindre tir : faites-le passer par un chemin imprévu ou sous couverture de fumée."),
"EMPOR": ("Char Overlord", """Le plus gros char de la Chine, une forteresse équipée d'obus d'artillerie.
Un fantassin embarqué lui ajoute une arme : mitrailleuse, missiles, lance-flammes ou propagande.
Il avance lentement, mais rien ne l'arrête vraiment.""",
"Adaptez l'occupant à la menace : conscrit contre l'infanterie, soldat roquette contre l'aviation, hacker pour la propagande. Accompagnez-le d'antiaérien : l'aviation est sa grande faiblesse."),
"FTRK": ("Canon antiaérien mobile", """Canon de DCA soviétique monté sur camion.
Il crible le ciel d'obus explosifs et fauche aussi l'infanterie au sol.
Un compagnon indispensable de toute colonne soviétique.""",
"Escortez vos colonnes et vos bases avancées contre les hélicoptères et drones. Il est fragile : gardez-le derrière les chars."),
"GRAD": ("BM-21 Grad", """Lance-roquettes multiple russe, conçu pour saturer une zone plutôt que viser.
Ses quarante tubes font pleuvoir le feu sur tout ce qui n'est pas enterré.
L'artillerie la plus répandue au monde, et pour de bonnes raisons.""",
"Saturez infanterie et véhicules légers regroupés. Imprécis : visez les zones, pas les cibles isolées. Bon marché, il se remplace facilement."),
"GRIZZ": ("Char Grizzly", """Char de combat américain de la carte WW3, rapide et bien armé.
Il combine un canon de 90 mm et un lance-missiles antiaérien.
Il symbolise la doctrine américaine : polyvalence et production industrielle.""",
"Char polyvalent : il peut se défendre contre l'aviation légère. Utilisez-le en masse, soutenu par l'aviation américaine."),
"GTNK": ("Char Gatling", """Char chinois équipé d'un canon rotatif à tir ultra-rapide.
Sa cadence infernale déchire l'infanterie comme les aéronefs.
Il est la réponse de Pékin aux drones et aux hélicoptères ennemis.""",
"Escortez vos colonnes contre l'infanterie et l'aviation. Évitez les chars ennemis : son blindage léger ne tient pas."),
"HARV": ("Camion de minerai", """Le véhicule le plus important de toute partie, même si personne ne le dit.
Il collecte le minerai et les gemmes pour alimenter l'effort de guerre.
Blindé, lent et sans arme, il se contente de faire vivre l'économie.""",
"Protégez vos camions avant tout : chaque camion perdu, c'est la production qui s'arrête. Construisez-en 2 par raffinerie et placez des défenses près des champs de minerai."),
"HFTK": ("Char Dragon", """Char chinois équipé de deux lance-flammes lourds.
Il nettoie les tranchées, les bunkers et les rues d'un seul passage.
Un cauchemar pour l'infanterie retranchée.""",
"Envoyez-le contre l'infanterie retranchée et les bâtiments légers. Courte portée : couvrez son approche avec des chars lourds."),
"HOVHARV": ("Camion de minerai à coussin d'air", """Version espagnole du camion de minerai, capable de naviguer sur l'eau.
Il atteint les gisements des îles et des rivages inaccessibles aux autres.
Sa discrétion sur l'eau a sauvé plus d'une économie espagnole.""",
"Exploitez les champs de minerai isolés par l'eau que l'ennemi ne peut pas atteindre facilement."),
"HOWI": ("Obusier", """Obusier américain de 155 mm de la carte WW3.
Il pilonne l'ennemi à 12 cases avec la précision de l'artillerie moderne.
Sa puissance est celle de l'artillerie alliée, avec l'industrie américaine derrière.""",
"Même emploi que l'artillerie alliée : derrière la ligne, avec des éclaireurs. Protégez-le de l'aviation ennemie."),
"HUMM": ("Humvee", """Véhicule tout-terrain américain, emblème des guerres modernes.
Rapide, il transporte quatre fantassins et une mitrailleuse lourde.
Il ne gagne pas de bataille, mais il y arrive toujours le premier.""",
"Éclaireur rapide et transport d'infanterie : reconnaissance, raids contre les camions de minerai, déploiement rapide d'ingénieurs."),
"IFV": ("Véhicule de combat d'infanterie", """Transport modulaire allié de la carte WW3, dont l'arme dépend de son passager.
Un ingénieur le transforme en engin de réparation, un soldat roquette en lanceur antiaérien.
Sa polyvalence le rend imprévisible au combat.""",
"Changez l'occupant selon la menace : soldat roquette contre l'aviation, médecin pour soigner, sniper pour la longue portée. Furtif : idéal pour des embuscades."),
"ISU": ("Char de siège", """Artillerie lourde ukrainienne de la carte WW3, à obus à fragmentation.
Blindée comme un char, elle peut s'approcher des défenses sans craindre la riposte.
Chaque obus se disperse en sous-munitions sur la zone d'impact.""",
"Approchez des bases ennemies sous escorte et démolissez défenses et infanterie. Elle résiste mieux que les artilleries légères, mais reste lente."),
"JAGUAR": ("EBRC Jaguar", """Véhicule blindé français de reconnaissance et de combat, 6x6 rapide.
Ses missiles tire-et-oublie MMP frappent les blindés avant même d'être repérés.
Il incarne la doctrine française : voir, frapper, disparaître.""",
"Chassez les blindés en flanquement puis repliez-vous. Fragile : n'engagez pas l'infanterie ni les chars de face. Il active la liaison SCORPION des Leclerc proches."),
"JEEP": ("Ranger", """Jeep armée d'une mitrailleuse, éclaireur standard des Alliés.
Elle file sur les routes et emmène un fantassin dans les coins reculés.
Personne ne compte sur elle pour tenir une ligne ; tout le monde compte sur elle pour la trouver.""",
"Reconnaissance et harcèlement des camions de minerai. Évitez tout véhicule blindé ; elle est faite pour voir et fuir."),
"KATY": ("Katioucha", """Lance-roquettes turc de la carte WW3, héritier des « orgues de Staline ».
Ses salves à longue portée ravagent les défenses et l'infanterie.
Imprécis, il compense par le nombre de projectiles.""",
"Saturez les défenses et l'infanterie ennemies à distance. Très lent : planifiez sa position à l'avance et protégez-le."),
"LASHER": ("Char Lasher", """Char de combat turc de la carte WW3, combinant deux calibres.
Il cumule un canon de 90 mm et un double canon de 105 mm.
Robuste et bon marché, il porte l'essentiel des assauts turcs.""",
"Char de ligne turc : groupez-le avec des saboteurs et Crazy Ivan pour ouvrir les défenses. Il manque de réponse à l'aviation."),
"LATNK": ("Rideau de fer portable", """Projecteur de Rideau de fer ukrainien monté sur véhicule.
Il rend invulnérables les unités amies qu'il cible pour un court instant.
Il ne tire pas pour tuer, mais pour empêcher de mourir.""",
"Accompagnez un assaut de chars lourds : rendez invulnérable l'unité la plus exposée au moment critique. Il est lui-même fragile et coûteux ; gardez-le derrière."),
"LECLERC": ("Leclerc XLR", """Char de combat français rénové, mobile et hyperconnecté.
Son chargeur automatique lui donne une cadence que peu de chars égalent.
Relié au réseau SCORPION, il frappe ce que ses éclaireurs ont repéré.""",
"Opérez-le avec des GCP, drones ou Jaguar à proximité pour la liaison SCORPION (rechargement -20 %). Utilisez sa vitesse pour tirer, se déplacer et exploiter les brèches ; sa protection GALIX absorbe le premier missile."),
"LEOPARD": ("Leopard 2A7+", """Char de combat allemand, référence mondiale en matière de blindage.
Son canon L55 et sa protection avancée en font un adversaire redoutable.
Ses équipages gardent leur sang-froid tant que la caisse tient.""",
"Formez un bloc blindé qui encaisse en première ligne, guidé par un drone Luna qui désigne les cibles (+25 % de dégâts). Moins rapide que le Leclerc : choisissez vos combats."),
"MCV": ("Véhicule de construction mobile", """Base mobile capable de se déployer en chantier de construction.
C'est la naissance de toute armée, et sa seconde chance.
Le perdre en début de partie, c'est souvent perdre la partie.""",
"Déployez-en un second pour étendre votre base près d'un champ de minerai ou fonder une base de secours. Escortez-le toujours."),
"MGG": ("Générateur de brouillard mobile", """Véhicule britannique qui régénère le brouillard de guerre autour de lui.
Il cache vos troupes au regard ennemi, radar compris.
Une armée invisible est une armée qui choisit ses combats.""",
"Accompagnez vos colonnes pour masquer leur approche ; placez-le près de votre artillerie pour cacher sa position."),
"MNLY": ("Poseur de mines", """Véhicule qui sème des mines antichars sur les axes de passage.
Il détecte aussi les mines adverses.
Une route minée vaut souvent mieux que dix défenses.""",
"Minez les accès à votre base et les passages obligés. Posez des mines sur les chemins des camions de minerai ennemis."),
"MRJ": ("Brouilleur radar mobile", """Véhicule allié qui brouille les radars ennemis proches.
Il dévie aussi les missiles entrants.
L'ennemi perd sa carte là où votre armée passe.""",
"Approchez-le des bases ennemies pour couper leur radar pendant un assaut. Il protège aussi vos colonnes des missiles."),
"MSAM": ("SAM mobile", """Lanceur de missiles antiaériens russe de la carte WW3.
Ses missiles Nike abattent les avions et les drones à longue distance.
Il transforme n'importe quelle colonne en zone d'exclusion aérienne.""",
"Escortez vos chars contre l'aviation et les drones. Gardez-le derrière la ligne : il ne vaut rien contre les unités terrestres."),
"MSAR": ("Réseau de capteurs mobile", """Poste d'écoute soviétique qui se déploie comme un radar mobile.
Déployé, il augmente la vision des véhicules proches et détecte les furtifs.
Il voit ce que les yeux ne voient pas.""",
"Déployez-le près du front pour détecter les unités furtives (Mirage, GCP) et étendre la vision de vos véhicules."),
"NAG": ("NAMICA (missiles Nag)", """Chasseur de chars indien sur châssis BMP-2, armé de missiles Nag.
Ses missiles guidés font des ravages parmi les blindés lourds.
Il doit s'immobiliser pour tirer : c'est à la fois sa force et sa faiblesse.""",
"Placez-le en embuscade derrière votre ligne pour briser les charges blindées. Il doit être à l'arrêt : ne lui demandez pas de poursuivre. Protégez-le de l'infanterie et de l'artillerie."),
"PANZER": ("Char Panzer", """Char de combat allemand de la carte WW3.
Il associe un canon de 90 mm et une mitrailleuse puissante.
Polyvalent, il répond aussi bien à l'infanterie qu'aux blindés.""",
"Char polyvalent allemand : utile contre l'infanterie comme contre les véhicules. Il complète bien le Leopard en ligne."),
"PCAN": ("Canon prisme", """Prototype espagnol d'artillerie à rayon lumineux concentré.
Il frappe les bâtiments à 11 cases avec une précision chirurgicale.
Chaque tir concentre l'énergie d'une tour prisme entière.""",
"Détruisez les bâtiments et défenses ennemis à distance, sous escorte. Fragile : repliez-le dès qu'il est menacé."),
"PTNK": ("Char prisme", """Char espagnol équipé d'une arme à rayon prisme.
Ses faisceaux se reflètent et frappent défenses et infanterie à distance.
L'arme la plus spectaculaire de l'arsenal espagnol.""",
"Artillerie à moyenne portée : détruisez défenses et infanterie, laissez les chars aux autres unités. Protégez-le de l'aviation."),
"PZH": ("Panzerhaubitze 2000", """Obusier automoteur allemand, l'un des plus puissants au monde.
Chaque obus frappe avec une violence que peu d'artilleries égalent.
Fortement blindé, il peut tenir une position que d'autres doivent quitter.""",
"Guidé par un drone KZO, pilonnez les concentrations ennemies avec de gros obus. Il peut rester plus près du front que les autres artilleries grâce à son blindage."),
"QTNK": ("Char MAD", """Char soviétique qui ancre son châssis au sol et génère des ondes sismiques.
Il détruit les véhicules et bâtiments proches, puis explose.
Une arme de dernier recours, redoutée même par ses alliés.""",
"Approchez-le d'une concentration de véhicules ou d'une base, puis déployez-le. Protégez-le de l'infanterie pendant qu'il charge."),
"RAVIT": ("Camion de ravitaillement", """Camion de transport militaire non armé, commun à toutes les armées.
Il transporte quinze fantassins ou trois véhicules sur de longues distances.
L'arme secrète des offensives rapides : la logistique.""",
"Déployez rapidement l'infanterie et les véhicules vers une base avancée. Escortez-le toujours : il n'a aucune arme."),
"RTNK": ("Char Mirage", """Char français de la carte WW3 qui se camoufle en arbre à l'arrêt.
Il attend immobile que l'ennemi passe à portée de son canon.
Beaucoup ont découvert le Mirage en perdant leur colonne.""",
"Embusquez-le sur les axes de passage ennemis. Il ne se camoufle qu'à l'arrêt : frappez puis repositionnez-vous."),
"SCUDL": ("Lance-Scud", """Lance-missiles balistique turc de la carte WW3.
Ses missiles Scud portent à 11 cases et frappent les bases ennemies.
Imprécis, il compte sur la terreur plus que sur la précision.""",
"Frappez les bâtiments ennemis à longue distance. Il ne fait pas le poids contre les véhicules : protégez-le."),
"STNK": ("Transport à phase", """Transport de troupes furtif français de la carte WW3.
Il amène cinq fantassins derrière les lignes ennemies sans être vu.
Ses missiles lui permettent de se défendre contre les blindés légers.""",
"Infiltrez ingénieurs, GCP ou Tanya dans la base ennemie. Évitez de tirer : attaquer révèle sa position."),
"T90M": ("T-90M Proryv", """Char de combat russe modernisé, héritier de la lignée T-72.
Son blindage réactif neutralise presque entièrement le premier missile antichar.
Il a été conçu pour survivre aux guerres de missiles.""",
"Utilisez-le pour percer les lignes appuyées par l'infanterie antichar : son blindage réactif encaisse le premier missile. Réparez-le pour recharger l'ERA ; attention au NLAW et au FPV, qui l'ignorent."),
"TITN": ("Titan", """Robot de combat grec de la carte WW3, un mech lourd et lent.
Son canon de 130 mm et ses missiles dominent le champ de bataille.
Il marche là où les chars ne passent pas.""",
"Unité d'appui lourde : avancez avec les hoplites et les Spartan. Lent : couvrez-le contre l'aviation."),
"TNKD": ("Chasseur de chars", """Chasseur de chars allemand de la carte WW3, armé d'un canon à rail.
Sa puissance de feu antichar est exceptionnelle.
Il n'a qu'une mission : détruire les blindés.""",
"Placez-le en seconde ligne contre les chars ennemis. Faible contre l'infanterie : escortez-le."),
"TRUK": ("Camion de ravitaillement en crédits", """Camion qui transporte de l'argent vers un allié.
Il ne combat pas ; il fait vivre les coalitions.
Un bon allié sait quand envoyer ses crédits.""",
"En partie en équipe, envoyez des crédits à un allié en difficulté. Escortez-le."),
"TTNK": ("Char Tesla", """Char soviétique équipé d'une bobine Tesla.
Ses arcs électriques traversent infanterie, véhicules et bâtiments.
Il porte la puissance d'une défense Tesla sur des chenilles.""",
"Char polyvalent à courte portée : ses arcs gèrent infanterie et véhicules. Il est léger : ne l'exposez pas aux chars lourds sans soutien."),
"TTNK2": ("Mammouth Tesla", """Char Mammouth russe adapté avec deux bobines Tesla.
Ses arcs électriques détruisent aussi bien l'infanterie que les blindés.
Une forteresse électrique qui avance lentement.""",
"Unité de percée russe : avancez contre les blindés lourds et l'infanterie. Protégez-le de l'aviation, qu'il ne peut pas attaquer."),
"TXTRK": ("Camion toxique", """Camion turc chargé d'armes chimiques mortelles.
Il répand un nuage toxique qui décime l'infanterie.
Son blindage est aussi faible que sa réputation est terrible.""",
"Envoyez-le au cœur des concentrations d'infanterie ennemie. Il meurt vite : profitez d'une diversion."),
"TYPE10": ("Type 10", """Char de combat japonais, léger, rapide et très précis.
Sa conduite de tir moderne lui permet de frapper fort à longue distance.
Il privilégie la mobilité et la précision à la masse.""",
"Harcelez les blindés ennemis à longue distance (au-delà de 4 cases, obus plus puissant), puis repositionnez-vous. Moins résistant que le Leopard : évitez les combats rapprochés prolongés."),
"TYPE16": ("Type 16", """Chasseur de chars japonais à roues, conçu pour la défense mobile.
Il file sur les routes et frappe les blindés avec un canon de 105 mm.
Mais il ne tient pas longtemps un combat de face.""",
"Flanquez l'ennemi, tirez, puis repliez-vous : son canon recharge lentement et son blindage est léger. Ne l'engagez jamais en combat frontal prolongé."),
"TYPE19": ("Type 19", """Obusier japonais de 155 mm sur camion 8x8.
Rapide et précis, il tire vite et change de position aussitôt.
Il privilégie la précision aux gros calibres.""",
"Pilonnez à longue portée avec précision, puis déplacez-vous. Plus mobile que le PzH : utilisez cette mobilité pour éviter la contre-batterie."),
"UARTY": ("M777 (Excalibur)", """Obusier ultraléger américain utilisé par l'Ukraine, tirant des obus guidés Excalibur.
Sa portée et sa précision sont extrêmes, mais il doit voir sa cible.
Associé à un drone, il frappe à 12 cases avec une précision chirurgicale.""",
"Associez-le toujours à un drone de reconnaissance (Leleka, Shark) qui fournit la vision. Il ne tire pas sur une cible non visible : restez loin et laissez les drones voir pour lui."),
"V2RL": ("Lance-V2", """Lance-missiles balistique soviétique hérité de la Seconde Guerre mondiale.
Ses missiles V2 frappent l'infanterie et les bâtiments à longue portée.
Il reste redoutable malgré son âge.""",
"Artillerie soviétique de base : pilonnez défenses et infanterie depuis l'arrière. Fragile face aux véhicules."),
"V3RL": ("Lance-V3", """Lance-missiles russe de la carte WW3, à très longue portée.
Ses missiles V3 frappent à 14 cases les bases ennemies.
Aucune défense statique n'est à l'abri.""",
"Pilonnez les bases ennemies de très loin. Fragile : protégez-le des raids et de l'aviation."),
"ftnk": ("Char lance-flammes", """Char équipé d'un lance-flammes lourd.
Il incendie l'infanterie et les bâtiments à courte portée.
Rien ne résiste longtemps à sa chaleur.""",
"Nettoyez l'infanterie et les bâtiments légers. Courte portée : approchez-le sous couverture."),
}
