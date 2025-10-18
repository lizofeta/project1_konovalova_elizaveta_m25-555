from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room

def show_inventory(game_state : dict):
    player_inventory = game_state.get('player_inventory')
    if not isinstance(player_inventory, list):
        raise TypeError('Ожидался список в качестве инвентаря.')
    if not all(isinstance(item, str) for item in player_inventory):
        raise TypeError('Все элементы списка инвентаря должны быть строками.')
    if player_inventory:
        print(f'Инвентарь: {', '.join(player_inventory)}') # мб заменим на ретурн (посмотрим позже)
    else: 
        print('Инвентарь пуст.') # тут тоже

def get_input(prompt="> "):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print('\nВыход из игры')
        return 'quit'

def move_player(game_state, direction):
    if not isinstance(direction, str):
        print('Ошибка: направление должно быть текстом (например: north)')
    current_room = game_state.get('current_room')
    if direction in ROOMS[current_room]['exits'].keys():
        game_state['current_room'] = ROOMS[current_room]['exits'].get(direction) 
        game_state['steps_taken'] += 1
        describe_current_room(game_state)
    else: 
        print('Нельзя пройти в этом направлении.')