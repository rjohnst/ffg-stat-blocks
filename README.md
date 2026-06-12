# ffg-stat-blocks

generate custom pngs for FFG Star Wars stat blocks so I don't have to.

## stat-block.py

usage: stat_block.py [-h] [--theme THEME] [--output OUTPUT] values values values values values values

Generate a themed stat block image.

positional arguments:
  values           Six characteristic values: brawn agility intellect cunning willpower presence

options:
  -h, --help       show this help message and exit
  --theme THEME    Theme: blacksun, default
  --output OUTPUT  output filename

## def_block.py
usage: def_block.py [-h] [--theme THEME] [--output OUTPUT] soak wounds strain mr_def

Generate header stat block.

positional arguments:
  soak
  wounds
  strain
  mr_def

options:
  -h, --help       show this help message and exit
  --theme THEME    Theme: blacksuns, default
  --output OUTPUT

## skills.py
usage: skills.py [-h] [--output OUTPUT]

Generate a skills block image.

options:
  -h, --help       show this help message and exit
  --output OUTPUT  Output filename

## TODO

* validate skill names / prompt for each skill (tedious though)
* show "remove a setback die" for skills
* show "add an automatic advantage/threat" for skills
* more themes I guess

