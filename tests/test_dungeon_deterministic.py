import unittest
from unittest.mock import patch
import sys
import os

# Añadir el directorio src al path para los imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from aimaze.ai_connector import generate_dungeon_layout
from aimaze.dungeon import Dungeon, Level, Room, PlayerLocation


class TestDungeonDeterministic(unittest.TestCase):
    """
    Tests para validar la generación determinista de mazmorras.
    Verifica que generate_dungeon_layout() siempre produce mazmorras válidas y navegables.
    """

    def setUp(self):
        """Configuración para cada test"""
        # Crear un archivo .env temporal para los tests
        with open('.env', 'w') as f:
            f.write('OPENAI_API_KEY=test_key\n')

    def test_generate_dungeon_layout_returns_valid_dungeon(self):
        """Test que generate_dungeon_layout() siempre devuelve una Dungeon válida"""
        for i in range(10):  # Probar múltiples generaciones
            with self.subTest(iteration=i):
                dungeon = generate_dungeon_layout()
                
                # Verificar que es una instancia de Dungeon
                self.assertIsInstance(dungeon, Dungeon)
                
                # Verificar propiedades básicas
                self.assertGreaterEqual(dungeon.total_levels, 1)
                self.assertEqual(dungeon.current_level, 1)
                self.assertIn(1, dungeon.levels)
                
                # Verificar el nivel 1
                level_1 = dungeon.levels[1]
                self.assertIsInstance(level_1, Level)
                self.assertEqual(level_1.id, 1)
                self.assertGreater(level_1.width, 0)
                self.assertGreater(level_1.height, 0)
                self.assertIsInstance(level_1.rooms, dict)
                self.assertGreater(len(level_1.rooms), 0)

    def test_coordinates_within_bounds_multiple_executions(self):
        """Test que valida coordenadas dentro de límites para múltiples ejecuciones"""
        for i in range(15):  # Múltiples ejecuciones para mayor cobertura
            with self.subTest(execution=i):
                dungeon = generate_dungeon_layout()
                level = dungeon.levels[1]
                
                # Verificar que start_coords están dentro de límites
                start_x, start_y = level.start_coords
                self.assertGreaterEqual(start_x, 0)
                self.assertLess(start_x, level.width)
                self.assertGreaterEqual(start_y, 0)
                self.assertLess(start_y, level.height)
                
                # Verificar que exit_coords están dentro de límites
                exit_x, exit_y = level.exit_coords
                self.assertGreaterEqual(exit_x, 0)
                self.assertLess(exit_x, level.width)
                self.assertGreaterEqual(exit_y, 0)
                self.assertLess(exit_y, level.height)
                
                # Verificar que todas las habitaciones tienen coordenadas válidas
                for room_key, room in level.rooms.items():
                    room_x, room_y = room.coordinates
                    self.assertGreaterEqual(room_x, 0, f"Habitación {room.id} X fuera de límites")
                    self.assertLess(room_x, level.width, f"Habitación {room.id} X fuera de límites")
                    self.assertGreaterEqual(room_y, 0, f"Habitación {room.id} Y fuera de límites")
                    self.assertLess(room_y, level.height, f"Habitación {room.id} Y fuera de límites")
                    
                    # Verificar que la clave coincide con las coordenadas
                    expected_key = f"{room_x},{room_y}"
                    self.assertEqual(room_key, expected_key)
                    
                    # Verificar que todas las conexiones apuntan a coordenadas válidas
                    for direction, target_coords in room.connections.items():
                        target_x, target_y = target_coords
                        self.assertGreaterEqual(target_x, 0, f"Conexión {direction} X fuera de límites")
                        self.assertLess(target_x, level.width, f"Conexión {direction} X fuera de límites")
                        self.assertGreaterEqual(target_y, 0, f"Conexión {direction} Y fuera de límites")
                        self.assertLess(target_y, level.height, f"Conexión {direction} Y fuera de límites")

    def test_start_and_exit_coords_properly_defined(self):
        """Test que confirma que start_coords y exit_coords están correctamente definidas"""
        for i in range(10):
            with self.subTest(iteration=i):
                dungeon = generate_dungeon_layout()
                level = dungeon.levels[1]
                
                # Verificar que start_coords y exit_coords existen
                self.assertIsNotNone(level.start_coords)
                self.assertIsNotNone(level.exit_coords)
                
                # Verificar que son tuplas de 2 elementos
                self.assertIsInstance(level.start_coords, tuple)
                self.assertIsInstance(level.exit_coords, tuple)
                self.assertEqual(len(level.start_coords), 2)
                self.assertEqual(len(level.exit_coords), 2)
                
                # Verificar que start_coords y exit_coords son diferentes
                self.assertNotEqual(level.start_coords, level.exit_coords)
                
                # Verificar que existen habitaciones en start_coords y exit_coords
                start_key = f"{level.start_coords[0]},{level.start_coords[1]}"
                exit_key = f"{level.exit_coords[0]},{level.exit_coords[1]}"
                
                self.assertIn(start_key, level.rooms, "No existe habitación en start_coords")
                self.assertIn(exit_key, level.rooms, "No existe habitación en exit_coords")

    def test_complete_connectivity_all_rooms_reachable(self):
        """Test que verifica conectividad completa (todas las habitaciones alcanzables)"""
        for i in range(8):
            with self.subTest(iteration=i):
                dungeon = generate_dungeon_layout()
                level = dungeon.levels[1]
                
                # Usar BFS para verificar conectividad desde start_coords
                start_coords = level.start_coords
                visited = set()
                queue = [start_coords]
                
                while queue:
                    current_coords = queue.pop(0)
                    if current_coords in visited:
                        continue
                    
                    visited.add(current_coords)
                    current_key = f"{current_coords[0]},{current_coords[1]}"
                    
                    if current_key in level.rooms:
                        room = level.rooms[current_key]
                        # Añadir todas las habitaciones conectadas a la cola
                        for direction, neighbor_coords in room.connections.items():
                            if neighbor_coords not in visited:
                                queue.append(neighbor_coords)
                
                # Obtener todas las coordenadas de habitaciones existentes
                all_room_coords = set()
                for room in level.rooms.values():
                    all_room_coords.add(room.coordinates)
                
                # Verificar que todas las habitaciones son alcanzables
                unreachable_rooms = all_room_coords - visited
                self.assertEqual(len(unreachable_rooms), 0, 
                               f"Habitaciones no alcanzables detectadas: {unreachable_rooms}")
                
                # Verificar específicamente que exit_coords es alcanzable
                self.assertIn(level.exit_coords, visited, 
                            "La salida no es alcanzable desde el inicio")

    def test_main_path_exists_and_navigable(self):
        """Test que verifica que el camino principal existe y es navegable"""
        for i in range(10):
            with self.subTest(iteration=i):
                dungeon = generate_dungeon_layout()
                level = dungeon.levels[1]
                
                # Usar Dijkstra/BFS para encontrar el camino más corto
                start_coords = level.start_coords
                exit_coords = level.exit_coords
                
                # BFS para encontrar camino
                queue = [(start_coords, [start_coords])]
                visited = set()
                path_found = None
                
                while queue and not path_found:
                    current_coords, path = queue.pop(0)
                    
                    if current_coords == exit_coords:
                        path_found = path
                        break
                    
                    if current_coords in visited:
                        continue
                    
                    visited.add(current_coords)
                    current_key = f"{current_coords[0]},{current_coords[1]}"
                    
                    if current_key in level.rooms:
                        room = level.rooms[current_key]
                        for direction, neighbor_coords in room.connections.items():
                            if neighbor_coords not in visited:
                                new_path = path + [neighbor_coords]
                                queue.append((neighbor_coords, new_path))
                
                # Verificar que se encontró un camino
                self.assertIsNotNone(path_found, "No existe camino navegable desde inicio hasta salida")
                self.assertGreaterEqual(len(path_found), 2, "El camino debe tener al menos 2 habitaciones")
                self.assertEqual(path_found[0], start_coords, "El camino debe empezar en start_coords")
                self.assertEqual(path_found[-1], exit_coords, "El camino debe terminar en exit_coords")
                
                # Verificar que el camino es válido (cada paso está conectado)
                for j in range(len(path_found) - 1):
                    current = path_found[j]
                    next_room = path_found[j + 1]
                    current_key = f"{current[0]},{current[1]}"
                    
                    self.assertIn(current_key, level.rooms)
                    room = level.rooms[current_key]
                    
                    # Verificar que next_room está en las conexiones de current
                    connected_coords = list(room.connections.values())
                    self.assertIn(next_room, connected_coords, 
                                f"Habitación {current} no está conectada con {next_room}")

    def test_room_connections_are_bidirectional(self):
        """Test que verifica que las conexiones entre habitaciones son bidireccionales"""
        for i in range(5):
            with self.subTest(iteration=i):
                dungeon = generate_dungeon_layout()
                level = dungeon.levels[1]
                
                # Verificar bidireccionalidad de conexiones
                for room_key, room in level.rooms.items():
                    for direction, target_coords in room.connections.items():
                        target_key = f"{target_coords[0]},{target_coords[1]}"
                        
                        # Verificar que la habitación objetivo existe
                        self.assertIn(target_key, level.rooms, 
                                    f"Habitación {room.id} conecta a coordenadas inexistentes {target_coords}")
                        
                        target_room = level.rooms[target_key]
                        source_coords = room.coordinates
                        
                        # Verificar que existe conexión de vuelta
                        reverse_connection_exists = source_coords in target_room.connections.values()
                        self.assertTrue(reverse_connection_exists, 
                                      f"Conexión no bidireccional: {room.id}({room.coordinates}) -> {target_room.id}({target_coords})")

    def test_dungeon_generation_consistency(self):
        """Test que verifica consistencia en múltiples generaciones"""
        dungeons = []
        for i in range(5):
            dungeon = generate_dungeon_layout()
            dungeons.append(dungeon)
        
        # Verificar que todas las mazmorras tienen características básicas similares
        for i, dungeon in enumerate(dungeons):
            with self.subTest(dungeon=i):
                level = dungeon.levels[1]
                
                # Verificar rangos esperados de dimensiones
                self.assertIn(level.width, range(3, 6), "Ancho fuera de rango esperado")
                self.assertIn(level.height, range(3, 6), "Alto fuera de rango esperado")
                
                # Verificar que hay al menos 2 habitaciones (inicio y salida)
                self.assertGreaterEqual(len(level.rooms), 2)
                
                # Verificar que no excede el máximo posible
                max_possible_rooms = level.width * level.height
                self.assertLessEqual(len(level.rooms), max_possible_rooms)


if __name__ == '__main__':
    unittest.main() 