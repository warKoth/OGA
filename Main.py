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
class UniteAbstaite(Subject, ABC):
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
    def __init__(self, name: str, puissance: int, grade:str, defense:int, vitesse:int, experience:int, equipements :list = None):
        super().__init__(name)
        self.puissance = puissance
        self.grade = grade
        self.defense = defense
        self.vitesse = vitesse
        self.experience = experience
        self.equipements = [] if equipements is None else equipements

    def equiper(self, equipement: str):
        name = equipement.nom if hasattr(equipement, 'nom') else str(equipement)
        self.equipements.append(equipement)
        self.notify(f"{self.name} est équipé de {name}.")

    def desequiper(self, equipement: str):
        name = equipement.nom if hasattr(equipement, 'nom') else str(equipement)
        self.equipements.remove(equipement)
        self.notify(f"{self.name} s'est déséquipé de {name}.")


    def get_effectif(self) -> int:
        return 1

    def get_puissance_totale(self) -> int:
        # Base stats
        total = self.puissance + self.defense + self.vitesse
        # Add equipment bonuses when equipment objects are present
        bonus = 0
        for eq in self.equipements:
            if hasattr(eq, 'puissance_bonus') or hasattr(eq, 'defense_bonus') or hasattr(eq, 'vitesse_bonus'):
                pb = getattr(eq, 'puissance_bonus', 0)
                db = getattr(eq, 'defense_bonus', 0)
                vb = getattr(eq, 'vitesse_bonus', 0)
                bonus += (pb + db + vb)
        return total + bonus

    def afficher(self, indent: int = 0):
        equip_names = []
        for e in self.equipements:
            equip_names.append(e.nom if hasattr(e, 'nom') else str(e))
        equip_str = ', '.join(equip_names) if equip_names else 'Rien'
        print(' ' * indent + f"└─ {self.grade} {self.name} [F: {self.puissance} D: {self.defense} V: {self.vitesse} ] equipé de : {equip_str}")

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
        print(f"{prefix}┌─ {self.name} (Effectif: {self.get_effectif()})")
        if self.commandant:
            print(f"{prefix}│  Commandant:")
            self.commandant.afficher(indent + 1)
        for membre in self.membres:
            membre.afficher(indent + 1)

#3. Pattern Factory : Permet de créer des objets sans exposer la logique de création au client.
class TroupeFactory:
    """Classe factory pour créer des unités militaires."""
    @staticmethod
    def creer_soldat(name: str, grade:str) -> Soldat:
        puissance = random.randint(5, 15)
        defense = random.randint(5, 15)
        vitesse = random.randint(5, 15)
        experience = 0
        return Soldat(name, puissance, grade, defense, vitesse, experience)
    
    @staticmethod
    def creer_soldat_special(name: str, grade:str, puissance:int, defense:int, vitesse:int) -> Soldat:
        puissance = random.randint(9, 25)
        defense = random.randint(9, 25)
        vitesse = random.randint(10, 25)
        experience = 0
        return Soldat(name, puissance, grade, defense, vitesse, experience)
    
    @staticmethod
    def creer_officier(name: str, grade:str) -> Soldat:
        puissance = random.randint(15, 30)
        defense = random.randint(15, 30)
        vitesse = random.randint(15, 30)
        experience = 0
        return Soldat(name, puissance, grade, defense, vitesse, experience)


# Class equipement Decorator
class Equipement:
    """Classe de base pour les équipements."""
    def __init__(self, nom: str, puissance_bonus: int, defense_bonus: int, vitesse_bonus: int):
        self.nom = nom
        self.puissance_bonus = puissance_bonus
        self.defense_bonus = defense_bonus
        self.vitesse_bonus = vitesse_bonus
    
class Fusil(Equipement):
    """Classe représentant un fusil."""
    def __init__(self):
        super().__init__("Fusil", puissance_bonus=5, defense_bonus=0, vitesse_bonus=0)
    

class GiletPareBalles(Equipement):
    """Classe représentant un gilet pare-balles."""
    def __init__(self):
        super().__init__("Gilet Pare-Balles", puissance_bonus=0, defense_bonus=5, vitesse_bonus=0)

class BottesOfficier(Equipement):
    """Classe représentant des bottes d'officier."""
    def __init__(self):
        super().__init__("Bottes d'Officier", puissance_bonus=0, defense_bonus=0, vitesse_bonus=5)

    


# Class d'observateur concret journal des evenements
class JournalCombat(Observer):
    """Classe observateur pour enregistrer les événements de combat."""
    
    def __init__(self):
        self.historique = []

    def update (self, subject, event: str):
        self.historique.append(event)
        print(f"[Journal] {event}")

    def afficher_historique(self):
        print("\n ======Historique des événements de combat======")
        for i, event in enumerate(self.historique, 1):
            print(f"{i}. {event}")

# Exemple d'utilisation
if __name__ == "__main__":
    print ("Simulation de création d'armée avec patterns de conception\n")

    # creation d'un observateur
    journal = JournalCombat()

    # Factory pour créer des soldats

    Factory = TroupeFactory()

    soldat1 = TroupeFactory.creer_soldat("Jean", "Caporal")
    soldat2 = TroupeFactory.creer_soldat("Pierre", "Soldat")
    soldat3 = TroupeFactory.creer_soldat_special("Luc", "Sergent", 20, 15, 10)
    soldat4 = TroupeFactory.creer_soldat("Marc", "Soldat")
    soldat5 = TroupeFactory.creer_soldat("Paul", "Caporal")
    soldat6 = TroupeFactory.creer_soldat("Antoine", "Soldat")
    officier1 = TroupeFactory.creer_officier("Alice", "Lieutenant")

    #Donner des équipements aux soldats
    soldat1.equiper(Fusil())
    soldat2.equiper(Fusil())
    officier1.equiper(BottesOfficier())
    officier1.equiper(GiletPareBalles())
    officier1.equiper(Fusil())

    # Création de groupes
    escouade1 = Groupe("Escouade Alpha", Commandant=officier1)
    escouade1.attach(journal)

    escouade2 = Groupe("Escouade Bravo", Commandant=soldat3)
    escouade2.attach(journal)

    escouade1.ajouter_unite(soldat2)
    escouade1.ajouter_unite(soldat4)
    escouade2.ajouter_unite(soldat5)
    escouade2.ajouter_unite(soldat6)

    # Affichage de la structure de l'armée
    print ("\nStructure de l'armée :")
    escouade1.afficher()
    escouade2.afficher()

    print (f"\nEffectif total de l'armée : {escouade1.get_effectif() + escouade2.get_effectif()}")
    print (f"Puissance totale de l'armée : {escouade1.get_puissance_totale() + escouade2.get_puissance_totale()}\n")

    # Simuler des gains d'expérience
    soldat5.gagner_experience(15)
    soldat6.gagner_experience(5)


    # Affichage de l'historique des événements
    journal.afficher_historique()



