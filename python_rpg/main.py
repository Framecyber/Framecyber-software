from game_logic.player import Player
from game_logic.world import STARTING_AREA

def game_loop():
    player_name = "Hero" # Or get from input
    player = Player(name=player_name, starting_area=STARTING_AREA)

    print(f"Welcome, {player.name}!")
    print("Type 'quit' to exit the game.")
    print("-" * 20)

    while True:
        # Check Player Status at Start of Turn
        if not player.is_alive:
            # Game over message is printed by player.take_damage
            # print("Game Over! You have been defeated.") 
            break

        # Player Action Phase
        player.current_area.describe()
        action = input("What do you do? (e.g., 'move east', 'attack', 'quit'): ").strip().lower()

        if action == "quit":
            print("Thanks for playing!")
            break
        elif action.startswith("move "):
            parts = action.split(" ", 1)
            if len(parts) > 1:
                direction = parts[1]
                player.move(direction)
            else:
                print("Move where? Try 'move <direction>'.")
        elif action == "attack":
            target_enemy = player.current_area.enemy
            player.attack(target_enemy)
            # Check if enemy was defeated by player's attack
            if target_enemy and not target_enemy.is_alive:
                # Optional: print f"{target_enemy.name} lies defeated." (already handled in take_damage)
                player.current_area.enemy = None # Remove defeated enemy from area
        elif action == "help":
            print("\nAvailable commands:")
            print("  move <direction> - Change your location (e.g., 'move north').")
            print("  attack           - Attack the enemy in your current area.")
            print("  look             - Describe your current surroundings again.")
            print("  help             - Show this help message.")
            print("  quit             - Exit the game.\n")
        elif action == "look":
            player.current_area.describe()
            current_enemy = player.current_area.enemy
            if current_enemy and current_enemy.is_alive:
                print(f"You also see {current_enemy.name} ({current_enemy.health}/{current_enemy.max_health} HP) here.")
            else:
                print("The area is quiet.")
        else:
            print("Invalid command. Type 'help' to see available commands.")
        
        print() # Spacing

        # Enemy Action Phase (if player is still alive and an enemy is present)
        # Check player status again in case a future action (like a trap) could defeat them
        if not player.is_alive: # Player might have lost during their action if we add traps etc.
             # Game over message already printed by take_damage
             break

        current_enemy = player.current_area.enemy
        if current_enemy and current_enemy.is_alive and player.is_alive:
            print(f"--- {current_enemy.name}'s turn ---")
            current_enemy.act(player, player.current_area) # Pass current_area
            # Check if player was defeated by enemy's attack
            if not player.is_alive:
                # Game over message is printed by player.take_damage
                break
        
        print() # Spacing after enemy turn or if no enemy action

if __name__ == "__main__":
    game_loop()
