import math
from labyrinth_game.constants import ROOMS


def describe_current_room(game_state : dict):

    if not isinstance(game_state, dict):
        raise TypeError('Параметр game_state должен быть словарем (dict)')

    current_room = game_state.get('current_room')
    if current_room is None:
        print('Ошибка! Не указана текущая комната')
    print(f'== {current_room.upper()} ==')
    print(f'Описание комнаты: {ROOMS[current_room].get('description')}')
    items = ROOMS[current_room].get('items')
    if items:
        print(f'Заметные предметы: {', '.join(ROOMS[current_room].get('items'))}') 
    print('Выходы: ')
    # Игрок будет видеть только направления, но не названия комнат
    for direction in ROOMS[current_room].get('exits', {}).keys():
        print(f'{direction}')
    puzzle = ROOMS[current_room].get('puzzle')
    if puzzle:
        print('Кажется, здесь есть загадка (используйте команду solve)')

def solve_puzzle(game_state):
    puzzle = ROOMS[game_state['current_room']]['puzzle']
    if puzzle:
        print(puzzle[0])
        answer = input("Ваш ответ: ")
        if answer == puzzle[1]:
            print("Успех! Загадка разгадана.")
            ROOMS[game_state['current_room']]['puzzle'] = None
            game_state['score'] += 1
        else: 
            print('Неверно. Попробуйте снова.')
    else: 
        print("Загадок здесь нет.")

def victory(game_state):
    print('В сундуке сокровище! Вы победили!')
    ROOMS[game_state['current_room']]['items'].remove('treasure_chest')
    game_state['game_over'] = True 


def attempt_open_treasure(game_state):
    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ и замок щёлкает! Сундук открыт!")
        victory(game_state)
    else: 
        open_attempt = input("Сундук заперт. Попробуем ввести код? (да/нет)")
        open_attempt = open_attempt.lower().strip()
        if open_attempt == 'да':
            puzzle = ROOMS[game_state['current_room']]['puzzle']
            print(puzzle[0])
            code = input("Ваш ответ: ")
            if code == puzzle[1]:
                print("Успех! Ваш код подошел, вы открыли сундук!")
                victory(game_state)
            else: 
                print("Ошибка! Код неверный.")
        else:
            print("Вы отступаете от сундука")

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение") 

def pseudo_random(seed, modulo):
    if not isinstance(seed, int) or not isinstance(modulo, int):
        raise TypeError("Параметры должны быть целыми числами.")
    random = math.sin(seed * 12.9898) * 43758.5453 
    random = abs(random - math.floor(random)) * modulo 
    return int(random)

def trigger_trap(game_state):
    print('Ловушка активирована! Пол стал дрожать...')
    if game_state['player_inventory']:
        item_index = pseudo_random(game_state['steps_taken'], len(game_state['player_inventory']))
        lost_item = game_state['player_inventory'].pop(item_index)
        print(f'Вы потеряли {lost_item}')
    else: 
        damage = pseudo_random(0, 9)
        if damage < 3:
            print("Вы получили травмы несовместимые с жизнью. Игра окончена.")
            game_state['game_over'] = True 
        else: 
            print("Вам повезло! Отделались царапинами.")

def random_event(game_state):
    prob = pseudo_random(game_state['steps_taken'], 10)
    if prob == 0:
        event = pseudo_random(game_state['steps_taken'] + 1, 3)
        match event:
            case 0:
                # Находка 
                print("Вы нашли монетку!")
                game_state['player_inventory'].append('coin')
            case 1:
                # Испуг
                print("Здесь кто-то есть! Слышен какой-то шорох...")
                if 'sword' in game_state['player_inventory']:
                    print("Ваш меч отпугнул существо")
            case 2:
                # Ловушка 
                if game_state['current_room'] == 'trap_room' and 'torch' not in game_state['player_inventory']:
                    print("Опасность!")
                    trigger_trap(game_state)