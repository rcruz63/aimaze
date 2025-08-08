import random
from aimaze.events import EventType, GameEvent


def generate_random_event(location_context: str) -> GameEvent | None:
    """
    Genera un evento aleatorio ligero favoreciendo puzzles (implementación local para MVP).
    """
    if random.random() < 0.30:
        return None

    r = random.random()
    if r < 0.6:
        event_type = random.choice(
            [EventType.PUZZLE_RIDDLE, EventType.PUZZLE_LOGIC, EventType.PUZZLE_OBSERVATION]
        )
        if event_type == EventType.PUZZLE_RIDDLE:
            return GameEvent(
                event_type=event_type,
                description=(
                    "Un susurro recorre la estancia: 'No soy ser vivo, pero crezco; no tengo pulmones, pero necesito aire; no tengo boca, pero el agua me mata. ¿Qué soy?'"
                ),
                puzzle_solution="fuego",
                alternative_solutions=["la llama", "llama"],
                success_text="Una runa se ilumina y sientes una calidez que te reconforta.",
                failure_text="Las sombras se arremolinan, burlonas, dejándote en duda.",
                xp_reward=15,
                damage_on_failure=0,
            )
        if event_type == EventType.PUZZLE_LOGIC:
            return GameEvent(
                event_type=event_type,
                description=(
                    "Tres palancas numeradas 1, 2 y 3. Si 1 está arriba, 2 debe estar abajo; si 2 está arriba, 3 debe estar arriba; solo una configuración activa el mecanismo. ¿Cuál? (responde como '1 abajo, 2 arriba, 3 arriba')"
                ),
                puzzle_solution="1 abajo, 2 arriba, 3 arriba",
                alternative_solutions=["1 abajo 2 arriba 3 arriba"],
                success_text="Escuchas un chasquido y el muro se desplaza unos centímetros.",
                failure_text="El mecanismo vibra y se detiene, como si se riera de ti.",
                xp_reward=15,
                damage_on_failure=0,
            )
        return GameEvent(
            event_type=event_type,
            description=(
                "Un mural cubierto de polvo muestra símbolos repetidos: ◇◆◇◆◇. Falta uno al final. ¿Cuál sigue? (responde '◇' o '◆')"
            ),
            puzzle_solution="◇",
            alternative_solutions=["rombo", "diamante"],
            success_text="Un compartimento secreto se abre, revelando un pequeño relieve.",
            failure_text="Nada ocurre, salvo un rumor que parece burlarse.",
            xp_reward=10,
            damage_on_failure=0,
        )

    event_type = random.choice([EventType.OBSTACLE_PHYSICAL, EventType.ENCOUNTER_CREATURE])
    if event_type == EventType.OBSTACLE_PHYSICAL:
        return GameEvent(
            event_type=event_type,
            description="Un foso estrecho bloquea el paso. ¿Saltas? (responde 'saltar' o 'no')",
            puzzle_solution="saltar",
            alternative_solutions=["brincar", "saltar el foso"],
            success_text="Aterrizas al otro lado con una sonrisa triunfal.",
            failure_text="Dudas y pierdes el momento. El foso parece más ancho ahora...",
            xp_reward=8,
            damage_on_failure=0,
        )
    return GameEvent(
        event_type=event_type,
        description="Un murciélago gigante desciende en espiral. ¿Gritar o permanecer inmóvil?",
        puzzle_solution="permanecer inmóvil",
        alternative_solutions=["quedarse quieto", "quieto"],
        success_text="El murciélago te rodea y se aleja desinteresado.",
        failure_text="El grito lo irrita y rasga tu capa antes de irse.",
        xp_reward=12,
        damage_on_failure=5,
    )