from Main import *

# hero = Personnage("Tommy", 100, 30, 15, 10)
import random

# Création des monstres avec un système de puissance
def creer_monstre():
  aquapode = Monster(
      nom = "Aquapode",
      pv = 50,
      pm = 20,
      atck = 10,
      deff = 5,
      sorts = [
          {"nom": "Splash", "cout_pm": 5, "effet": "degats", "valeur": 10},
          {"nom": "haleine toxic", "cout_pm": 8, "effet": "degats", "valeur": 15}
      ]
  )
  tornador = Monster(
      nom = "Tornador",
      pv = 60,
      pm = 25,
      atck = 15,
      deff = 8,
      sorts = [
          {"nom": "supertornade", "cout_pm": 8, "effet": "degats", "valeur": 20},
          {"nom": "tornade", "cout_pm": 5, "effet": "degats", "valeur": 10}
      ]
  )
  spectrokane = Monster(
      nom = "Spectrokane",
      pv = 70,
      pm = 35,
      atck = 25,
      deff = 1,
      sorts = [
          {"nom": "souffle frais", "cout_pm": 5, "effet": "degats", "valeur": 15},
          {"nom": "souffle frois", "cout_pm": 15, "effet": "degats", "valeur": 30}
      ]
  )

  return [aquapode, tornador, spectrokane]

# Création du boss avec dialogues
def creer_boss():
  boss = Monster(
      nom = "Mortamor",
      pv = 250,
      pm = 80,
      atck = 25,
      deff = 15,
      sorts = [
          {"nom": "orage d'éclaire", "cout_pm": 20, "effet": "degats", "valeur": 30},
          {"nom": "gigaslash", "cout_pm": 25, "effet": "degats", "valeur": 50}
      ]
  )
  boss.dialogues = [
      "Vous osez défier le grand Mortamor ?",
      "Votre fin est proche, misérable humain !",
      "Vous ne survivrez pas à ma colère !",
      "Mouhahahahahahaha !!"
  ]
  return boss