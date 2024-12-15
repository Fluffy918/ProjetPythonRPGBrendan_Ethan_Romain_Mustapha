import random
class Creature:
    def __init__(self, nom, pv, pm, atck, deff):
        self.nom = nom
        self.pv = pv
        self.pm = pm
        self.atck = atck
        self.deff = deff
        self.defending = False # Indique si la creature se défend

    def attaquer(self, cible):
        """Effectue une attaque sur une cible."""
        degats = max(1, self.atck - (cible.deff // 2 if cible.defending else cible.deff)) # Les dégats ne peuvent pas être supérieur à 1
        cible.pv -= degats
        print(f"{self.nom} attaque {cible.nom} et inflige {degats} dégats !")
        if cible.pv <= 0:
            print(f"{cible.nom} est vaincue(e) !")

    def lancer_sort(self, cible, sort):
        """Lance un sort si le personnage a asser de PM."""
        if self.pm >= sort["cout_pm"]:
            self.pm -= sort["cout_pm"]
            effet = sort.get("effet", None)
            if effet == "degats":
                cible.pv -= sort["valeur"]
                print(f"{self.nom} lance  {sort['nom']} et inflige {sort['valeur']} dégats à {cible.nom} !")
            elif effet == "soin":
                self.pv += sort["valeur"]
                print(f"{self.nom} utilise {sort['nom']} et récupère {sort['valeur']} PV !")
            elif effet == "poison":
                cible.pv -= sort["valeur"]
                print(f"{self.nom} empoisonne {cible.nom} avec {sort['nom']} infligeant {sort['valeur']} dégats !")

            elif cible.pv <= 0:
                print(f"{cible.nom} est vaincu(e)")

        else:
            print(f"{self.nom} n'a pas assez de PM")

    def afficher_stats(self):
        """Affiche les statistiques actuelles du personnage."""
        print(f"Nom: {self.nom} | PV: {self.pv} | PM: {self.pm} | Atck: {self.atck} | Deff: {self.deff}")


class Personnage(Creature):
    def __init__(self, nom, pv, pm, atck, deff):
        super().__init__(nom, pv, pm, atck, deff)
        self.inventaire = [] # Liste d'objets
        self.niveau = 1
        self.xp = 0
        self.xp_niveau_suivant = 100
        self.or_ = 50 # Or du personnage
        self.arme = None
        self.armure = None
        self.sorts = [
            {"nom": "Fireball", "cout_pm": 7, "effet": "degats", "valeur": 25},
            {"nom": "Premier Secours", "cout_pm": 5, "effet": "soin", "valeur": 30}
        ]

    def equiper(self, objet):
      """Equiper une arme ou une armure."""
      if "Epée" in objet:
        if self.arme:
          print(f"self.nom déséquipe {self.arme}")
        self.arme = objet
        self.atck += 10
        print(f"{self.nom} équipe {objet} (+10 Attaque) !")
      elif "Armure" in objet:
        if self.armure:
          print(f"{self.nom} déséquipe {self.armure}")
        self.armure = objet
        self.deff += 5
        print(f"{self.nom} équipe {objet} (+5 Défense) !")
      else:
        print(f"{objet} ne peut pas être équipé.")

    def gagner_or(self, montant):
      """Ajouter de l'or au personnage."""
      self.or_ += montant
      print(f"{self.nom} gagne {montant} pièces d'or !")

    def acheter_objet(self, objet, prix):
      """Permet d'acheter un objet si le héros a assez d'or."""
      if self.or_ >= prix:
        self.or_ -= prix
        self.inventaire.append(objet)
        print(f"{self.nom} a acheté {objet} pour {prix} pièces d'or !")
      else:
        print(f"pas assez d'or pour acheter {objet}.")

    def utiliser_objet(self, objet):
        """Utilise un objet de l'inventaire."""
        if objet in self.inventaire:
            if objet == "Potion":
                self.pv += 20
                print(f"{self.nom} utilise {objet} !")
                print(f"{self.nom} récupère 20 PV")
            elif objet.startswith("Epée de feu"):
              self.equiper(objet)
            elif objet.startswith("Armure de glace"):
              self.equiper(objet)
            self.inventaire.remove(objet)
        else:
            print(f"{objet} n'est pas dans l'inventaire")


    def ajouter_objet(self, objet):
        """Ajouter un objet à l'inventaire."""
        self.inventaire.append(objet)
        print(f"{objet} ajouté à l'inventaire de {self.nom}.")

    def gagner_xp(self, montant):
        """Ajouter de l'XP et vérifie si le personnage monte de niveau"""
        self.xp += montant
        print(f"{self.nom} gagne {montant} XP !")
        if self.xp >= self.xp_niveau_suivant:
            self.niveau += 1
            self.xp -= self.xp_niveau_suivant
            self.xp_niveau_suivant += 50 # Augmentation du seuil pour le niveau suivant
            self.pv += 10
            self.pm += 5
            self.atck += 2
            self.deff += 2
            print(f"{self.nom} monte au niveau {self.niveau} ! Stats améliorées !")

    def afficher_inventaire(self):
      """Afficher le contenu de l'inventaire."""
      print(f"\nInventaire de {self.nom} :")
      print(f"Or : {self.or_} pièces")
      if not self.inventaire:
        print("Aucun objet.")
      else:
        for i, objet in enumerate(self.inventaire, 1):
          print(f"{i} - {objet}")

class Monster(Creature):
    def __init__(self, nom, pv, pm, atck, deff, sorts):
        super().__init__(nom, pv, pm, atck, deff)
        self.sorts = sorts # Listes des sorts sous la forme [{"nom": "Sort", "cout_pm": X, "degats": Y}]

    def agir(self, cible):
        """IA stratégique pour le monstre"""
        if self.pv <= 10 and self.pm >=5:
            # Si le monstre est en danger, il peut lancer un sort de soin s'il en a
            for sort in self.sorts:
                if sort["effet"] == "soin":
                    self.lancer_sort(self, sort)
                    return
        elif self.pm >= 5:
            # Priorité au sort offensif si suffisament de PM
            for sort in self.sorts:
                if sort["effet"] == "degats":
                    self.lancer_sort(cible, sort)
                    return
        else:
            self.attaquer(cible)


class Marchand:
  def __init__(self):
    self.objets = [
        {"nom": "Potion", "prix": 10},
        {"nom": "Epéé de feu", "prix": 30},
        {"nom": "Armure de glace", "prix": 25}
    ]

  def afficher_objets(self):
    """Affiche les objets disponible à la vente"""
    print("\n--- Objets disponibles chez le Marchand ---")
    for i, objet in enumerate(self.objets, 1):
      print(f"{i} - {objet['nom']} : {objet['prix']} pièces d'or")

  def acheter(self, hero, choix):
    """Permet au héro d'acheter un objet."""
    if 0 <= choix < len(self.objets):
      objet = self.objets[choix]
      if hero.or_ >= objet["prix"]:
        hero.or_ -= objet["prix"]
        hero.ajouter_objet(objet["nom"])
        print(f"{hero.nom} achète {objet['nom']} pour {objet['prix']} pièces d'or.")
      else:
        print(f"Vous n'avez pas assez d'or pour acheter {objet['nom']} !")
    else:
      print("Choix invalide")

def menu_marchand(hero, marchand):
  """Menu pour intéragir avec le marchand."""
  while True:
    print("\nBienvenue chez le Marchand !")
    print("1 - Voir les objets")
    print("2 - Acheter un objet")
    print("3 - Quitter le marchand")
    choix = input("Votre choix : ")
    if choix == "1":
      marchand.afficher_objets()
    elif choix == "2":
      marchand.afficher_objets()
      choix_objet = int(input("Choisissez un objet :")) - 1
      marchand.acheter(hero, choix_objet)
    elif choix == "3":
      print("Au revoir !")
      break
    else:
      print("Choix invalide.")




def combat(hero, monstres, boss):
  random.shuffle(monstres) # Mélanger les ennemis
  marchand = Marchand()

  for monstre in monstres :
    print(f"\n Un {monstre.nom} apparaît !")
    if hasattr(monstre, 'dialogues'): # Si le monstre est un boss
      print(f"\n{monstre.nom} : {random.choice(monstre.dialogues)}")
    """Système de combat tour par tour."""
    while hero.pv > 0 and monstre.pv > 0:
        print("\n--- Nouveau Tour ---")
        hero.afficher_stats()
        monstre.afficher_stats()

        # Tour du héros
        print("\nOptions :")
        print("1 - Attaquer")
        print("2 - Lancer un sort")
        print("3 - Défendre")
        print("4 - Inventaire")
        print("5 - Fuir")
        choix = input("Votre choix :")
        if choix == "1":
            hero.attaquer(monstre)
        elif choix == "2":
            print("Sorts disponibles :")
            for i, sort in enumerate(hero.sorts):
                print(f"{i + 1} - {sort['nom']} (Coût : {sort['cout_pm']} PM)")
            choix_sort = int(input("Choisissez un sort : ")) - 1
            if 0 <= choix_sort < len(hero.sorts):
                hero.lancer_sort(monstre, hero.sorts[choix_sort])
        elif choix == "3":
            hero.defending = True
            print(f"{hero.nom} se défend !")
        elif choix == "4":
          hero.afficher_inventaire()
          choix_inventaire = input("Choisissez un objet à utiliser (ou q pour quitter) :")
          if choix_inventaire.isdigit() and 1 <= int(choix_inventaire) <= len(hero.inventaire):
            hero.utiliser_objet(hero.inventaire[int(choix_inventaire) - 1])
        elif choix == "5":
            print(f"{hero.nom} fuit le combat !")
            return

        if monstre.pv <= 0:
            print(f"{monstre.nom} est vaincu !")
            hero.gagner_xp(50)
            hero.gagner_or(random.randint(10, 30)) # Récompense en or
            loot = random.choice(["Potion", "Epée de feu", "armure de glace"])
            hero.ajouter_objet(loot)
            print(f"Vous trouvez un butin : {loot} !")
            break

        # Tour du monstre
        monstre.agir(hero)
        if hero.pv <= 0:
            print(f"{hero.nom} est vaincu(e) !")
            return

        # Fin du tour
        hero.defending = False

    # Interaction avec le marchand après chaque combat
    print("\nVous croisez un marchand itinérant.")
    menu_marchand(hero, marchand)

  # Combat contre le boss
  print(f"\n{boss.nom} : {boss.dialogues}")
  while hero.pv > 0 and boss.pv > 0:
    print("\n--- Combat contre le boss ---")
    hero.afficher_stats()
    boss.afficher_stats()

    # Tour du héro
    print("\nOptions :")
    print("1 - Attaquer")
    print("2 - Lancer un sort")
    print("3 - Défendre")
    print("4 - Inventaire")
    print("5 - Fuir")
    choix = input("Votre choix :")
    if choix == "1":
        hero.attaquer(boss)
    elif choix == "2":
        print("Sorts disponibles :")
        for i, sort in enumerate(hero.sorts):
            print(f"{i + 1} - {sort['nom']} (Coût : {sort['cout_pm']} PM)")
        choix_sort = int(input("Choisissez un sort : ")) - 1
        if 0 <= choix_sort < len(hero.sorts):
            hero.lancer_sort(boss, hero.sorts[choix_sort])
    elif choix == "3":
        hero.defending = True
        print(f"{hero.nom} se défend !")
    elif choix == "4":
          hero.afficher_inventaire()
          choix_inventaire = input("Choisissez un objet à utiliser (ou q pour quitter) :")
          if choix_inventaire.isdigit() and 1 <= int(choix_inventaire) <= len(hero.inventaire):
            hero.utiliser_objet(hero.inventaire[int(choix_inventaire) - 1])
    elif choix == "5":
        print(f"{hero.nom} fuit le combat !")
        return

    if boss.pv <= 0:
        print(f"{boss.nom} est vaincu !")
        hero.gagner_xp(50)
        hero.gagner_or(random.randint(20, 50))

    # Tour du boss
    boss.agir(hero)
    if hero.pv <= 0:
      print(f"{hero.nom} est vaincu(e) !")
      return

    # Fin du tour
    hero.defending = False

