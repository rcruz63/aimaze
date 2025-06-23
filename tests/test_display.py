import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Añadir el directorio src al path para los imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from aimaze.display import display_scenario
from aimaze.ai_connector import LocationDescription
from aimaze.dungeon import PlayerLocation, Dungeon, Level, Room


class TestDisplay(unittest.TestCase):
    
    def setUp(self):
        """Configurar datos de prueba con nueva estructura PlayerLocation y Dungeon"""
        # Crear una habitación de prueba
        test_room = Room(
            id="test_room_start", 
            coordinates=(0, 0),
            connections={
                'east': (1, 0),
                'south': (0, 1)
            }
        )
        
        # Crear un nivel de prueba
        test_level = Level(
            id=1,
            width=3,
            height=3,
            start_coords=(0, 0),
            exit_coords=(2, 2),
            rooms={"0,0": test_room}
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
            "game_over": False
        }
        
        self.mock_location_description = LocationDescription(
            description="Te encuentras en la entrada polvorienta de la mazmorra. Una brisa fría te abraza."
        )

    @patch('aimaze.display.generate_location_description')
    @patch('builtins.print')
    def test_display_scenario_with_ai_generation(self, mock_print, mock_generate):
        """Test que display_scenario usa IA para generar descripciones"""
        # Configurar el mock
        mock_generate.return_value = self.mock_location_description
        
        # Ejecutar la función
        display_scenario(self.mock_game_state)
        
        # Verificar que se llamó a la función de IA con el contexto correcto
        expected_context = "Level 1 at (0,0) - test_room_start"
        mock_generate.assert_called_once_with(expected_context)
        
        # Verificar que se almacenó en game_state con la nueva clave
        expected_key = "location_description_1:0:0"
        self.assertIn(expected_key, self.mock_game_state)
        self.assertEqual(
            self.mock_game_state[expected_key], 
            self.mock_location_description
        )
        
        # Verificar que se imprimieron los elementos esperados
        printed_calls = [call[0][0] for call in mock_print.call_args_list]
        
        # Verificar que se imprimió la descripción
        self.assertIn(self.mock_location_description.description, printed_calls)
        
        # Verificar que se imprimió el encabezado con coordenadas
        location_header_found = any("[NIVEL 1 - POSICIÓN (0, 0)]" in str(call) for call in printed_calls)
        self.assertTrue(location_header_found, "El encabezado con coordenadas debería aparecer")

    @patch('builtins.print')
    def test_display_scenario_with_cached_description(self, mock_print):
        """Test que display_scenario usa descripción cacheada si ya existe"""
        # Añadir descripción cacheada al game_state con nueva clave
        cache_key = "location_description_1:0:0"
        self.mock_game_state[cache_key] = self.mock_location_description
        
        with patch('aimaze.display.generate_location_description') as mock_generate:
            # Ejecutar la función
            display_scenario(self.mock_game_state)
            
            # Verificar que NO se llamó a la función de IA
            mock_generate.assert_not_called()
            
            # Verificar que se imprimió la descripción cacheada
            printed_calls = [call[0][0] for call in mock_print.call_args_list]
            self.assertIn(self.mock_location_description.description, printed_calls)

    @patch('aimaze.display.generate_location_description')
    @patch('builtins.print')
    def test_display_scenario_with_ai_error(self, mock_print, mock_generate):
        """Test que display_scenario maneja errores de IA correctamente"""
        # Configurar el mock para que falle
        mock_generate.side_effect = Exception("Error de IA simulado")
        
        # Ejecutar la función
        display_scenario(self.mock_game_state)
        
        # Verificar que se creó una descripción de fallback
        cache_key = "location_description_1:0:0"
        self.assertIn(cache_key, self.mock_game_state)
        fallback_desc = self.mock_game_state[cache_key]
        
        # Verificar que es una instancia de LocationDescription
        self.assertIsInstance(fallback_desc, LocationDescription)
        self.assertIn("test_room_start", fallback_desc.description)

    @patch('builtins.print')
    def test_display_scenario_unknown_location(self, mock_print):
        """Test que display_scenario maneja ubicaciones desconocidas"""
        # Configurar game_state con coordenadas que no existen en la mazmorra
        self.mock_game_state["player_location"] = PlayerLocation(level=1, x=5, y=5)
        
        # Ejecutar la función
        display_scenario(self.mock_game_state)
        
        # Verificar que se establece game_over
        self.assertTrue(self.mock_game_state["game_over"])
        
        # Verificar que se imprimió mensaje de error
        printed_calls = [call[0][0] for call in mock_print.call_args_list]
        error_messages = [msg for msg in printed_calls if "ERROR" in str(msg)]
        self.assertTrue(any(error_messages))

    @patch('builtins.print')
    def test_display_scenario_options_generation(self, mock_print):
        """Test que display_scenario genera las opciones correctamente"""
        # Añadir descripción cacheada para evitar llamadas a IA
        cache_key = "location_description_1:0:0"
        self.mock_game_state[cache_key] = self.mock_location_description
        
        # Ejecutar la función
        display_scenario(self.mock_game_state)
        
        # Verificar que se generó el mapa de opciones
        self.assertIn("current_options_map", self.mock_game_state)
        options_map = self.mock_game_state["current_options_map"]
        
        # Verificar que las opciones están mapeadas correctamente basándose en las conexiones
        # La habitación tiene conexiones 'east' y 'south'
        self.assertIn("1", options_map)
        self.assertIn("2", options_map)
        
        # Verificar que cada opción tiene dirección y coordenadas
        for option_key, option_value in options_map.items():
            self.assertIsInstance(option_value, tuple)
            self.assertEqual(len(option_value), 2)  # (direction, coordinates)
        
        # Verificar que se imprimieron las opciones
        printed_calls = [str(call[0][0]) for call in mock_print.call_args_list]
        options_printed = any("Opciones:" in call for call in printed_calls)
        self.assertTrue(options_printed, "Las opciones deberían aparecer en la salida")


if __name__ == '__main__':
    unittest.main()
