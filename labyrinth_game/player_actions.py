from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def show_inventory(game_state : dict):
    """
    Функция отображает инвентарь игрока, если он не пуст. 
    Если инвентарь пуст, выводится соответствующее сообщение.
    """
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
    """
    Функция запрашивает ввод у пользователя. 
    При нажатии клавиш "Ctrl + С" заканчивает игру.
    """
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print('\nВыход из игры')
        return 'quit'

def change_room(game_state, new_room):
    """
    Вспомогательная функция для перехода между комнатами.
    """
    game_state['current_room'] = new_room
    game_state['steps_taken'] += 1
    describe_current_room(game_state)
    random_event(game_state)

def move_player(game_state, direction):
    """
    Функция передвижения.
    Перемещает игрока в соответствии с указанным им направлении, 
        если такой проход доступен.
    Если игрок переходит в комнату сокровищ, проверяет наличие ключа:
    Если ключа нет, игрок в комнату не проходит. 
    """
    if not isinstance(direction, str):
        raise TypeError('Ошибка: направление должно быть текстом (например: north)')
    current_room = game_state.get('current_room')
    if direction in ROOMS[current_room]['exits'].keys():
        new_room = ROOMS[current_room]['exits'][direction]
        if new_room == 'treasure_room':
            if 'rusty_key' not in game_state['player_inventory']:
                print('Дверь заперта, нужен ключ, чтобы пройти дальше.')
            else: 
                print('Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.') # noqa E501
                change_room(game_state, new_room)
        else: 
            change_room(game_state, new_room)
    else: 
        print('Нельзя пройти в этом направлении.')
    
def take_item(game_state, item_name):
    """
    Функция подбирания объекта игроком.
    """
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
    """
    Функуия использования объекта игроком, если объектом возможно воспользоваться.
    """
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