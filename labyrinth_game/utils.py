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
    for direction, exit in ROOMS[current_room].get('exits', {}).items():
        print(f'{direction}: {exit}')
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