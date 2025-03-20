import shlex
import asyncio
import cowsay
from io import StringIO
import cmd


custom_monsters = {
    "jgsbat" : cowsay.read_dot_cow(StringIO(r"""
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

}
weapon_damage = {
    'sword': 10,
    'spear': 15,
    'axe': 20
}


def encounter(monster_name, hello):
    if monster_name in cowsay.list_cows():
        print(cowsay.cowsay(hello, cow = monster_name))
    else:
        print(cowsay.cowsay(hello, cowfile=custom_monsters[monster_name]))


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


def parse_attack(args):
    args = shlex.split(args)
    if not (monster_name := args[0]):
        print("Invalid arguments")
        return

    if len(args) == 1:
        damage = weapon_damage['sword']
    elif args[1] == 'with':
        if args[2] not in weapon_damage:
            print("Unknown weapon!")
            return
        damage = weapon_damage[args[2]]

    return monster_name, damage


class MUD(cmd.Cmd):
    intro = '<<< Welcome to Python-MUD 0.1 >>>'
    prompt = 'MUD>> '

    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_event_loop()
        self.receiver = None
        self.sender = None

    def preloop(self):
        self.loop.run_until_complete(self.init_users())

    async def init_users(self):
        self.receiver, self.sender = await asyncio.open_connection('localhost', 25565)

    async def send(self, request):
        self.sender.write((request + '\n').encode())
        await self.sender.drain()
        reply = await self.receiver.readline()
        return reply.decode().strip()


    def do_up(self):
        self.loop.run_until_complete(self._move_player(0, -1))

    def do_down(self):
        self.loop.run_until_complete(self._move_player(0, 1))

    def do_left(self):
        self.loop.run_until_complete(self._move_player(-1, 0))

    def do_right(self):
        self.loop.run_until_complete(self._move_player(1, 0))

    async def _move(self, dx, dy):
        server_response = await self.send(f"move {dx} {dy}")
        x, y, *monster_data = shlex.split(server_response)
        print(f'Moved to ({x}, {y})')
        if monster_data:
            monster_name, *hello = monster_data
            hello = ' '.join(hello)
            encounter(monster_name, hello)


    def do_addmon(self, arg):
        monster_name, hello_word, hp, location = parse_addmon_args(arg)
        if (monster_name not in cowsay.list_cows()) and (monster_name not in custom_monsters):
            print('Cannot add unknown monster')
            return
        self.loop.run_until_complete(self._add_monster(monster_name, hello_word, hp, location))

    async def _add_monster(self, monster_name, hello, hp, location):
        server_response = await self.send(f"addmon {monster_name} {location[0]} {location[1]} {hp} {hello}")
        print(f'Added monster {monster_name} to ({location[0]}, {location[1]}) saying {hello}')
        if server_response == 'replaced':
            print('Replaced the old monster')

    def complete_addmon(self, line, text):
        monsters = cowsay.list_cows() + list(custom_monsters.keys())
        if len(line.split()) < 3:
            return [name for name in monsters if name.startswith(text)]
        else:
            return [name for name in ['coords', 'hello', 'hp'] if name.startswith(text)]


    def do_attack(self, arg):
        monster_name, damage = parse_attack(arg)
        self.loop.run_until_complete(self._attack(monster_name, damage))

    async def _attack(self, monster_name, damage):
        server_response = await self.send(f"attack {monster_name} {damage}")
        if server_response:
            damage, hp = server_response.split(' ', 1)
            print(f'Attacked {monster_name},  damage {damage} hp')
            if hp == '0':
                print(f'{monster_name} died')
            else:
                print(f'{monster_name} now has {hp}')
        else: print(f'No {monster_name} here')

    def complete_attack(self, line, text):
        monsters = cowsay.list_cows() + list(custom_monsters.keys())
        if len(line.split(' ')) == 2:
            return [name for name in monsters if name.startswith(text)]
        elif len(line.split(' ')) == 3:
            return ['with']
        else:
            return [name for name in list(weapon_damage.keys()) if name.startswith(text)]


def main():
    MUD().cmdloop()

if __name__ == "__main__":
    main()
