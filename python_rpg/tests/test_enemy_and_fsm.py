import unittest
import sys
import os
import random # For testing defend state

# Add project root to sys.path to allow direct import of game modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from game_logic.enemy import Enemy
from game_logic.player import Player
from game_logic.world import Area
from ai.fsm import IdleState, AttackingState, State # Import base State for type checks

class TestEnemyAndFSM(unittest.TestCase):
    def setUp(self):
        self.area = Area("Test Arena", "Arena for testing")
        # Suppress print output during player/enemy creation and actions in setup
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            self.player = Player("Test Player", starting_area=self.area, health=100, attack_power=10, defense=5)
            self.enemy = Enemy(name="Test Goblin", health=50, attack_power=8, defense=3, description="A test goblin")
            self.area.enemy = self.enemy 
            # self.enemy.current_state.enter(self.enemy) # Not strictly needed as enter methods are simple
        finally:
            sys.stdout.close()
            sys.stdout = original_stdout

    def test_enemy_creation(self):
        self.assertEqual(self.enemy.name, "Test Goblin")
        self.assertEqual(self.enemy.health, 50)
        self.assertEqual(self.enemy.max_health, 50)
        self.assertTrue(self.enemy.is_alive)
        self.assertIsInstance(self.enemy.current_state, IdleState)

    def test_enemy_take_damage(self):
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            initial_health = self.enemy.health
            self.enemy.take_damage(10)
            self.assertEqual(self.enemy.health, initial_health - 10)
            self.enemy.take_damage(100) # More than remaining
            self.assertEqual(self.enemy.health, 0)
            self.assertFalse(self.enemy.is_alive)
        finally:
            sys.stdout.close()
            sys.stdout = original_stdout

    def test_enemy_defend_reduces_damage(self):
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            self.enemy.defend() # Sets is_defending to True
            self.assertTrue(self.enemy.is_defending)
            initial_health = self.enemy.health
            damage_amount = 10
            self.enemy.take_damage(damage_amount)
            self.assertEqual(self.enemy.health, initial_health - (damage_amount // 2))
        finally:
            sys.stdout.close()
            sys.stdout = original_stdout

    def test_enemy_perform_attack_damages_player(self):
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            initial_player_health = self.player.health
            expected_damage = max(1, self.enemy.attack_power - self.player.defense)
            self.enemy.perform_attack(self.player)
            self.assertEqual(self.player.health, initial_player_health - expected_damage)
        finally:
            sys.stdout.close()
            sys.stdout = original_stdout

    def test_fsm_initial_state_is_idle(self):
        self.assertIsInstance(self.enemy.current_state, IdleState)

    def test_fsm_idle_to_attacking_transition_when_player_present(self):
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            # Player and enemy are in the same area in setUp
            self.enemy.act(self.player, self.area) 
            self.assertIsInstance(self.enemy.current_state, AttackingState)
        finally:
            sys.stdout.close()
            sys.stdout = original_stdout

    def test_fsm_attacking_state_performs_attack(self):
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            # Transition to AttackingState first
            self.enemy.act(self.player, self.area) 
            self.assertIsInstance(self.enemy.current_state, AttackingState)

            initial_player_health = self.player.health
            # Ensure enemy is healthy so it's more likely to attack
            self.enemy.health = self.enemy.max_health 
            # Reset is_defending in case a previous test set it and act didn't run fully
            self.enemy.is_defending = False 

            self.enemy.act(self.player, self.area) # Should call perform_attack via FSM
            self.assertTrue(self.player.health < initial_player_health)
            self.assertFalse(self.enemy.is_defending) # Should not have defended
        finally:
            sys.stdout.close()
            sys.stdout = original_stdout

    def test_fsm_attacking_state_can_choose_defend_when_low_health(self):
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            # Transition to AttackingState
            self.enemy.act(self.player, self.area) 
            self.assertIsInstance(self.enemy.current_state, AttackingState)

            self.enemy.health = self.enemy.max_health * 0.1 # Low health (10% of max)
            
            # Mock random.random to control the outcome for defend
            original_random_func = random.random
            random.random = lambda: 0.4 # Ensure the 0.5 threshold for defending is met
            
            self.enemy.act(self.player, self.area) # Enemy should choose to defend
            
            self.assertTrue(self.enemy.is_defending)
            
            random.random = original_random_func # Restore original random function
        finally:
            sys.stdout.close()
            sys.stdout = original_stdout

    def test_fsm_attacking_to_idle_transition_if_player_defeated(self):
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            # Ensure enemy is in AttackingState
            self.enemy.act(self.player, self.area) 
            self.assertIsInstance(self.enemy.current_state, AttackingState)

            self.player.take_damage(self.player.max_health * 2) # Defeat player
            self.assertFalse(self.player.is_alive)

            self.enemy.act(self.player, self.area) # Enemy's turn
            self.assertIsInstance(self.enemy.current_state, IdleState)
        finally:
            sys.stdout.close()
            sys.stdout = original_stdout
            
    def test_fsm_attacking_to_idle_transition_if_enemy_defeated(self):
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            # Ensure enemy is in AttackingState
            self.enemy.act(self.player, self.area)
            self.assertIsInstance(self.enemy.current_state, AttackingState)

            self.enemy.take_damage(self.enemy.max_health * 2) # Defeat enemy
            self.assertFalse(self.enemy.is_alive)
            
            # The FSM's AttackingState.execute already checks `if not agent.is_alive`.
            # We just need to call the execute method to see if it returns the new state.
            new_state_instance = self.enemy.current_state.execute(self.enemy, self.player, self.area)
            if new_state_instance and new_state_instance != self.enemy.current_state:
                # self.enemy.current_state.exit(self.enemy) # Not strictly necessary for this test if enter/exit are simple
                self.enemy.current_state = new_state_instance
                # self.enemy.current_state.enter(self.enemy)
            
            self.assertIsInstance(self.enemy.current_state, IdleState)
        finally:
            sys.stdout.close()
            sys.stdout = original_stdout

if __name__ == '__main__':
    unittest.main()
