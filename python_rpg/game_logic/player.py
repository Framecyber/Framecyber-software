from typing import TYPE_CHECKING
from .world import Area

if TYPE_CHECKING:
    from .enemy import Enemy

class Player:
    def __init__(self, name: str, starting_area: Area, health: int = 100, attack_power: int = 10, defense: int = 5):
        self.name = name
        self.health = health
        self.max_health = health # Added max_health
        self.attack_power = attack_power
        self.defense = defense
        self.current_area = starting_area

    def move(self, direction: str):
        """Moves the player to a new area if the direction is valid."""
        if direction in self.current_area.exits:
            self.current_area = self.current_area.exits[direction]
            print(f"You move {direction} to {self.current_area.name}.")
        else:
            print(f"You can't go {direction}.")

    def attack(self, target: 'Enemy' | None): # Changed type hint
        """Player attacks a target enemy."""
        if target and target.is_alive:
            damage = max(1, self.attack_power - target.defense)
            print(f"You attack {target.name} with your weapon!")
            target.take_damage(damage)
        elif target and not target.is_alive:
            print(f"{target.name} is already defeated.")
        else:
            print("There is nothing to attack here.")

    def take_damage(self, amount: int):
        self.health -= amount
        self.health = max(0, self.health)
        print(f"You take {amount} damage. Your health: {self.health}/{self.max_health}")
        if not self.is_alive:
            print("You have been defeated! Game Over.")

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def defend(self):
        """Placeholder for player defending."""
        print(f"{self.name} defends")
