def enum(**enums):
    return type('Enum', (), enums)

# Pokedexes
from data.natdex_reference import natdex_ref
from data.nat_pokedex import nat_pokedex            # every pokemon
from data.pal_pokedex import pal_pokedex            # entire paldea dex
from data.pal_pokedex import pal_pokedex_unique     # paldea dex with unique pokemon only (only fully evolved, minus hisuian evolution lines for now)
from data.pal_pokedex import pal_pokedex_basic      # unique paldea dex without legends and paradox

POKEDEX_ENUM = enum(NAT=nat_pokedex, PAL=pal_pokedex)
POKEDEXES = {"National": nat_pokedex, "Paldea": pal_pokedex, "Paldea - Unique": pal_pokedex_unique, "Paldea - Basic": pal_pokedex_basic}


types = ["fire", "water", "grass", "electric", "rock", "ground", "flying", "poison", "bug", "normal", "fighting", "psychic", "ghost", "ice", "dragon", "dark", "steel", "fairy"]

sprites_path = "img/sprites/"
sprites_8bit_path = "img/sprites_8bit/"
types_path = "img/types/"
icon_path = "img/icon/"
