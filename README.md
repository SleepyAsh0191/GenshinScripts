# [WIP] GenshinScripts

A collection of scripts to be used with the data from https://github.com/Dimbreath/GenshinData (huge thanks to them btw)

## What can these scripts extract ?

- Quests (Daily commissions and World Quests) and Chapters (Archon, Story and Event Quests) (.txt)
- Cooking recipes (.txt)
- Achievements (.txt)
- Characters (.json)

And more to come...

## Requirements

- Python 3.6+

## How to use it

- Python 3.6+ should be installed
- Download the data from https://github.com/Dimbreath/GenshinData and extract it in a data/ folder at the root of the project.
- The files structure should look like this :
```
GenshinScripts/     (main folder)
├── data/             (from Dimbreath/GenshinData)
│   ├── Excel/
│   │   ├── _.json
│   │   ...
│   ├── Readable/       (books and items descriptions)
│   │   ├── {lang}/...
│   │   ...
│   └── TextMap/
│       ├──text_.json
│       ...
├── utils/
│   ├── _.py
│   ...
├── main.py
└── README.md
```
- Now `main.py` can be used with the parameter `--lang EN|FR|JP|....` with the language being formatted like the textmaps in `data/`. However this file can't be called directly in a terminal, but functions from the `utils/` scripts can be imported and called in this file.
