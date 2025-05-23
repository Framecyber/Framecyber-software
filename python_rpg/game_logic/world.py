from .enemy import Enemy

class Area:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.exits = {}  # e.g., {"north": another_area_object}
        self.enemy: Enemy | None = None

    def describe(self):
        """Prints the area's name and description and available exits."""
        print(f"\n--- {self.name} ---")
        print(self.description)
        if self.exits:
            available_exits = ", ".join(self.exits.keys())
            print(f"Exits: {available_exits}")
        else:
            print("There are no obvious exits.")

        if self.enemy and self.enemy.is_alive:
            print(f"You see a {self.enemy.name} here! {self.enemy.description}")

# Create sample Area objects
forest_clearing = Area("Forest Clearing", "You are in a sun-dappled clearing. Birds are singing.")
cave_entrance = Area("Cave Entrance", "A dark, ominous cave entrance looms before you to the east.")
dark_cave = Area("Dark Cave", "It is pitch black. You hear dripping water.")

# Link areas together
forest_clearing.exits['east'] = cave_entrance
cave_entrance.exits['west'] = forest_clearing
cave_entrance.exits['east'] = dark_cave
dark_cave.exits['west'] = cave_entrance

# Create an enemy
goblin = Enemy(name="Goblin Grunt", health=30, attack_power=8, defense=2, description="A small, aggressive goblin wielding a rusty dagger.")
dark_cave.enemy = goblin

# Export the starting area
STARTING_AREA = forest_clearing

if __name__ == '__main__':
    # Example usage:
    current_area = STARTING_AREA
    current_area.describe()

    if 'east' in current_area.exits:
        current_area = current_area.exits['east']
        current_area.describe()

    if 'east' in current_area.exits:
        current_area = current_area.exits['east']
        current_area.describe()

    if 'west' in current_area.exits:
        current_area = current_area.exits['west']
        current_area.describe()
