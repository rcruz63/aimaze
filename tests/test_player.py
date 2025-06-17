import unittest
#import sys
#import os

# Añadir el directorio src al path para importar los módulos
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from aimaze.player import Player


class TestPlayer(unittest.TestCase):
    """Tests para la clase Player."""
    
    def test_player_initialization(self):
        """Test para verificar que una instancia de Player se inicializa con los atributos correctos."""
        player = Player()
        
        # Verificar atributos principales
        self.assertEqual(player.strength, 10)
        self.assertEqual(player.dexterity, 10)
        self.assertEqual(player.intelligence, 10)
        self.assertEqual(player.perception, 10)
        
        # Verificar atributos de salud
        self.assertEqual(player.health, 100)
        self.assertEqual(player.max_health, 100)
        
        # Verificar experiencia
        self.assertEqual(player.experience, 0)
        
        # Verificar inventario
        self.assertEqual(player.inventory, [])
        self.assertIsInstance(player.inventory, list)
    
    def test_gain_xp(self):
        """Test para gain_xp() que verifique que la experiencia se incrementa correctamente."""
        player = Player()
        
        # Experiencia inicial debe ser 0
        self.assertEqual(player.experience, 0)
        
        # Ganar 50 puntos de experiencia
        player.gain_xp(50)
        self.assertEqual(player.experience, 50)
        
        # Ganar más experiencia (acumulativa)
        player.gain_xp(25)
        self.assertEqual(player.experience, 75)
        
        # Verificar que funciona con cantidades grandes
        player.gain_xp(1000)
        self.assertEqual(player.experience, 1075)
    
    def test_take_damage(self):
        """Test para take_damage() que verifique que la salud se reduce correctamente."""
        player = Player()
        
        # Salud inicial debe ser 100
        self.assertEqual(player.health, 100)
        
        # Recibir 30 puntos de daño
        player.take_damage(30)
        self.assertEqual(player.health, 70)
        
        # Recibir más daño
        player.take_damage(20)
        self.assertEqual(player.health, 50)
        
        # Verificar que la salud no baja de 0
        player.take_damage(100)  # Más daño que la salud restante
        self.assertEqual(player.health, 0)
        
        # Verificar que no se puede ir por debajo de 0
        player.take_damage(50)
        self.assertEqual(player.health, 0)
    
    def test_take_damage_edge_cases(self):
        """Test para casos límite de take_damage."""
        player = Player()
        
        # Daño de 0 no debe cambiar la salud
        player.take_damage(0)
        self.assertEqual(player.health, 100)
        
        # Daño exacto a la salud actual
        player.take_damage(100)
        self.assertEqual(player.health, 0)


if __name__ == '__main__':
    unittest.main() 