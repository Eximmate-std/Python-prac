import shlex
import cowsay
from io import StringIO
import cmd

from werkzeug.datastructures import Range

player_position = (0, 0)
game_map = [ (10 * [None]) for _ in range(10) ]
custom_monsters = dict()
weapon_damage = {
    'sword': 10,
    'spear': 15,
    'axe': 20
}

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
    if (name not in cowsay.list_cows()) and (name not in custom_monsters):
        print('Cannot add unknown monster')
        return

    x, y = location
    print(f'Added monster {name} to ({x}, {y}) saying {hello_word} with {hp} hp')

    if game_map[x][y]:
        print('Replaced the old monster')

    game_map[y][x] = Entity(name, hello_word, hp)


def parse_addmon_args(args):
    try:
        args = shlex.split(args.strip())

        if len(args) != 8:
            raise ValueError

        monster_name = args[0]
        params = args[1:]

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
                raise ValueError

        if None in (hello_word, hp, location):
            raise ValueError

    except Exception as e:
        print('Invalid arguments')

    return monster_name, hello_word, hp, location


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


def attack(weapon='sword'):
    x, y = player_position
    entity = game_map[y][x]

    if not entity:
        print("No monster here")
        return

    damage = min(weapon_damage[weapon], entity.hp)
    entity.hp -= damage
    print(f"Attacked {entity.name} with {weapon}, damage {damage} hp")

    if entity.hp <= 0:
        print(f"{entity.name} died")
        game_map[y][x] = None
    else:
        print(f"{entity.name} now has {entity.hp}")


def parse_attack(args):
    args = shlex.split(args)
    weapon = 'sword'

    if len(args) == 0:
        pass
    elif len(args) == 2 and args[0] == 'with':
        if args[1] in weapon_damage:
            weapon = args[1]
        else:
            raise ValueError("Unknown weapon")
    else:
        raise ValueError("Invalid command syntax. Use: attack [with <weapon>]")
    return weapon


class MUD(cmd.Cmd):
    intro = '<<< Welcome to Python-MUD 0.1 >>>'
    prompt = 'MUD>> '

    def do_up(self, args):
        move((0, -1))

    def do_down(self, args):
        move((0, 1))

    def do_left(self, args):
        move((-1, 0))

    def do_right(self, args):
        move((1, 0))


    def do_addmon(self, arg):
        monster_name, hello_word, hp, location = parse_addmon_args(arg)
        add_monster(monster_name, hello_word, hp, location)

    def complete_addmon(self, line, text):
        monsters = cowsay.list_cows() + list(custom_monsters.keys())
        if len(line.split()) < 3:
            return [name for name in monsters if name.startswith(text)]
        else:
            return [name for name in ['coords', 'hello', 'hp'] if name.startswith(text)]


    def do_attack(self, arg):
        attack(parse_attack(arg))

    def complete_attack(self, line, text):
        monsters = cowsay.list_cows() + list(custom_monsters.keys())
        if len(line.split(' ')) == 2:
            return [name for name in monsters if name.startswith(text)]
        elif len(line.split(' ')) == 3:
            return ['with']
        else:
            return [name for name in list(weapon_damage.keys()) if name.startswith(text)]


def main():
    add_custom_monsters()
    MUD().cmdloop()


if __name__ == "__main__":
    main()
