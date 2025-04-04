import shlex
import asyncio
import sys
import cmd
import cowsay
import readline
import threading
from io import StringIO


weapon_damage = {
    'sword': 10,
    'spear': 15,
    'axe': 20
}

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
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.username = sys.argv[1]
        self.loc_loop = None
        self.loc_queue = None
        self.close_event = None

    def postcmd(self, stop, line):
        if self.close_event.is_set():
            return True
        return super().postcmd(stop, line)

    def send(self, msg):
        if self.loc_loop and self.loc_queue:
            self.loc_loop.call_soon_threadsafe(
                self.loc_queue.put_nowait,
                msg
            )
        else:
            exit(0)

    def do_up(self):
        self.move(0, -1)

    def do_down(self):
        self.move(0, 1)

    def do_left(self):
        self.move(-1, 0)

    def do_right(self):
        self.move(1, 0)

    async def move(self, dx, dy):
        self.send(f"move {dx} {dy}")


    def do_addmon(self, arg):
        monster_name, hello_word, hp, (x, y) = parse_addmon_args(arg)
        if (monster_name not in cowsay.list_cows()) and (monster_name not in custom_monsters):
            print('Cannot add unknown monster')
            return
        self.send(f"addmon {monster_name} {x} {y} {hp} {hello_word}")

    def complete_addmon(self, line, text):
        monsters = cowsay.list_cows() + list(custom_monsters.keys())
        if len(line.split()) < 3:
            return [name for name in monsters if name.startswith(text)]
        else:
            return [name for name in ['coords', 'hello', 'hp'] if name.startswith(text)]


    def do_attack(self, arg):
        monster_name, damage = parse_attack(arg)
        self.send(f"attack {monster_name} {damage}")

    def complete_attack(self, line, text):
        monsters = cowsay.list_cows() + list(custom_monsters.keys())
        if len(line.split(' ')) == 2:
            return [name for name in monsters if name.startswith(text)]
        elif len(line.split(' ')) == 3:
            return ['with']
        else:
            return [name for name in list(weapon_damage.keys()) if name.startswith(text)]

    def do_sayall(self, arg):
        if ' ' in arg:
            if arg.startswith('"') and arg.endswith('"'):
                self.send(f"sayall {arg.strip('" ')}")
            else: print("Invalid Input!")
        else:
            self.send(f'sayall {arg}')


async def local_srv(mud):
    try:
        receiver, sender = await asyncio.open_connection('localhost', 25565)
    except Exception:
        mud.close_event.set()
        print('Server is unavailable!')
        exit(0)

    sender.write(f'{sys.argv[1]}\n'.encode())
    resp = (await receiver.readline()).decode().strip()

    if resp == 'Username is already taken':
        mud.close_event.set()
        print('Username is already taken!')
        sender.close()
        await sender.wait_closed()
        exit(0)

    send_task = asyncio.create_task(mud.local_srv_queue.get())
    receive_task = asyncio.create_task(receiver.readline())

    try:
        while True:
            done, pending = await asyncio.wait(
                [send_task, receive_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in done:
                if task is send_task:
                    data = task.result()
                    sender.write(f"{data}\n".encode())
                    await sender.drain()
                    send_task = asyncio.create_task(mud.local_srv_queue.get())

                elif task is receive_task:
                    response = task.result().decode().strip()
                    if response == 'server is unavailable':
                        mud.close_event.set()
                        print('server is unavailable!')
                        raise Exception('server is unavailable')

                    print(f'\n{response.replace('\\n', '\n')}\n{mud.prompt}{readline.get_line_buffer()}', end='',
                          flush=True)
                    receive_task = asyncio.create_task(receiver.readline())

    except Exception as e:
        if e.args[0] != 'server is unavailable':
            print(e)
    finally:
        send_task.cancel()
        receive_task.cancel()
        sender.close()
        await sender.wait_closed()


def run_local_srv_in_thread(mud):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    mud.loc_queue = asyncio.Queue()
    mud.loc_loop = loop
    mud.close_event = threading.Event()

    loop.run_until_complete(local_srv(mud))


def main():
    if len(sys.argv) < 2:
        print("Enter username")
        return
    mud = MUD()
    threading.Thread(target=run_local_srv_in_thread, args=(mud,)).start()
    mud.cmdloop()


if __name__ == "__main__":
    main()
