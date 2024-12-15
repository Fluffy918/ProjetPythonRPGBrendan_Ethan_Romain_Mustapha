from Creation import *
from Main import *

hero = Personnage("Tommy", 150, 50, 15, 10)
monstres = creer_monstre()
boss = creer_boss()
combat(hero, monstres, boss)

hero.gagner_xp(random.randint(50, 100))
hero.gagner_or(random.randint(10, 30))