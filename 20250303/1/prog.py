import sys
import cowsay

player_position = (0, 0)
game_map = [ (10 * [None]) for _ in range(10) ]

class Entity:
    def __init__(self, name, hello_word, hp):
        self.hello_word = hello_word
        self.name = name
        self.hp = hp


def move(direction):
    global player_position
    player_position = ((player_position[0] + direction[0] + 10) % 10,
                       (player_position[1] + direction[1] + 10) % 10)
    print(f'Moved to ({player_position[0]}, {player_position[1]})')
    if game_map[player_position[1]][player_position[0]]:
        encounter()
    return player_position


def add_monster(name, hello_word, hp, location):
    if name not in cowsay.list_cows():
        print('Cannot add unknown monster')
        return

    x, y = location
    print(f'Added monster {name} to ({x}, {y}) saying {hello_word}')

    if game_map[x][y]:
        print('Replaced the old monster')

    game_map[y][x] = Entity(name, hello_word, hp)


def encounter():
    entity = game_map[player_position[1]][player_position[0]]
    print(cowsay.cowsay(entity.hello_word, cow = entity.name))


def main():
    for user_input in sys.stdin:
        if not user_input.strip:
            continue

        args = user_input.strip().split()
        command = args[0]

        try:
             match command:
                case "up":
                    move((0, -1))
                case "down":
                    move((0, 1))
                case "right":
                    move((1, 0))
                case "left":
                    move((-1, 0))
                case "addmon":
                    if len(args) != 5:
                        raise ValueError
                    add_monster(args[1], args[4], 100, (int(args[2]), int(args[3])))
                case _:
                    print("Invalid command")
        except Exception as e:
            print('Invalid arguments')


if __name__ == "__main__":
    main()
