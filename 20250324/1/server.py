import asyncio


player_position = (0, 0)
game_map = [ (10 * [None]) for _ in range(10) ]


class Entity:
    def __init__(self, name, hello_word, hp):
        self.hello_word = hello_word
        self.name = name
        self.hp = hp


def move(dx, dy):
    global player_position
    player_position = ((player_position[0] + dx + 10) % 10, (player_position[1] + dy + 10) % 10)
    x, y = player_position
    response = f'{x} {y} '
    if game_map[y][x]:
        response += f'{game_map[y][x].name} {game_map[y][x].hello} '

    return response


def add_monster(name, x, y, hp, hello_word):
    if game_map[x][y]:
        return 'replaced'
    game_map[y][x] = Entity(name, hello_word, hp)
    return


def attack(monster_name, damage):
    x, y = player_position
    entity = game_map[y][x]

    if not entity or (entity.name != monster_name):
        return
    else:
        damage = min(damage, entity.hp)
        entity.hp -= damage
        if entity.hp == 0:
            game_map[y][x] = None
        return f'{damage} {entity.hp}'


async def proccess(receiver, sender):
    while args := await receiver.readline():
        args = args.decode().strip().split(' ')

        match args[0]:
            case "move":
                response = move(int(args[1]), int(args[2]))
            case "addmon":
                response = add_monster(args[1], int(args[2]), int(args[3]), int(args[4]), ' '.join(*args[5:]))
            case "attack":
                response = attack(args[1], int(args[2]))
            case _:
                continue

        sender.write((response + '\n').encode())
        await sender.drain()
    sender.close()


async def main():
    server = await asyncio.start_server(proccess, 'localhost', 25565)
    async with server:
        await server.serve_forever()

asyncio.run(main())
