from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .player import Player
    from ..ai.fsm import State # For self.current_state type hint

from ..ai.fsm import IdleState

class Enemy:
    def __init__(self, name: str, health: int, attack_power: int, defense: int, description: str = ""):
        self.name = name
        self.health = health
        self.max_health = health  # Store original health
        self.attack_power = attack_power
        self.defense = defense
        self.description = description
        self.is_defending: bool = False # Added is_defending
        self.current_state: 'State' = IdleState()
        # self.current_state.enter(self) # Call enter when state is first set

    def defend(self) -> None:
        self.is_defending = True
        print(f"{self.name} takes a defensive stance!")

    def take_damage(self, amount: int):
        actual_damage = amount
        if self.is_defending:
            actual_damage = amount // 2
            print(f"{self.name} is defending! Damage reduced by half to {actual_damage}.")
        
        self.health -= actual_damage
        self.health = max(0, self.health)
        # Message adjusted to show actual_damage
        print(f"{self.name} takes {actual_damage} damage. Current health: {self.health}/{self.max_health}")
        if not self.is_alive:
            print(f"{self.name} has been defeated!")

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def perform_attack(self, player_context: 'Player'):
        damage = max(1, self.attack_power - player_context.defense)
        print(f"{self.name} (FSM) attacks {player_context.name} for {damage} damage!")
        player_context.take_damage(damage)

    def act(self, player_context: 'Player', current_area_enemy_is_in: Any) -> None:
        self.is_defending = False # Reset defense status each turn
        # current_area_enemy_is_in is player_context.current_area, passed from main
        if not self.is_alive: 
            return
        
        # The 'current_area_enemy_is_in' might be useful if states need to know area details
        # but for now, the logic in states implicitly handles player presence.
        new_state_instance = self.current_state.execute(self, player_context, current_area_enemy_is_in)
        if new_state_instance and new_state_instance != self.current_state:
            self.current_state.exit(self)
            self.current_state = new_state_instance
            self.current_state.enter(self)
