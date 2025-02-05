import shlex
import sys
import cowsay
from io import StringIO


player_position = (0, 0)
game_map = [ (10 * [None]) for _ in range(10) ]
custom_monsters = dict()


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


def add_monster(name, hello_word, hp, location, ):
    if (name not in cowsay.list_cows()) and (name not in custom_monsters):
        print('Cannot add unknown monster')
        return

    x, y = location
    print(f'Added monster {name} to ({x}, {y}) saying {hello_word} with {hp} hp')

    if game_map[x][y]:
        print('Replaced the old monster')

    game_map[y][x] = Entity(name, hello_word, hp)


def encounter():
    entity = game_map[player_position[1]][player_position[0]]

    if entity.name in cowsay.list_cows():
        print(cowsay.cowsay(entity.hello_word, cow = entity.name))
    else:
        print(cowsay.cowsay(entity.hello_word,
                            cowfile=custom_monsters[entity.name]))


def add_custom_monsters():
    custom_monsters["jgsbat"] = cowsay.read_dot_cow(StringIO(r"""
    $the_cow = <<EOC;
             $thoughts
              $thoughts
        ,_                    _,
        ) '-._  ,_    _,  _.-' (
        )  _.-'.|\\\\--//|.'-._  (
         )'   .'\\/o\\/o\\/'.   `(
          ) .' . \\====/ . '. (
           )  / <<    >> \\  (
            '-._/``  ``\\_.-'
      jgs     __\\\\'--'//__
             (((""`  `"")))
    EOC
    """))



def main():
    add_custom_monsters()

    print('<<< Welcome to Python-MUD 0.1 >>>')
    for user_input in sys.stdin:
        if not user_input.strip:
            continue

        try:
            args = shlex.split(user_input.strip())
            command = args[0]

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
                    if len(args) != 9:
                        raise ValueError

                    monster_name = args[1]
                    params = args[2:]

                    hello_word = None
                    hp = None
                    location = None
                    i = 0

                    while i < len(params):
                        if params[i] == 'hello':
                            hello_word = params[i + 1]
                            i += 2
                        elif params[i] == 'hp':
                            hp = int(params[i + 1])
                            i += 2
                        elif params[i] == 'coords':
                            location = (int(params[i + 1]), int(params[i + 2]))
                            i += 3
                        else:
                            raise ValueError("Unknown parameter")

                    if None in (hello_word, hp, location):
                        raise ValueError("Missing required parameters")

                    add_monster(monster_name, hello_word, hp, location)

                case _:
                    print("Invalid command")

        except Exception as e:
            print('Invalid arguments')


if __name__ == "__main__":
    main()
