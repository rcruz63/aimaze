import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Añadir el directorio src al path para los imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from aimaze.display import display_scenario
from aimaze.ai_connector import LocationDescription


class TestDisplay(unittest.TestCase):
    
    def setUp(self):
        """Configurar datos de prueba"""
        self.mock_game_state = {
            "player_location_id": "inicio",
            "simulated_dungeon_layout": {
                "inicio": {
                    "description_id": "inicio_desc",
                    "options": {
                        "1": "pasillo",
                        "2": "salir_mazmorra"
                    }
                }
            }
        }
        
        self.mock_location_description = LocationDescription(
            description="Te encuentras en la entrada polvorienta de la mazmorra. Una brisa fría te abraza.",
            ascii_art="""
    ╔════════════════════════════════════════╗
    ║                ENTRADA                 ║
    ║                                        ║
    ║    [ ]                         [ ]     ║
    ║     |                           |      ║
    ║    ---                         ---     ║
    ║                                        ║
    ╚════════════════════════════════════════╝
            """
        )

    @patch('aimaze.display.generate_location_description')
    @patch('builtins.print')
    def test_display_scenario_with_ai_generation(self, mock_print, mock_generate):
        """Test que display_scenario usa IA para generar descripciones"""
        # Configurar el mock
        mock_generate.return_value = self.mock_location_description
        
        # Ejecutar la función
        display_scenario(self.mock_game_state)
        
        # Verificar que se llamó a la función de IA
        mock_generate.assert_called_once_with("inicio - inicio_desc")
        
        # Verificar que se almacenó en game_state
        self.assertIn("location_description_inicio", self.mock_game_state)
        self.assertEqual(
            self.mock_game_state["location_description_inicio"], 
            self.mock_location_description
        )
        
        # Verificar que se imprimieron la descripción y ASCII art
        printed_calls = [call[0][0] for call in mock_print.call_args_list]
        
        # Verificar que se imprimió el ASCII art
        self.assertIn(self.mock_location_description.ascii_art, printed_calls)
        
        # Verificar que se imprimió la descripción
        self.assertIn(self.mock_location_description.description, printed_calls)

    @patch('builtins.print')
    def test_display_scenario_with_cached_description(self, mock_print):
        """Test que display_scenario usa descripción cacheada si ya existe"""
        # Añadir descripción cacheada al game_state
        self.mock_game_state["location_description_inicio"] = self.mock_location_description
        
        with patch('aimaze.display.generate_location_description') as mock_generate:
            # Ejecutar la función
            display_scenario(self.mock_game_state)
            
            # Verificar que NO se llamó a la función de IA
            mock_generate.assert_not_called()
            
            # Verificar que se imprimieron la descripción y ASCII art cacheados
            printed_calls = [call[0][0] for call in mock_print.call_args_list]
            self.assertIn(self.mock_location_description.ascii_art, printed_calls)
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
        self.assertIn("location_description_inicio", self.mock_game_state)
        fallback_desc = self.mock_game_state["location_description_inicio"]
        
        # Verificar que es una instancia de LocationDescription
        self.assertIsInstance(fallback_desc, LocationDescription)
        self.assertIn("inicio", fallback_desc.description)

    @patch('builtins.print')
    def test_display_scenario_unknown_location(self, mock_print):
        """Test que display_scenario maneja ubicaciones desconocidas"""
        # Configurar game_state con ubicación inexistente
        self.mock_game_state["player_location_id"] = "ubicacion_inexistente"
        
        # Ejecutar la función
        display_scenario(self.mock_game_state)
        
        # Verificar que se establece game_over
        self.assertTrue(self.mock_game_state["game_over"])
        
        # Verificar que se imprimió mensaje de error
        printed_calls = [call[0][0] for call in mock_print.call_args_list]
        error_messages = [msg for msg in printed_calls if "ERROR" in str(msg)]
        self.assertTrue(any(error_messages))


if __name__ == '__main__':
    unittest.main() 