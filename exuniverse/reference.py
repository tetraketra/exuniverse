import more_itertools as mit

MAX_AT_AB_MT_LENGTH = 128
MAX_CARD_NAME_LENGTH = 128

ATTRIBUTES = [*mit.padded(['DARK', 'EARTH', 'FIRE', 'LIGHT', 'WATER', 'WIND', 'DIVINE'], '?', MAX_AT_AB_MT_LENGTH)]
ABILITIES = [*mit.padded(['Flip', 'Gemini', 'Spirit', 'Toon', 'Tuner', 'Union'], '?', MAX_AT_AB_MT_LENGTH)]
MONSTER_TYPES = [*mit.padded(
    [
     'Aqua', 'Beast', 'Beast-Warrior', 'Creator God', 'Cyberse',
     'Dinosaur', 'Divine-Beast', 'Dragon', 'Fairy', 'Fiend', 'Fish',
     'Illusion', 'Insect', 'Machine', 'Plant', 'Psychic', 'Pyro', 'Reptile',
     'Rock', 'Sea Serpent', 'Spellcaster', 'Thunder', 'Warrior',
     'Winged Beast', 'Wyrm', 'Zombie', 'Celestial Warrior', 'Cyborg',
     'Galaxy', 'High Dragon', 'Magical Knight', 'Omega Psychic', 'Yokai'
    ], '?', MAX_AT_AB_MT_LENGTH)]

TTYPES = ["Monster", "Spell", "Trap"] # 1 2 3
TSUBTYPES = [
    (1, 'Normal'), (1, 'Effect'), (1, 'Ritual'), (1, 'Fusion'), (1, 'Synchro'), 
    (1, 'Xyz'), (1, 'Link'), (1, 'Token'), (2, 'Normal'), (2, 'Continuous'), 
    (2, 'Field'), (2, 'Equip'), (2, 'Quick-Play'), (2, 'Ritual'), 
    (3, 'Normal'), (3, 'Continuous'), (3, 'Counter')
]
TSUBTYPES_NAMES = [*zip(*TSUBTYPES)][1]

FORMATS = ["OCG", "TCG", "EXU"]