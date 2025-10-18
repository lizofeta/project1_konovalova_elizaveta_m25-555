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