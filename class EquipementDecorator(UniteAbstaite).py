class EquipementDecorator(UniteAbstaite):
    """Classe de base pour les décorateurs d'équipement."""
    def __init__(self, soldat: Soldat):
        super().__init__(soldat.name)
        self.soldat = soldat
    
    def get_effectif(self) -> int:
        return self.soldat.get_effectif()
    
    def afficher(self, indent: int = 0):
        self.soldat.afficher(indent)

class FusilDecorator(EquipementDecorator):
    """Décorateur pour ajouter un fusil à un soldat."""
    def __init__(self, soldat: Soldat):
        super().__init__(soldat)
        self.soldat.puissance += 5
        self.notify(f"{self.soldat.name} équipé d'un fusil (+5 puissance).")

    def get_puissance_totale(self) -> int:
        return self.soldat.get_puissance_totale()
    
    def afficher(self, indent: int = 0):
        print("  " * indent + f"└─ {self.soldat.grade} {self.soldat.name} [F:{self.soldat.puissance} D:{self.soldat.defense}⬆ V:{self.soldat.vitesse}] +Fusil")

class GiletPareBallesDecorator(EquipementDecorator):
    """Décorateur pour ajouter un gilet pare-balles à un soldat."""
    def __init__(self, soldat: Soldat):
        super().__init__(soldat)
        self.soldat.defense += 5
        self.notify(f"{self.soldat.name} équipé d'un gilet pare-balles (+5 défense).")

    def get_puissance_totale(self) -> int:
        return self.soldat.get_puissance_totale()
    
    def afficher(self, indent=0):
        print("  " * indent + f"└─ {self.soldat.grade} {self.soldat.name} [F:{self.soldat.puissance} D:{self.soldat.defense}⬆ V:{self.soldat.vitesse}] +Gilet")

class BottesOfficierDecorator(EquipementDecorator):
    """Décorateur pour ajouter des bottes d'officier à un soldat."""
    def __init__(self, soldat: Soldat):
        super().__init__(soldat)
        self.soldat.vitesse += 5
        self.notify(f"{self.soldat.name} équipé de bottes d'officier (+5 vitesse).")
    
    def get_puissance_totale(self) -> int:
        return self.soldat.get_puissance_totale()
    
    def afficher(self, indent=0):
        print("  " * indent + f"└─ {self.soldat.grade} {self.soldat.name} [F:{self.soldat.puissance} D:{self.soldat.defense}⬆ V:{self.soldat.vitesse}] +Bottes")