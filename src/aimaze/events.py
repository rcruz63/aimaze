from __future__ import annotations

import random
from enum import Enum
from typing import List, Optional, Tuple

from pydantic import BaseModel, Field


class EventType(str, Enum):
    PUZZLE_RIDDLE = "PUZZLE_RIDDLE"
    PUZZLE_LOGIC = "PUZZLE_LOGIC"
    PUZZLE_OBSERVATION = "PUZZLE_OBSERVATION"
    OBSTACLE_PHYSICAL = "OBSTACLE_PHYSICAL"
    ENCOUNTER_CREATURE = "ENCOUNTER_CREATURE"
    ENCOUNTER_NPC = "ENCOUNTER_NPC"


class GameEvent(BaseModel):
    event_type: EventType
    description: str
    ascii_art: Optional[str] = Field(
        default=None,
        description="Arte ASCII para el evento (onomatopeyas, dibujos, texto misterioso)",
    )
    puzzle_solution: Optional[str] = Field(
        default=None, description="Solución esperada para eventos de rompecabezas"
    )
    alternative_solutions: List[str] = Field(
        default_factory=list, description="Soluciones alternativas válidas"
    )
    success_text: str
    failure_text: str
    xp_reward: int = 0
    item_reward: Optional[str] = Field(
        default=None, description="ID del objeto otorgado en caso de éxito"
    )
    clue_reward: Optional[str] = Field(
        default=None, description="Texto de pista otorgado en caso de éxito"
    )
    damage_on_failure: int = 0
    # Campos para futuras fases multi-habitación (placeholders)
    event_size: int = Field(1, description="Número de habitaciones clave involucradas")
    related_locations: List[str] = Field(
        default_factory=list, description="Otras coordenadas de habitaciones involucradas"
    )


def _normalize_answer(value: Optional[str]) -> str:
    if value is None:
        return ""
    return value.strip().lower()


def resolve_event(
    game_state: dict, event: GameEvent, player_input: Optional[str]
) -> Tuple[bool, str]:
    """
    Resuelve un evento, actualizando game_state (XP/salud) y devolviendo el resultado.
    Para eventos de rompecabezas, compara la entrada normalizada con las soluciones esperadas.
    Para otros tipos, realiza una simple tirada de d20 si se especifica más adelante (no implementado aún).
    """
    player = game_state.get("player")

    # Handle puzzle-like events
    if event.event_type in {
        EventType.PUZZLE_RIDDLE,
        EventType.PUZZLE_LOGIC,
        EventType.PUZZLE_OBSERVATION,
    }:
        provided = _normalize_answer(player_input)
        expected = _normalize_answer(event.puzzle_solution)
        alternatives = {_normalize_answer(x) for x in event.alternative_solutions}

        success = False
        if provided and (provided == expected or provided in alternatives):
            success = True

        if success:
            if player:
                player.gain_xp(event.xp_reward)
            return True, event.success_text
        else:
            if player and event.damage_on_failure > 0:
                player.take_damage(event.damage_on_failure)
            return False, event.failure_text

    # Fallback for non-puzzle events: simple coin flip with narrative
    roll = random.randint(1, 20)
    success_threshold = 10
    success = roll >= success_threshold

    if success:
        if player:
            player.gain_xp(event.xp_reward)
        return True, event.success_text

    if player and event.damage_on_failure > 0:
        player.take_damage(event.damage_on_failure)
    return False, event.failure_text
