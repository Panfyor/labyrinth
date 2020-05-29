""" File containing the main function and running the game. """

from labyrinth import Labyrinth
from player import Player
from game import Game
from enemy import Enemy
from cfg import KEY_MAP
import pygame


def play_game_labyrinth():
    """
    Main function to play the game
    """
    player = get_player()
    enemies = get_enemies()
    size = get_labyrinth_size()
    scale = get_scale()
    game = Game(Labyrinth(player, enemies, size, scale, len(enemies)), player, enemies)
    game.place_player()
    game.place_enemies()
    game.display_rules()
    game.labyrinth.display_labyrinth()


    while not game.game_over:

        player_moved = False
        while not player_moved:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key in KEY_MAP['quit']:
                        pygame.display.quit()

                    if event.key in KEY_MAP['right']:
                        direction = 'right'
                        do_move(game, player, direction)

                    if event.key in KEY_MAP['left']:
                        direction = 'left'
                        do_move(game, player, direction)

                    if event.key in KEY_MAP['down']:
                        direction = 'up'
                        do_move(game, player, direction)

                    if event.key in KEY_MAP['up']:
                        direction = 'down'
                        do_move(game, player, direction)

                    if event.key in KEY_MAP['skip']:
                        game.skip()
                        player_moved = True

                    player_moved = True
                    if event.key in KEY_MAP['activate']:
                        player_moved = game.activate_cell()
                        if player_moved:
                            game.labyrinth.display_labyrinth()

        if game.labyrinth.cells[game.player.position].content == 'river':
            game.river_move_player(player)
            game.labyrinth.display_labyrinth()

        for enemy in enemies:
            game.move_enemy(enemy)

        game.game_over, reason = game.is_game_over()

        if game.game_over:
            print(reason)
            break

    # game.labyrinth.display_labyrinth()
    # game.labyrinth.display_legend()


def get_player():
    """
    Get Player name in console
    Returns
    -------
    player : Player
    """
    name = input('Enter your name: ')
    player = Player(name)

    return player


def get_enemies():
    """
    Get enemies in console
    Returns
    -------
    enemies : list
    """
    level = ''
    enemies = []
    while level not in ['easy', 'medium', 'hard', 'youdead']:
        level = input('Enter difficulty: youdead, hard, medium, easy: ')
    if level == 'medium':
        enemies.extend([Enemy(enemy_type=1)])
    if level == 'hard':
        enemies.extend([Enemy(enemy_type=2), Enemy(enemy_type=1)])
    if level == 'youdead':
        enemies.extend([Enemy(enemy_type=3), Enemy(enemy_type=2), Enemy(enemy_type=1)])
    return enemies


def get_labyrinth_size():
    """
    Get size of the Labyrinth in console
    Returns
    -------
    size : int
    """
    size = 0
    while size not in [str(i) for i in range(4, 13)]:
        size = input('Enter the desired size of labyrinth (must be comprised between 4 and 12): ')

    return int(size)


def get_scale():
    """
    Get scale in console
    Scale must be (40-140)

    Returns
    -------
    scale : int
    """
    scale = 0
    while scale not in [str(i) for i in range(40, 141)]:
        scale = input('Please, enter the Scale (40 - 140): ')

    return int(scale)


def do_move(game, player, direction):
    """
    This function is to move player from one cell to another
    Parameters
    ----------
    game
    player
    direction

    Returns
    -------
    """
    move_possible, reason = game.is_move_possible(player, direction)
    if move_possible:
        game.move_player(direction)
        game.labyrinth.display_labyrinth()
    else:
        print(reason)


if __name__ == '__main__':

    new_game = True
    while new_game:

        play_game_labyrinth()
        answer = input('\nDo you want to play another game? [y/n] ').strip().lower()
        if answer not in ['y', 'yes']: new_game = False
