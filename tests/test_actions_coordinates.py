import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Añadir el directorio src al path para los imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from aimaze.actions import process_player_action, validate_player_input, get_action_description
from aimaze.dungeon import PlayerLocation, Dungeon, Level, Room
from aimaze.player import Player


class TestActionsCoordinates(unittest.TestCase):
    
    def setUp(self):
        """Configurar datos de prueba con nueva estructura PlayerLocation y Dungeon"""
        # Crear habitaciones de prueba conectadas
        room_start = Room(
            id="room_start", 
            coordinates=(0, 0),
            connections={
                'east': (1, 0),
                'south': (0, 1)
            }
        )
        
        room_east = Room(
            id="room_east", 
            coordinates=(1, 0),
            connections={
                'west': (0, 0),
                'south': (1, 1)
            }
        )
        
        room_exit = Room(
            id="room_exit", 
            coordinates=(2, 2),
            connections={
                'west': (1, 2),
                'north': (2, 1)
            }
        )
        
        # Crear un nivel de prueba
        test_level = Level(
            id=1,
            width=3,
            height=3,
            start_coords=(0, 0),
            exit_coords=(2, 2),
            rooms={
                "0,0": room_start,
                "1,0": room_east,
                "2,2": room_exit
            }
        )
        
        # Crear mazmorra de prueba
        test_dungeon = Dungeon(
            total_levels=1,
            current_level=1,
            levels={1: test_level}
        )
        
        # Game state con nueva estructura
        self.mock_game_state = {
            "player_location": PlayerLocation(level=1, x=0, y=0),
            "dungeon": test_dungeon,
            "player": Player(),
            "game_over": False,
            "objective_achieved": False,
            "current_options_map": {
                "1": ("east", (1, 0)),
                "2": ("south", (0, 1)),
                "3": ("save", None)
            }
        }

    @patch('builtins.print')
    def test_process_player_action_valid_movement(self, mock_print):
        """Test que process_player_action actualiza correctamente PlayerLocation"""
        initial_x = self.mock_game_state["player_location"].x
        initial_y = self.mock_game_state["player_location"].y
        
        # Simular movimiento al este
        result_state = process_player_action(self.mock_game_state, "1")
        
        # Verificar que la ubicación se actualizó correctamente
        self.assertEqual(result_state["player_location"].x, 1)
        self.assertEqual(result_state["player_location"].y, 0)
        self.assertEqual(result_state["player_location"].level, 1)
        
        # Verificar que se imprimió el mensaje de movimiento
        printed_calls = [str(call[0][0]) for call in mock_print.call_args_list]
        movement_message_found = any("Te mueves hacia el Este" in call for call in printed_calls)
        self.assertTrue(movement_message_found, "Debería aparecer mensaje de movimiento")

    @patch('builtins.print')
    def test_process_player_action_invalid_direction(self, mock_print):
        """Test que process_player_action maneja direcciones inválidas correctamente"""
        # Modificar las opciones para incluir una dirección que no existe en room.connections
        self.mock_game_state["current_options_map"]["4"] = ("north", (0, -1))
        
        # Simular movimiento al norte (no disponible desde la habitación inicial)
        result_state = process_player_action(self.mock_game_state, "4")
        
        # Verificar que la ubicación NO se actualizó
        self.assertEqual(result_state["player_location"].x, 0)
        self.assertEqual(result_state["player_location"].y, 0)
        
        # Verificar que se imprimió mensaje de error
        printed_calls = [str(call[0][0]) for call in mock_print.call_args_list]
        error_message_found = any("No puedes ir hacia el north" in call for call in printed_calls)
        self.assertTrue(error_message_found, "Debería aparecer mensaje de error")

    @patch('builtins.print')
    def test_process_player_action_coordinates_out_of_bounds(self, mock_print):
        """Test que process_player_action maneja coordenadas fuera de límites"""
        # Modificar las conexiones para apuntar fuera de límites
        room_start = self.mock_game_state["dungeon"].levels[1].rooms["0,0"]
        room_start.connections["north"] = (0, -1)  # Fuera de límites
        
        # Añadir la opción al mapa
        self.mock_game_state["current_options_map"]["4"] = ("north", (0, -1))
        
        # Simular movimiento fuera de límites
        result_state = process_player_action(self.mock_game_state, "4")
        
        # Verificar que la ubicación NO se actualizó
        self.assertEqual(result_state["player_location"].x, 0)
        self.assertEqual(result_state["player_location"].y, 0)
        
        # Verificar que se imprimió mensaje de error de límites
        printed_calls = [str(call[0][0]) for call in mock_print.call_args_list]
        bounds_error_found = any("fuera de los límites del nivel" in call for call in printed_calls)
        self.assertTrue(bounds_error_found, "Debería aparecer mensaje de error de límites")

    @patch('builtins.print')
    def test_process_player_action_exit_detection(self, mock_print):
        """Test que process_player_action detecta condiciones de salida basadas en exit_coords"""
        # Mover el jugador a la coordenada de salida
        self.mock_game_state["player_location"].x = 2
        self.mock_game_state["player_location"].y = 2
        
        # Simular acción de salida
        self.mock_game_state["current_options_map"]["1"] = ("exit", None)
        result_state = process_player_action(self.mock_game_state, "1")
        
        # Verificar que se estableció objective_achieved
        self.assertTrue(result_state["objective_achieved"])
        self.assertTrue(result_state["game_over"])
        
        # Verificar mensaje de éxito
        printed_calls = [str(call[0][0]) for call in mock_print.call_args_list]
        success_message_found = any("Felicidades" in call and "escapado" in call for call in printed_calls)
        self.assertTrue(success_message_found, "Debería aparecer mensaje de éxito")

    @patch('builtins.print')
    def test_process_player_action_exit_from_wrong_location(self, mock_print):
        """Test que process_player_action maneja intento de salida desde ubicación incorrecta"""
        # El jugador está en (0,0) pero la salida está en (2,2)
        self.mock_game_state["current_options_map"]["1"] = ("exit", None)
        result_state = process_player_action(self.mock_game_state, "1")
        
        # Verificar que NO se estableció objective_achieved
        self.assertFalse(result_state.get("objective_achieved", False))
        self.assertFalse(result_state["game_over"])
        
        # Verificar mensaje de error
        printed_calls = [str(call[0][0]) for call in mock_print.call_args_list]
        error_message_found = any("No puedes salir desde aquí" in call for call in printed_calls)
        self.assertTrue(error_message_found, "Debería aparecer mensaje de error de salida")

    @patch('aimaze.actions.save_game')
    @patch('builtins.print')
    def test_process_player_action_save_game(self, mock_print, mock_save_game):
        """Test que process_player_action maneja la acción de guardar correctamente"""
        # Simular acción de guardar
        result_state = process_player_action(self.mock_game_state, "3")
        
        # Verificar que se llamó a save_game
        mock_save_game.assert_called_once_with(self.mock_game_state)
        
        # Verificar mensaje de éxito
        printed_calls = [str(call[0][0]) for call in mock_print.call_args_list]
        save_message_found = any("Partida guardada exitosamente" in call for call in printed_calls)
        self.assertTrue(save_message_found, "Debería aparecer mensaje de guardado exitoso")

    @patch('aimaze.actions.save_game')
    @patch('builtins.print')
    def test_process_player_action_save_game_error(self, mock_print, mock_save_game):
        """Test que process_player_action maneja errores de guardado"""
        # Configurar save_game para que falle
        mock_save_game.side_effect = Exception("Error de guardado simulado")
        
        # Simular acción de guardar
        result_state = process_player_action(self.mock_game_state, "3")
        
        # Verificar mensaje de error
        printed_calls = [str(call[0][0]) for call in mock_print.call_args_list]
        error_message_found = any("Error al guardar la partida" in call for call in printed_calls)
        self.assertTrue(error_message_found, "Debería aparecer mensaje de error de guardado")

    def test_validate_player_input(self):
        """Test de la función validate_player_input"""
        valid_options = {"1": ("east", (1, 0)), "2": ("south", (0, 1))}
        
        # Test con entrada válida
        self.assertTrue(validate_player_input("1", valid_options))
        self.assertTrue(validate_player_input("2", valid_options))
        
        # Test con entrada inválida
        self.assertFalse(validate_player_input("3", valid_options))
        self.assertFalse(validate_player_input("invalid", valid_options))

    def test_get_action_description(self):
        """Test de la función get_action_description"""
        # Test con direcciones
        self.assertIn("Norte", get_action_description("north"))
        self.assertIn("Sur", get_action_description("south"))
        self.assertIn("Este", get_action_description("east"))
        self.assertIn("Oeste", get_action_description("west"))
        
        # Test con coordenadas
        description = get_action_description("east", (1, 0))
        self.assertIn("Este", description)
        self.assertIn("(1, 0)", description)
        
        # Test con acciones especiales
        self.assertIn("salir", get_action_description("exit").lower())
        self.assertIn("guardar", get_action_description("save").lower())


if __name__ == '__main__':
    unittest.main() 