import asyncio
from io import StringIO
import shlex
import cowsay


players = {}
game_map = [ (10 * [None]) for _ in range(10) ]
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


class Entity:
    def __init__(self, name, hello_word, hp):
        self.hello_word = hello_word
        self.name = name
        self.hp = hp


class Player:
    def __init__(self, queue):
        self.pos = (0, 0)
        self.queue = queue


def encounter(monster_name, hello):
    if monster_name in cowsay.list_cows():
        return cowsay.cowsay(hello, cow = monster_name)
    else:
        return cowsay.cowsay(hello, cowfile=custom_monsters[monster_name])


def move(player_name, dx, dy):
    x, y = players[player_name].pos
    x, y = ((x + dx) % 10, (y + dy) % 10)
    response = f'Moved to ({x}, {y})'
    if game_map[y][x]:
        response += f'\n{encounter(game_map[y][x].name, game_map[y][x].hello)} '
    return response


def add_monster(player_name, monster_name, x, y, hp, hello_word):
    broadcast = (f'{player_name} added monster' +
                       f'{monster_name} saying {hello_word} with {hp} hp')
    response = (f'Added monster {monster_name} to' +
                f' ({x}, {y}) saying {hello_word} with {hp} hp')
    if game_map[x][y]:
        replace = '\nReplaced the old monster'
        broadcast += replace
        response += replace
    game_map[y][x] = Entity(monster_name, hello_word, hp)
    return response, broadcast


def attack(player_name, monster_name, damage):
    x, y = players[player_name].pos
    entity = game_map[y][x]
    broadcast = ""
    response = ""

    if (not entity) or (entity.name != monster_name):
        response = f'No {monster_name} here'
    else:
        damage = min(damage, entity.hp)
        entity.hp -= damage
        attack_msg = f'attacked {monster_name},  damage {damage} hp'
        broadcast = f'{player_name} ' + attack_msg
        response += attack_msg
        if entity.hp == 0:
            game_map[y][x] = None
            dead_msg = f'\n{monster_name} died'
            response += dead_msg
            broadcast += dead_msg
        else:
            mon_hp_msg = f'\n{monster_name} now has {entity.hp}'
            response += mon_hp_msg
            broadcast += mon_hp_msg

    return response, broadcast


async def proccess(receiver, sender):
    try:
        username = (await receiver.readline()).decode().strip()
        if username in players:
            sender.write(b'Username is already taken\n')
            await sender.drain()
            sender.close()
            return

        sender.write(b'Connection successful\n')
        await sender.drain()
        players[username] = Player(asyncio.Queue())

        broadcast_msg = f'{username} connected.'
        for player_name in players:
            if player_name != username:
                await players[player_name].queue.put(broadcast_msg)

        read_task = asyncio.create_task(receiver.readline())
        queue_task = asyncio.create_task(players[username].queue.get())

        while not receiver.at_eof():
            done, pending = await asyncio.wait(
                [read_task, queue_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in done:
                if task is read_task:
                    args = task.result().decode().strip()
                    if not args:
                        continue

                    args = shlex.split(args)
                    broadcast = ""

                    match args[0]:
                        case 'move':
                            dx, dy = map(int, args[1:3])
                            response = move(username, dx, dy)

                        case 'addmon':
                            name = args[1]
                            x = int(args[2])
                            y = int(args[3])
                            hp = int(args[4])
                            hello = ' '.join(args[5:])
                            response, broadcast = add_monster(username, name, x, y, hp, hello)

                        case 'attack':
                            name = args[1]
                            damage = int(args[2])
                            response, broadcast = attack(username, name, damage)

                        case _:
                            response = 'Invalid command'

                    if broadcast:
                        for player_name in players:
                            if player_name != username:
                                await players[player_name].queue.put(broadcast)
                            else:
                                await players[player_name].queue.put((response.replace('\n', '\\n') + '\n').encode())

                    read_task = asyncio.create_task(receiver.readline())

                elif task is queue_task:
                    sender.write((task.result().replace('\n', '\\n') + '\n').encode())
                    await sender.drain()
                    queue_task = asyncio.create_task(players[username].queue.get())

    finally:
        if username in players:
            del players[username]
            broadcast_msg = f'{username} disconnected.'
            for player_name in players:
                await players[player_name].queue.put(broadcast_msg)

        sender.write(b'server is unavailable\n')
        await sender.drain()
        sender.close()


async def main():
    server = await asyncio.start_server(proccess, 'localhost', 25565)
    async with server:
        await server.serve_forever()

asyncio.run(main())
