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