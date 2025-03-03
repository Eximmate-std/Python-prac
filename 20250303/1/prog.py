import sys
import cowsay

player_position = (0, 0)
game_map = [ (10 * [None]) for _ in range(10) ]

class Entity:
    def __init__(self, name, hello_word):
        self.hello_word = hello_word
        self.name = name


def move(direction):
    global player_position
    player_position = ((player_position[0] + direction[0] + 10) % 10, (player_position[1] + direction[1] + 10) % 10)
    print(f'Moved to ({player_position[0]}, {player_position[1]})')

    if game_map[player_position[1]][player_position[0]]:
        encounter()

    return player_position


def add_monster(name, location, hello_word):
    if name not in cowsay.list_cows():
        print('Cannot add unknown monster')
        return

    print(f'Added monster {name} to ({location[0]}, {location[1]}) saying {hello_word}')

    if game_map[player_position[1]][player_position[0]]:
        print('Replaced the old monster')

    game_map[location[1]][location[0]] = Entity(name, hello_word)


def encounter():
    print(cowsay.cowsay(game_map[player_position[1]][player_position[0]].hello_word,
                        cow = game_map[player_position[1]][player_position[0]].name))


def main():
    print('<<< Welcome to Python-MUD 0.1 >>>')
    for user_input in sys.stdin:
        if not user_input.strip:
            continue

        args = user_input.strip().split()
        command = args[0]

        try:
             match command:
                case("up"):
                    move((0, -1))
                case("down"):
                    move((0, 1))
                case("right"):
                    move((1, 0))
                case("left"):
                    move((-1, 0))
                case("addmon"):
                    if len(args) != 5:
                        raise ValueError
                    add_monster(args[1], (int(args[2]), int(args[3])), args[4])
                case _:
                    print("Invalid command")
        except Exception as e:
            print('Invalid arguments')
            print(e)


if __name__ == "__main__":
    main()
