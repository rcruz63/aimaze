import unittest
from unittest.mock import patch, MagicMock
from aimaze.game_state import initialize_game_state

class TestGameState(unittest.TestCase):
    @patch('aimaze.game_state.load_config')
    @patch('aimaze.game_state.get_simulated_dungeon_layout')
    def test_initialize_game_state_returns_expected_keys(self, mock_dungeon_layout, mock_load_config):
        # Configurar el mock de get_simulated_dungeon_layout
        mock_dungeon_layout.return_value = {
            "inicio": {"connections": {"north": "sala_1"}},
            "sala_1": {"connections": {"south": "inicio", "north": "salida"}},
            "salida": {"connections": {"south": "sala_1"}}
        }

        # Llamar a la función bajo prueba
        game_state = initialize_game_state()

        # Verificar que se llamó a load_config
        mock_load_config.assert_called_once()

        # Verificar que se llamó a get_simulated_dungeon_layout
        mock_dungeon_layout.assert_called_once()

        # Verificar las claves básicas esperadas
        self.assertIn("player_location_id", game_state)
        self.assertIn("game_over", game_state)
        self.assertIn("objective_achieved", game_state)
        self.assertIn("player_attributes", game_state)
        self.assertIn("inventory", game_state)
        self.assertIn("simulated_dungeon_layout", game_state)

        # Verificar los valores iniciales
        self.assertEqual(game_state["player_location_id"], "inicio")
        self.assertFalse(game_state["game_over"])
        self.assertFalse(game_state["objective_achieved"])
        self.assertEqual(game_state["player_attributes"], {})
        self.assertEqual(game_state["inventory"], [])

if __name__ == '__main__':
    unittest.main() 