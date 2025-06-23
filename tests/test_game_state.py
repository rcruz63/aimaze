import unittest
from unittest.mock import patch, MagicMock
from aimaze.game_state import initialize_game_state
from aimaze.player import Player
from aimaze.dungeon import PlayerLocation, Dungeon, Level, Room

class TestGameState(unittest.TestCase):
    @patch('aimaze.game_state.load_config')
    @patch('aimaze.game_state.generate_dungeon_layout')
    def test_initialize_game_state_returns_expected_keys(self, mock_generate_dungeon, mock_load_config):
        # Crear una mazmorra de prueba para el mock
        test_room = Room(
            id="start_room",
            coordinates=(0, 0),
            connections={'east': (1, 0)}
        )
        
        test_level = Level(
            id=1,
            width=3,
            height=3,
            start_coords=(0, 0),
            exit_coords=(2, 2),
            rooms={"0,0": test_room}
        )
        
        test_dungeon = Dungeon(
            total_levels=1,
            current_level=1,
            levels={1: test_level}
        )
        
        # Configurar el mock de generate_dungeon_layout
        mock_generate_dungeon.return_value = test_dungeon

        # Llamar a la función bajo prueba
        game_state = initialize_game_state()

        # Verificar que se llamó a load_config
        mock_load_config.assert_called_once()

        # Verificar que se llamó a generate_dungeon_layout
        mock_generate_dungeon.assert_called_once()

        # Verificar las claves básicas esperadas con nueva estructura
        self.assertIn("player_location", game_state)
        self.assertIn("game_over", game_state)
        self.assertIn("objective_achieved", game_state)
        self.assertIn("player", game_state)
        self.assertIn("dungeon", game_state)

        # Verificar los valores iniciales
        self.assertFalse(game_state["game_over"])
        self.assertFalse(game_state["objective_achieved"])
        
        # Verificar que player es una instancia de Player
        self.assertIsInstance(game_state["player"], Player)
        
        # Verificar que player_location es una instancia de PlayerLocation
        self.assertIsInstance(game_state["player_location"], PlayerLocation)
        
        # Verificar que dungeon es una instancia de Dungeon
        self.assertIsInstance(game_state["dungeon"], Dungeon)
        
        # Verificar la ubicación inicial del jugador
        player_location = game_state["player_location"]
        self.assertEqual(player_location.level, 1)
        self.assertEqual(player_location.x, 0)
        self.assertEqual(player_location.y, 0)
        
        # Verificar los atributos iniciales del jugador
        player = game_state["player"]
        self.assertEqual(player.strength, 10)
        self.assertEqual(player.dexterity, 10)
        self.assertEqual(player.intelligence, 10)
        self.assertEqual(player.perception, 10)
        self.assertEqual(player.health, 100)
        self.assertEqual(player.max_health, 100)
        self.assertEqual(player.experience, 0)
        self.assertEqual(player.inventory, [])

if __name__ == '__main__':
    unittest.main() 