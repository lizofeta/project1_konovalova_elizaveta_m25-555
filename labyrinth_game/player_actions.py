from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room

def show_inventory(game_state : dict):
    player_inventory = game_state.get('player_inventory')
    if not isinstance(player_inventory, list):
        raise TypeError('Ожидался список в качестве инвентаря.')
    if not all(isinstance(item, str) for item in player_inventory):
        raise TypeError('Все элементы списка инвентаря должны быть строками.')
    if player_inventory:
        print(f'Инвентарь: {', '.join(player_inventory)}') 
    else: 
        print('Инвентарь пуст.') 

def get_input(prompt="> "):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print('\nВыход из игры')
        return 'quit'

def move_player(game_state, direction):
    if not isinstance(direction, str):
        raise TypeError('Ошибка: направление должно быть текстом (например: north)')
    current_room = game_state.get('current_room')
    if direction in ROOMS[current_room]['exits'].keys():
        game_state['current_room'] = ROOMS[current_room]['exits'].get(direction) 
        game_state['steps_taken'] += 1
        describe_current_room(game_state)
    else: 
        print('Нельзя пройти в этом направлении.')
    
def take_item(game_state, item_name):
    if not isinstance(item_name, str):
        raise TypeError('Название предмета должно быть текстом (например: apple)')
    if item_name in ROOMS[game_state['current_room']]['items']:
        if item_name == 'treasure_chest':
            print("Вы не можете поднять сундук, он слишком тяжелый.")
        else: 
            game_state['player_inventory'].append(item_name)
            ROOMS[game_state['current_room']]['items'].remove(item_name)
            print(f'Вы подняли: {item_name}') 
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    if not isinstance(item_name, str):
        raise TypeError('Название предмета должно быть текстом (например:)')
    if item_name in game_state['player_inventory']:
        match item_name:
            case 'torch':
                print('Теперь хоть что-то видно..')
            case 'sword':
                print('Кто с мечом подойдет, от меча и погибнет!')
            case 'bronze_box':
                print('Вы открыли шкатулку')
                if 'rusty_key' not in game_state['player_inventory']:
                    game_state['player_inventory'].append('rusty_key')
            case _:
                print('Вы не знаете, как можете этим воспользоваться')
    else: 
        print('У вас нет такого предмета.')