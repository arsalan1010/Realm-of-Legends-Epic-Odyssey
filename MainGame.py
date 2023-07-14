import random

class Character:
    def __init__(self, name, health, attack_damage):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_damage = attack_damage
    
    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def attack(self, target):
        damage = random.randint(self.attack_damage // 2, self.attack_damage)
        target.take_damage(damage)
        print(f"{self.name} attacks {target.name} for {damage} damage!")

class Player(Character):
    def __init__(self, name, health, attack_damage):
        super().__init__(name, health, attack_damage)
        self.experience = 0
        self.level = 1
        self.has_special_power = False
        self.inventory = {"Health Potion": 3}
        self.super_attack_available = True

    def level_up(self):
        self.level += 1
        self.attack_damage += 2
        self.max_health += 10
        self.health = self.max_health
        self.super_attack_available = True
        print("Level up! You are now level", self.level)

    def super_attack(self, enemy):
        if self.super_attack_available:
            damage = random.randint(self.attack_damage * 2, self.attack_damage * 3)
            enemy.take_damage(damage)
            print(f"{self.name} performs a super attack on {enemy.name} for {damage} damage!")
            self.super_attack_available = False
        else:
            print("You have already used your super attack in this battle.")

class Enemy(Character):
    def __init__(self, name, health, attack_damage):
        super().__init__(name, health, attack_damage)

    def drop_loot(self):
        loot = random.choice(["Health Potion", "Mana Potion", "Gold"])
        print(f"{self.name} dropped {loot}!")

class Boss(Enemy):
    def __init__(self, name, health, attack_damage):
        super().__init__(name, health, attack_damage)

    def drop_loot(self):
        loot = random.choice(["Health Potion", "Mana Potion", "Gold", "Special Power"])
        print(f"{self.name} dropped {loot}!")

def battle(player, enemy):
    print(f"A wild {enemy.name} appears!")
    while player.is_alive() and enemy.is_alive():
        print(f"\n{player.name} (Level {player.level}) - Health: {player.health}/{player.max_health}")
        print(f"{enemy.name} - Health: {enemy.health}/{enemy.max_health}")
        print("What will you do?")
        print("1. Attack")
        print("2. Use Health Potion")
        print("3. Super Attack")
        print("4. Run")
        action = input("Enter your choice (1-4): ")
        if action == "1":
            player.attack(enemy)
            if enemy.is_alive():
                enemy.attack(player)
        elif action == "2":
            if "Health Potion" in player.inventory:
                if player.health == player.max_health:
                    print("You are already at full health.")
                else:
                    player.heal(25)
                    player.inventory["Health Potion"] -= 1
                    print(f"{player.name} used a Health Potion. Health restored by 25.")
            else:
                print("You don't have any Health Potions.")
        elif action == "3":
            player.super_attack(enemy)
            if enemy.is_alive():
                enemy.attack(player)
        elif action == "4":
            print("You managed to escape.")
            return False
        else:
            print("Invalid input. Try again.")
    if player.is_alive():
        print(f"\nYou defeated {enemy.name}!")
        player.experience += 10
        if player.experience >= 100:
            player.level_up()
        enemy.drop_loot()
        if enemy.name == "Mutilator" and "Special Power" in player.inventory:
            print("You used the Special Power and defeated Mutilator!")
            return True
        return True
    else:
        print("You were defeated!")
        return False

def main():
    player_name = input("Enter your name: ")
    player = Player(player_name, health=100, attack_damage=10)

    # Create enemies
    goblin = Enemy("Goblin", health=100, attack_damage=7)
    orc = Enemy("Orc", health=100, attack_damage=9)
    dragon = Boss("Dragon", health=150, attack_damage=12)
    mutilator = Boss("Mutilator", health=200, attack_damage=20)

    enemies = [goblin, orc]
    bosses = [dragon, mutilator]

    print("Welcome to the Text-Based RPG!")
    print(f"Let the battle begin, {player.name}!")

    while player.is_alive():
        enemy = random.choice(enemies)
        result = battle(player, enemy)
        if not result:
            break
        if player.level >= 5 and enemy.name in ["Goblin", "Orc"]:
            enemy = random.choice(bosses)
            result = battle(player, enemy)
            if not result:
                break
            player.level += 2
            if player.level >= 10 and enemy.name == "Mutilator":
                print("Congratulations! You have defeated the Mutilator and won the game!")
                break
        else:
            player.level += 1
            if player.level % 3 == 0:
                print("Level up! You have gained an additional Health Potion.")
                player.inventory["Health Potion"] += 1
            if player.level >= 5:
                print("You have reached level 5! Powerful enemies now await you.")

    print("Game Over!")

if __name__ == "__main__":
    main()
