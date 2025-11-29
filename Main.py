""" Projet de création d'armée pour un jeu de stratégie / wargame.
    Permet de créer des armées personnalisées de la chaine de commandement à l'organisation des bataillons."""

from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass
import random

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
