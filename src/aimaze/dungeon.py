# src/aimaze/dungeon.py

from pydantic import BaseModel, Field
from typing import Dict, List, Tuple, Optional


class PlayerLocation(BaseModel):
    """Represents the player's location in the dungeon using coordinates."""
    level: int
    x: int
    y: int
    
    def to_string(self) -> str:
        """Returns location in format 'nivel:x:y'."""
        return f"{self.level}:{self.x}:{self.y}"


class Room(BaseModel):
    """Represents a single room in the dungeon."""
    id: str
    coordinates: Tuple[int, int]
    connections: Dict[str, Tuple[int, int]] = Field(
        default_factory=dict,
        description="Dictionary where keys are directions ('north', 'south', 'east', 'west') and values are coordinates (x, y) of adjacent rooms within the same level"
    )


class Level(BaseModel):
    """Represents a complete level of the dungeon."""
    id: int
    width: int
    height: int
    start_coords: Tuple[int, int]
    exit_coords: Tuple[int, int]
    rooms: Dict[str, Room] = Field(
        default_factory=dict,
        description="Dictionary where key is 'x,y' coordinate string and value is the Room object"
    )


class Dungeon(BaseModel):
    """Represents the complete dungeon with multiple levels."""
    total_levels: int
    current_level: int = 1
    levels: Dict[int, Level] = Field(default_factory=dict)


def get_room_at_coords(level: Level, x: int, y: int) -> Optional[Room]:
    """
    Helper function to get a room at specific coordinates within a level.
    
    Args:
        level: The Level object to search in
        x: X coordinate of the room
        y: Y coordinate of the room
        
    Returns:
        Room object if found, None otherwise
    """
    coord_key = f"{x},{y}"
    return level.rooms.get(coord_key)
