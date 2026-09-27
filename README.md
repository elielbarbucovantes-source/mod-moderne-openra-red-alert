# Mod moderne pour OpenRA Red Alert

Un mod pour [OpenRA](https://www.openra.net) (Red Alert) qui ajoute des unités modernes et les factions de la carte « Europe: WW3 ».

## Contenu

- **Unités modernes** : Leopard 2, Challenger 3, T-90M, BMPT, EBRC Jaguar, PzH 2000, AS-90, César, Grad, drones (FPV, Reaper, Patroller, Colibri…), NLAW, Rafale, Harrier, Mi-24, tranchées, pont tactique…
- **Porte-avions** : les avions atterrissent dessus, se réarment et redécollent (code C# dans `OpenRA.Mods.Ratc/`).
- **Factions WW3** : USA, Espagne, Chine, Turquie et Grèce, avec leurs unités (A-10, F-22, Apache, Kirov, chars prisme, Apocalypse, Titan, Scud…).

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

## Organisation

| Chemin | Rôle |
| --- | --- |
| `mods/ratc/` | Règles, armes, séquences et sprites du mod |
| `mods/ratc/ww3/` | Contenu repris de la carte « Europe: WW3 » |
| `OpenRA.Mods.Ratc/` | Traits C# (porte-avions) |
| `tools/sprites/` | Scripts Python qui génèrent les sprites des véhicules |

## Crédits

- Mod : Leile.
- Contenu WW3 : carte « Europe: WW3 » de Trump, H, Therapist, Leile, Ruben et d'autres ; merci à Frenzy, Widow, Pinkthoth, SirCake, MedalMonkey, Inq8, Zypres et bien d'autres pour les graphismes, le code et l'aide.
- Basé sur l'[OpenRA Mod SDK](https://github.com/OpenRA/OpenRAModSDK).

## Licence

Le moteur OpenRA, les scripts du SDK et le code C# du mod sont sous licence [GPLv3](COPYING). Les graphismes et sons du dossier `ww3/` restent la propriété de leurs auteurs respectifs.
