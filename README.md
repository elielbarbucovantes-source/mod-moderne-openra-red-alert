# Mod moderne pour OpenRA Red Alert

Un mod pour [OpenRA](https://www.openra.net) (Red Alert) qui ajoute des unités modernes et les factions de la carte « Europe: WW3 ».

## Contenu

- **Unités modernes** : Leopard 2, Challenger 3, T-90M, BMPT, EBRC Jaguar, PzH 2000, AS-90, César, Grad, drones (FPV, Reaper, Patroller, Colibri…), NLAW, Rafale, Harrier, Mi-24, tranchées, pont tactique…
- **Porte-avions** : les avions atterrissent dessus, se réarment et redécollent (code C# dans `OpenRA.Mods.Ratc/`).
- **Factions WW3** : USA, Espagne, Chine, Turquie et Grèce, avec leurs unités (A-10, F-22, Apache, Kirov, chars prisme, Apocalypse, Titan, Scud…).
- **Japon** (Allié : précision et mobilité) : Type 10, Type 16, Type 19, drone SeaGuardian, brouillage électronique.
- **Inde** (Soviétique : polyvalence et saturation) : Arjun, NAMICA (missiles Nag), Dhanush, drone TAPAS, barrage Pinaka.
- **Pouvoirs de soutien nationaux** : chaque nation a son bâtiment dédié (SCALP, pontage, brouillage SAS, AWACS, TOS-1A, guerre électronique, Pinaka).

## Installation

Prérequis (Linux) : `git`, `make`, `curl`, `unzip` et le [SDK .NET 6](https://dotnet.microsoft.com/download/dotnet/6.0).

```sh
git clone https://github.com/elielbarbucovantes-source/mod-moderne-openra-red-alert.git
cd mod-moderne-openra-red-alert
make              # télécharge le moteur OpenRA (release-20231010) et compile le mod
./launch-game.sh
```

Sous Windows : `make.cmd` puis `launch-game.cmd`.

Sous macOS (Intel ou Apple Silicon) : installer le [SDK .NET 6](https://dotnet.microsoft.com/download/dotnet/6.0), puis les mêmes commandes que sous Linux dans le Terminal. Si seul un .NET plus récent est installé, lancer avec `DOTNET_ROLL_FORWARD=LatestMajor ./launch-game.sh`.

Au premier lancement, le jeu propose de télécharger les fichiers d'origine de Red Alert (version gratuite de 2008) : choisir « Quick Install ».

## Générateur de cartes aléatoires

Dans le sélecteur de cartes (lobby d'escarmouche ou de partie en réseau), le bouton **Générer une carte** ouvre le générateur de cartes aléatoires d'OpenRA. Il est repris du playtest-20260222 et adapté au moteur release-20231010 du mod. On y choisit le climat, la taille, le type de terrain, la forme, le nombre de joueurs, la symétrie, les ressources, les bâtiments technologiques, les zones d'expansion, les villages civils et les routes. **Nouvelle carte** tire une autre graine.

Différence avec le playtest : quand on clique sur **Jouer cette carte**, la carte est enregistrée comme un fichier `.oramap` dans le dossier des cartes de l'utilisateur (`maps/ra/release-20231010/aleatoire-…oramap`). Elle apparaît ensuite dans l'onglet **Custom Maps**, et on peut la rejouer, la partager ou l'ouvrir dans l'éditeur comme n'importe quelle autre carte.

Options ajoutées au générateur :

- **Région du monde** : Aléatoire (relief inventé, comme avant) ou une région réelle (Europe, France, Golfe Persique, Japon, Amériques, Australie…), avec ses vraies côtes et son vrai relief. Les trois cartes **Monde immense** font 512 cases de large : réaliste, continents séparés, ou continents reliés par des ponts permanents (solides, mais destructibles).
- **Oil derricks** : Auto (selon « Bâtiments tech. ») ou un nombre exact de derricks, de 1 à 100.

Pour tester sans lancer le jeu : `./utility.sh --generate-random-maps 20 /tmp/cartes` génère 20 cartes avec des réglages au hasard ; `Option=Choix` impose un réglage (ex. `WorldRegion=monde-ponts Players=4`).

Pour tester sans lancer le jeu : `./utility.sh --generate-random-maps 20 /tmp/cartes` génère 20 cartes avec des réglages au hasard, puis les enregistre avec leur aperçu.

## Organisation

| Chemin | Rôle |
| --- | --- |
| `mods/ratc/` | Règles, armes, séquences et sprites du mod |
| `mods/ratc/ww3/` | Contenu repris de la carte « Europe: WW3 » |
| `OpenRA.Mods.Ratc/` | Traits C# (porte-avions) |
| `mods/ratc/mapgen/` | Réglages du générateur de cartes aléatoires, pinceaux de tuiles des tilesets, sélecteur de cartes et panneau du générateur |
| `OpenRA.Mods.Ratc/MapGen/` | Générateur de cartes aléatoires rétroporté d'OpenRA (playtest-20260222) |
| `tools/sprites/` | Scripts Python qui génèrent les sprites des véhicules |

## Crédits

- Mod : Leile.
- Contenu WW3 : carte « Europe: WW3 » de Trump, H, Therapist, Leile, Ruben et d'autres ; merci à Frenzy, Widow, Pinkthoth, SirCake, MedalMonkey, Inq8, Zypres et bien d'autres pour les graphismes, le code et l'aide.
- Générateur de cartes aléatoires : code et données d'[OpenRA](https://github.com/OpenRA/OpenRA) (playtest-20260222, licence GPL v3) par les développeurs et contributeurs d'OpenRA, adaptés au moteur release-20231010.
- Régions du monde réel du générateur (`mods/ratc/mapgen/monde/`, produites par `tools/monde.py`) : côtes et lacs de [Natural Earth](https://www.naturalearthdata.com/) (domaine public) ; relief des [Terrain Tiles](https://registry.opendata.aws/terrain-tiles/) d'AWS (SRTM, GMTED2010, ETOPO1 et autres sources publiques, voir leur page d'attribution).
- Basé sur l'[OpenRA Mod SDK](https://github.com/OpenRA/OpenRAModSDK).

## Licence

Le moteur OpenRA, les scripts du SDK et le code C# du mod sont sous licence [GPLv3](COPYING). Les graphismes et sons du dossier `ww3/` restent la propriété de leurs auteurs respectifs.
