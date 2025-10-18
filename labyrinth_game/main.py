#!/usr/bin/env python3

from labyrinth_game.player_actions import (show_inventory, get_input, move_player, take_item, use_item)
from labyrinth_game.utils import describe_current_room, solve_puzzle
from labyrinth_game.constants import ROOMS

game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0, # Количество шагов
        'score': 0 # Награда за решение загадок в комнатах
  }

def process_command(game_state, command):
    command = command.lower()
    parts = command.split(' ')
    action = parts[0]
    argument = ' '.join(parts[1:]) if len(parts) > 1 else None
    match action:
        case 'go':
            move_player(game_state, argument)
        case 'take':
            take_item(game_state, argument)
        case 'look':
            describe_current_room(game_state)
        case 'inventory':
            show_inventory(game_state)
        case 'quit':
            game_state['game_over'] = True 
            print('Вы вышли из игры.')
        case 'use':
            use_item(game_state, argument)
        case 'solve':
            solve_puzzle(game_state)

def main():
    print('Добро пожаловать в Лабиринт сокровищ!')
    describe_current_room(game_state)
    while not game_state['game_over']:
        command = get_input('Что будете делать? > ')
        process_command(game_state, command)

if __name__ == '__main__':
    main()