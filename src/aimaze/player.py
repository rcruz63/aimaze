# quest_manager.py characters.py localization.py save_load.py

from pydantic import BaseModel, Field
from typing import List


class Player(BaseModel):
    """Modelo del jugador usando Pydantic BaseModel."""
    
    strength: int = 10
    dexterity: int = 10
    intelligence: int = 10
    perception: int = 10
    health: int = 100
    max_health: int = 100
    experience: int = 0
    inventory: List[str] = Field(default_factory=list)
    
    def gain_xp(self, amount: int) -> None:
        """Aumenta la experiencia del jugador."""
        self.experience += amount
    
    def take_damage(self, amount: int) -> None:
        """Reduce la salud del jugador, sin bajar de 0."""
        self.health = max(0, self.health - amount)
