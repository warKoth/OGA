""" Projet de création d'armée pour un jeu de stratégie / wargame.
    Permet de créer des armées personnalisées de la chaine de commandement à l'organisation des bataillons."""

from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass
import random

#1. Pattern Observateur : Permet de notifier les changement d'état d'un sujet aux observateurs enregistrés.
#Classe observateur pour le pattern observateur
class Observer(ABC):
    @abstractmethod
    def update(self, subject, event:str):
        pass

#Classe sujet pour le pattern observateur
class Subject(ABC):
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, event:str):
        for observer in self._observers:
            observer.update(self, event)

#2. Pattern Composite : Permet de composer des objets en structures arborescentes pour représenter des hiérarchies partie-tout.
class UniteAbstaite(ABC, Subject):
    """Classe de base pour toutes les unités militaires."""
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    @abstractmethod
    def get_effectif(self) -> int:
        pass

    @abstractmethod
    def get_puissance_totale(self) -> int:
        pass    

    @abstractmethod
    def afficher(self, indent: int = 0):
        pass

class Soldat(UniteAbstaite):
    """Classe représentant un soldat individuel."""
    def __init__(self, name: str, puissance: int, grade:str, defense:int, vitesse:int, experience:int):
        super().__init__(name)
        self.puissance = puissance
        self.grade = grade
        self.defense = defense
        self.vitesse = vitesse
        self.experience = experience

    def get_effectif(self) -> int:
        return 1

    def get_puissance_totale(self) -> int:
        return self.puissance + self.defense + self.vitesse 

    def afficher(self, indent: int = 0):
        print(' ' * indent + f"└─ {self.grade} {self.name} [F: {self.puissance} D: {self.defense} V: {self.vitesse} ]")

    def gagner_experience(self, points:int):
        self.experience += points
        self.notify(f"{self.name} a gagné {points} points XP.")

class Groupe(UniteAbstaite):
    """Classe représentant un groupe d'unités militaires."""
    def __init__(self, name: str, Commandant: Soldat = None):
        super().__init__(name)
        self.commandant = Commandant
        self.membres: List[UniteAbstaite] = []

    def ajouter_unite(self, unite: UniteAbstaite):
        self.membres.append(unite)
        self.notify(f"Unité {unite.name} ajoutée à {self.name}.")

    def retirer_unite(self, unite: UniteAbstaite):
        self.membres.remove(unite)
        self.notify(f"Unité {unite.name} retirée de {self.name}.")

    def get_effectif(self) -> int:
        total = 1 if self.commandant else 0
        for membre in self.membres:
            total += membre.get_effectif()
        return total

    def get_puissance_totale(self) -> int:
        total = self.commandant.get_puissance_totale() if self.commandant else 0
        for membre in self.membres:
            total += membre.get_puissance_totale()
        return total

    def afficher(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}┌─ {self.nom} (Effectif: {self.get_effectif()})")
        if self.commandant:
            print(f"{prefix}│  Commandant:")
            self.commandant.afficher(indent + 1)
        for membre in self.membres:
            membre.afficher(indent + 1)