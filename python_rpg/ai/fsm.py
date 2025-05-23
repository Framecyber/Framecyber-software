import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..game_logic.enemy import Enemy
    from ..game_logic.player import Player

class State:
    def __init__(self):
        pass

    def enter(self, agent):
        # Optional: print(f"{agent.name} enters {self.__class__.__name__}")
        pass

    def execute(self, agent: 'Enemy', player_context: 'Player', current_area_enemy_is_in: Any):
        raise NotImplementedError

    def exit(self, agent: 'Enemy'):
        # Optional: print(f"{agent.name} exits {self.__class__.__name__}")
        pass

class IdleState(State):
    def execute(self, agent: 'Enemy', player_context: 'Player', current_area_enemy_is_in: Any):
        # Agent is current_enemy, player_context is player
        # current_area_enemy_is_in is player_context.current_area (since enemy is in player's area to be active)
        if player_context.is_alive and agent.is_alive: # Check if player is in the same area is implicit
            print(f"{agent.name} (in IdleState) spots {player_context.name}!")
            from .fsm import AttackingState # Local import to avoid circularity at module level if states import each other
            return AttackingState()
        return None # No state change

class AttackingState(State):
    def execute(self, agent: 'Enemy', player_context: 'Player', current_area_enemy_is_in: Any):
        # TYPE_CHECKING imports for Enemy and Player are at the top of the file
        # from ..game_logic.player import Player # Not needed here if using string hint

        if not player_context.is_alive or not agent.is_alive:
            print(f"{agent.name} (in AttackingState): Target or self not alive. Returning to Idle.")
            from .fsm import IdleState # Local import
            return IdleState()

        # Decision: Attack or Defend
        # Defend if health is less than 30% of max_health, 50% chance
        if agent.health < (agent.max_health * 0.3) and random.random() < 0.5:
            agent.defend()
        else:
            # If not defending, then attack
            agent.perform_attack(player_context)
        
        return None # Stay in AttackingState, action chosen was either defend or attack
