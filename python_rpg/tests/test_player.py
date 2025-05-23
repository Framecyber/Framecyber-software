import unittest
import sys
import os

# Add project root to sys.path to allow direct import of game modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from game_logic.player import Player
from game_logic.world import Area
# We might need Enemy for attack tests later, but not for these initial ones.
# from game_logic.enemy import Enemy 

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.start_area = Area("Test Start", "Starting point")
        self.next_area = Area("Next Room", "Another room")
        self.start_area.exits["east"] = self.next_area
        self.next_area.exits["west"] = self.start_area # For moving back
        
        self.player = Player(name="Test Hero", 
                             starting_area=self.start_area, 
                             health=100, 
                             attack_power=10, 
                             defense=5)

    def test_player_creation(self):
        self.assertEqual(self.player.name, "Test Hero")
        self.assertEqual(self.player.health, 100)
        self.assertEqual(self.player.max_health, 100)
        self.assertEqual(self.player.attack_power, 10)
        self.assertEqual(self.player.defense, 5)
        self.assertEqual(self.player.current_area, self.start_area)
        self.assertTrue(self.player.is_alive)

    def test_player_move_valid(self):
        # Suppress print output during tests
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            self.player.move("east")
            self.assertEqual(self.player.current_area, self.next_area)
            # Test moving back
            self.player.move("west")
            self.assertEqual(self.player.current_area, self.start_area)
        finally:
            sys.stdout.close()
            sys.stdout = original_stdout

    def test_player_move_invalid_direction(self):
        initial_area = self.player.current_area
        # Suppress print output during tests
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            self.player.move("north") # Assuming 'north' is not a valid exit
            self.assertEqual(self.player.current_area, initial_area)
        finally:
            sys.stdout.close()
            sys.stdout = original_stdout

    def test_player_take_damage_reduces_health(self):
        initial_health = self.player.health
        damage_taken = 20
        # Suppress print output during tests
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            self.player.take_damage(damage_taken)
            self.assertEqual(self.player.health, initial_health - damage_taken)
        finally:
            sys.stdout.close()
            sys.stdout = original_stdout

    def test_player_take_damage_cannot_go_below_zero(self):
        # Suppress print output during tests
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            self.player.take_damage(self.player.max_health + 50) # Excessive damage
            self.assertEqual(self.player.health, 0)
        finally:
            sys.stdout.close()
            sys.stdout = original_stdout
            
    def test_player_is_alive_property(self):
        self.assertTrue(self.player.is_alive)
        # Suppress print output during tests
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            self.player.take_damage(self.player.max_health)
            self.assertFalse(self.player.is_alive)
        finally:
            sys.stdout.close()
            sys.stdout = original_stdout

if __name__ == '__main__':
    unittest.main()
