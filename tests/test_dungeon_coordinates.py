import unittest
from unittest.mock import patch
import sys
import os

# Añadir el directorio src al path para los imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from aimaze.dungeon import PlayerLocation, Room, Level, Dungeon, get_room_at_coords
from aimaze.ai_connector import generate_dungeon_layout
from typing import Dict, Tuple


class TestDungeonCoordinates(unittest.TestCase):
    """
    Tests para validar los nuevos modelos de coordenadas y funciones helper.
    Verifica PlayerLocation, Room, Level, Dungeon y get_room_at_coords.
    """

    def setUp(self):
        """Configuración para cada test"""
        # Crear un archivo .env temporal para los tests
        with open('.env', 'w') as f:
            f.write('OPENAI_API_KEY=test_key\n')

    def test_player_location_creation_and_to_string(self):
        """Test PlayerLocation.to_string() devuelve formato correcto 'nivel:x:y'"""
        # Test casos básicos
        location1 = PlayerLocation(level=1, x=0, y=0)
        self.assertEqual(location1.to_string(), "1:0:0")
        
        location2 = PlayerLocation(level=2, x=5, y=3)
        self.assertEqual(location2.to_string(), "2:5:3")
        
        location3 = PlayerLocation(level=10, x=15, y=25)
        self.assertEqual(location3.to_string(), "10:15:25")
        
        # Test valores negativos (aunque no deberían ocurrir en uso normal)
        location4 = PlayerLocation(level=1, x=0, y=0)
        self.assertEqual(location4.to_string(), "1:0:0")

    def test_player_location_attributes(self):
        """Test que PlayerLocation tiene los atributos correctos"""
        location = PlayerLocation(level=3, x=7, y=2)
        
        self.assertEqual(location.level, 3)
        self.assertEqual(location.x, 7)
        self.assertEqual(location.y, 2)
        self.assertIsInstance(location.level, int)
        self.assertIsInstance(location.x, int)
        self.assertIsInstance(location.y, int)

    def test_room_model_structure(self):
        """Test que Room tiene la estructura correcta"""
        # Crear una habitación de prueba
        test_connections = {
            'north': (1, 2),
            'south': (1, 0),
            'east': (2, 1)
        }
        
        room = Room(
            id="1,1",
            coordinates=(1, 1),
            connections=test_connections
        )
        
        # Verificar atributos
        self.assertEqual(room.id, "1,1")
        self.assertEqual(room.coordinates, (1, 1))
        self.assertEqual(room.connections, test_connections)
        
        # Verificar tipos
        self.assertIsInstance(room.id, str)
        self.assertIsInstance(room.coordinates, tuple)
        self.assertIsInstance(room.connections, dict)
        self.assertEqual(len(room.coordinates), 2)

    def test_room_connections_format(self):
        """Test que las conexiones de Room tienen el formato correcto"""
        test_connections = {
            'north': (0, 1),
            'south': (0, -1),
            'east': (1, 0),
            'west': (-1, 0)
        }
        
        room = Room(
            id="0,0",
            coordinates=(0, 0),
            connections=test_connections
        )
        
        # Verificar que las claves son direcciones cardinales válidas
        valid_directions = {'north', 'south', 'east', 'west'}
        for direction in room.connections.keys():
            self.assertIn(direction, valid_directions)
        
        # Verificar que los valores son tuplas de 2 elementos
        for direction, coords in room.connections.items():
            self.assertIsInstance(coords, tuple)
            self.assertEqual(len(coords), 2)
            self.assertIsInstance(coords[0], int)
            self.assertIsInstance(coords[1], int)

    def test_level_model_structure(self):
        """Test que Level tiene la estructura correcta"""
        # Crear habitaciones de prueba
        test_rooms = {
            "0,0": Room(id="0,0", coordinates=(0, 0), connections={'east': (1, 0)}),
            "1,0": Room(id="1,0", coordinates=(1, 0), connections={'west': (0, 0)})
        }
        
        level = Level(
            id=1,
            width=3,
            height=3,
            start_coords=(0, 0),
            exit_coords=(1, 0),
            rooms=test_rooms
        )
        
        # Verificar atributos básicos
        self.assertEqual(level.id, 1)
        self.assertEqual(level.width, 3)
        self.assertEqual(level.height, 3)
        self.assertEqual(level.start_coords, (0, 0))
        self.assertEqual(level.exit_coords, (1, 0))
        self.assertEqual(level.rooms, test_rooms)
        
        # Verificar tipos
        self.assertIsInstance(level.id, int)
        self.assertIsInstance(level.width, int)
        self.assertIsInstance(level.height, int)
        self.assertIsInstance(level.start_coords, tuple)
        self.assertIsInstance(level.exit_coords, tuple)
        self.assertIsInstance(level.rooms, dict)

    def test_dungeon_model_structure(self):
        """Test que Dungeon tiene la estructura correcta"""
        # Crear un nivel de prueba
        test_rooms = {
            "0,0": Room(id="0,0", coordinates=(0, 0), connections={'east': (1, 0)}),
            "1,0": Room(id="1,0", coordinates=(1, 0), connections={'west': (0, 0)})
        }
        
        test_level = Level(
            id=1,
            width=2,
            height=1,
            start_coords=(0, 0),
            exit_coords=(1, 0),
            rooms=test_rooms
        )
        
        dungeon = Dungeon(
            total_levels=1,
            current_level=1,
            levels={1: test_level}
        )
        
        # Verificar atributos
        self.assertEqual(dungeon.total_levels, 1)
        self.assertEqual(dungeon.current_level, 1)
        self.assertIn(1, dungeon.levels)
        self.assertEqual(dungeon.levels[1], test_level)
        
        # Verificar tipos
        self.assertIsInstance(dungeon.total_levels, int)
        self.assertIsInstance(dungeon.current_level, int)
        self.assertIsInstance(dungeon.levels, dict)

    def test_get_room_at_coords_function(self):
        """Test get_room_at_coords() encuentra habitaciones por coordenadas correctamente"""
        # Crear habitaciones de prueba
        room1 = Room(id="0,0", coordinates=(0, 0), connections={'east': (1, 0)})
        room2 = Room(id="1,0", coordinates=(1, 0), connections={'west': (0, 0), 'north': (1, 1)})
        room3 = Room(id="1,1", coordinates=(1, 1), connections={'south': (1, 0)})
        
        test_rooms = {
            "0,0": room1,
            "1,0": room2,
            "1,1": room3
        }
        
        level = Level(
            id=1,
            width=2,
            height=2,
            start_coords=(0, 0),
            exit_coords=(1, 1),
            rooms=test_rooms
        )
        
        # Test casos exitosos
        found_room1 = get_room_at_coords(level, 0, 0)
        self.assertIsNotNone(found_room1)
        self.assertEqual(found_room1.id, "0,0")
        self.assertEqual(found_room1.coordinates, (0, 0))
        
        found_room2 = get_room_at_coords(level, 1, 0)
        self.assertIsNotNone(found_room2)
        self.assertEqual(found_room2.id, "1,0")
        self.assertEqual(found_room2.coordinates, (1, 0))
        
        found_room3 = get_room_at_coords(level, 1, 1)
        self.assertIsNotNone(found_room3)
        self.assertEqual(found_room3.id, "1,1")
        self.assertEqual(found_room3.coordinates, (1, 1))
        
        # Test casos donde no existe habitación
        not_found = get_room_at_coords(level, 0, 1)
        self.assertIsNone(not_found)
        
        not_found2 = get_room_at_coords(level, 2, 2)
        self.assertIsNone(not_found2)
        
        # Test coordenadas negativas
        not_found3 = get_room_at_coords(level, -1, 0)
        self.assertIsNone(not_found3)

    def test_generate_dungeon_layout_returns_valid_dungeon_instance(self):
        """Test para generate_dungeon_layout que verifique que devuelve una instancia Dungeon válida con coordenadas consistentes"""
        for i in range(5):  # Múltiples ejecuciones
            with self.subTest(iteration=i):
                dungeon = generate_dungeon_layout()
                
                # Verificar que es una instancia de Dungeon
                self.assertIsInstance(dungeon, Dungeon)
                
                # Verificar que tiene al menos un nivel
                self.assertGreaterEqual(dungeon.total_levels, 1)
                self.assertIn(dungeon.current_level, dungeon.levels)
                
                # Verificar el nivel actual
                current_level = dungeon.levels[dungeon.current_level]
                self.assertIsInstance(current_level, Level)
                
                # Verificar consistencia de coordenadas en todas las habitaciones
                for room_key, room in current_level.rooms.items():
                    self.assertIsInstance(room, Room)
                    
                    # Verificar que la clave coincide con las coordenadas
                    expected_key = f"{room.coordinates[0]},{room.coordinates[1]}"
                    self.assertEqual(room_key, expected_key)
                    
                    # Verificar que get_room_at_coords puede encontrar esta habitación
                    found_room = get_room_at_coords(current_level, room.coordinates[0], room.coordinates[1])
                    self.assertIsNotNone(found_room)
                    self.assertEqual(found_room.id, room.id)
                    self.assertEqual(found_room.coordinates, room.coordinates)

    def test_coordinate_consistency_across_models(self):
        """Test que verifica consistencia de coordenadas entre todos los modelos"""
        dungeon = generate_dungeon_layout()
        level = dungeon.levels[1]
        
        # Verificar que start_coords y exit_coords apuntan a habitaciones reales
        start_room = get_room_at_coords(level, level.start_coords[0], level.start_coords[1])
        self.assertIsNotNone(start_room, "start_coords no apunta a una habitación válida")
        
        exit_room = get_room_at_coords(level, level.exit_coords[0], level.exit_coords[1])
        self.assertIsNotNone(exit_room, "exit_coords no apunta a una habitación válida")
        
        # Verificar que PlayerLocation puede ser creado con las coordenadas del nivel
        start_location = PlayerLocation(level=1, x=level.start_coords[0], y=level.start_coords[1])
        self.assertEqual(start_location.level, 1)
        self.assertEqual(start_location.x, level.start_coords[0])
        self.assertEqual(start_location.y, level.start_coords[1])
        
        # Verificar formato de string de PlayerLocation
        expected_string = f"1:{level.start_coords[0]}:{level.start_coords[1]}"
        self.assertEqual(start_location.to_string(), expected_string)

    def test_room_connections_point_to_valid_coordinates(self):
        """Test que verifica que todas las conexiones apuntan a coordenadas válidas dentro del nivel"""
        dungeon = generate_dungeon_layout()
        level = dungeon.levels[1]
        
        for room_key, room in level.rooms.items():
            for direction, target_coords in room.connections.items():
                # Verificar que las coordenadas objetivo están dentro de límites
                self.assertGreaterEqual(target_coords[0], 0, f"Conexión {direction} X fuera de límites")
                self.assertLess(target_coords[0], level.width, f"Conexión {direction} X fuera de límites")
                self.assertGreaterEqual(target_coords[1], 0, f"Conexión {direction} Y fuera de límites")
                self.assertLess(target_coords[1], level.height, f"Conexión {direction} Y fuera de límites")
                
                # Verificar que get_room_at_coords puede encontrar la habitación objetivo
                target_room = get_room_at_coords(level, target_coords[0], target_coords[1])
                self.assertIsNotNone(target_room, 
                                   f"Habitación {room.id} conecta a coordenadas inexistentes {target_coords}")

    def test_player_location_edge_cases(self):
        """Test casos límite para PlayerLocation"""
        # Coordenadas en el origen
        location1 = PlayerLocation(level=1, x=0, y=0)
        self.assertEqual(location1.to_string(), "1:0:0")
        
        # Coordenadas grandes
        location2 = PlayerLocation(level=999, x=100, y=200)
        self.assertEqual(location2.to_string(), "999:100:200")
        
        # Verificar que PlayerLocation es un modelo Pydantic válido
        self.assertIsInstance(location1, PlayerLocation)
        self.assertIsInstance(location2, PlayerLocation)

    def test_room_id_coordinate_consistency(self):
        """Test que verifica que room_key siempre coincide con las coordenadas de la habitación"""
        dungeon = generate_dungeon_layout()
        level = dungeon.levels[1]
        
        for room_key, room in level.rooms.items():
            # Verificar que room_key coincide con el formato de coordenadas
            expected_key = f"{room.coordinates[0]},{room.coordinates[1]}"
            self.assertEqual(room_key, expected_key)
            
            # Verificar que room.id es un string válido (puede ser descriptivo)
            self.assertIsInstance(room.id, str)
            self.assertGreater(len(room.id), 0)
            
            # Verificar que las coordenadas de la habitación coinciden con su posición en el diccionario
            self.assertEqual(room.coordinates, (int(room_key.split(',')[0]), int(room_key.split(',')[1])))


if __name__ == '__main__':
    unittest.main() 