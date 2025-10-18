from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import get_input

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
        print(f'Кажется, здесь есть загадка (используйте команду solve)')

def solve_puzzle(game_state):
    puzzle = ROOMS[game_state['current_room']]['puzzle']
    if puzzle:
        print(puzzle[0])
        answer = get_input("Ваш ответ: ")
        if answer == puzzle[1]:
            print("Успех! Загадка разгадана.")
            ROOMS[game_state['current_room']]['puzzle'] = None
            game_state['score'] += 1
        else: 
            print('Неверно. Попробуйте снова.')
    else: 
        print("Загадок здесь нет.")