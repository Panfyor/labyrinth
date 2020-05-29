""" File containing the game object. """

from random import choice, sample

from labyrinth import Labyrinth
from player import Player
from walker import Walker
from cfg import SPECIAL_CONTENT
from enemy import Enemy
import time

class Game:
    def __init__(self, labyrinth: Labyrinth, player: Player, enemies: list):
        """ Init game with parameters"""
        self.game_over = False
        self.player = player
        self.enemies = enemies
        self.labyrinth = labyrinth

    def display_rules(self):
        """ Display the labyrinth game's rules. """
        print("Find Treasure! Then find exit.")
        print("\nThis is a WASD game!")
        print("Use 'e' to activate Cell\n")

    def place_player(self):
        """ Place player if the cell is empty"""
        possible_positions = [pos for pos, cell in self.labyrinth.cells.items()
                              if cell.content not in SPECIAL_CONTENT]

        self.player.move(choice(possible_positions))

    def place_enemies(self):
        """ Place the enemies of the cells are empty"""
        possible_positions = [position for position, cell in self.labyrinth.cells.items()
                              if cell.content not in SPECIAL_CONTENT and position != self.player.position]

        positions = sample(possible_positions, k=len(self.enemies))

        for i, position in enumerate(positions):
            self.enemies[i].position = position

    def is_move_possible(self, walker: Walker, direction: str):
        """ Check if the move is possible"""

        if direction == 'up': x_move, y_move = 0, 1
        if direction == 'down': x_move, y_move = 0, -1
        if direction == 'left': x_move, y_move = -1, 0
        if direction == 'right': x_move, y_move = 1, 0
        x, y = walker.position

        if (x + x_move, y + y_move) in self.labyrinth.cells.keys():
            if self.labyrinth.junctions[(self.labyrinth.cells[x, y],
                                         self.labyrinth.cells[x + x_move, y + y_move])] != 'wall':
                return True, ''
            return False, 'WALL - are you blind?'
        return False, 'MONOLITH - are you blind?'

    def move_player(self, direction: str):
        """ Move the Player and notify what is inside the room"""
        if direction == 'up': x_move, y_move = 0, 1
        if direction == 'down': x_move, y_move = 0, -1
        if direction == 'left': x_move, y_move = -1, 0
        if direction == 'right': x_move, y_move = 1, 0

        x, y = self.player.position
        self.player.move((x + x_move, y + y_move))
        content = self.labyrinth.cells[self.player.position].content

        if content == 'empty': print(f'{self.player} is now in an empty room.')
        if content == 'wormhole': print(f'{self.player} is now in a room with wormhole.')
        if content == 'treasure': print(f'{self.player} is now in a room with treasure.')
        if content == 'map': print(f'{self.player} is now in a room with map.')
        if content == 'exit':
            if self.player.have_treasure:
                print(f'{self.player} is now in the exit room and can leave.')
            else:
                print(f'{self.player} is now in the exit room but you need the treasure to leave.')

    def player_hit(self, damage):
        """ Getting hit and notify the HP of the Player"""
        self.player.health -= damage
        if not self.player.have_treasure:
            print(f'{self.player} got hit, and now has {self.player.health} HP')
        else:
            self.labyrinth.cells[self.player.position].content = 'treasure'
            print(f'{self.player} got hit, dropped the treasure, and now has {self.player.health}HP')

    def activate_cell(self):
        """ Execute the cell action.
        If the cell contains map - open full map
        If the cell contains treasure - pick it up.
        """
        content = self.labyrinth.cells[self.player.position].content
        position = self.labyrinth.cells[self.player.position].position

        if content == 'map':
            print('You see an eye from HMM3 for whole map')
            for x in range(self.labyrinth.size):
                for y in range(self.labyrinth.size):
                    self.player.visited.append((x,y))

            self.labyrinth.cells[self.player.position].content = 'empty'
            self.labyrinth.display_labyrinth()

        if content == 'wormhole':
            for i in range(len(self.labyrinth.wormholes)):
                if self.labyrinth.wormholes[i] == self.labyrinth.cells[position]:
                    new_position = self.labyrinth.wormholes[(i + 1) % len(self.labyrinth.wormholes)].position
                    self.player.move(new_position)

                    print('Are you playing Portal?')
                    return True

        if content == 'treasure':
            self.player.have_treasure = True
            self.labyrinth.cells[self.player.position].content = 'empty'
            print('You now carry the treasure')
            return True

        if content == 'empty':
            print('Nothing happens')
            return False

    def move_enemy(self, enemy: Enemy):
        """ Randomly move enemy and refresh the display """
        steps = 0
        while steps < enemy.speed:
            # enemy can move several times
            direction = choice([(0, 1), (0, -1), (-1, 0), (1, 0)])

            x, y = enemy.position
            if (x + direction[0], y + direction[1]) in self.labyrinth.cells.keys():
                if self.labyrinth.junctions[(self.labyrinth.cells[x, y],
                                             self.labyrinth.cells[x + direction[0],
                                                                  y + direction[1]])] != 'wall':
                    enemy.position = x + direction[0], y + direction[1]
                    if (x, y) in self.player.visited:
                        time.sleep(0.1)
                        self.labyrinth.display_labyrinth()
                    steps += 1

            # hit player if the same position
            if self.player.position == enemy.position:
                # hit player
                self.player_hit(enemy.damage)
                while True:
                    direction = choice(['up', 'down', 'left', 'right'])
                    if self.is_move_possible(self.player, direction):
                        break
                self.move_player(direction)
        print(enemy.prin)

    def river_move_player(self, walker):
        """ Move player down the river """
        idx = 0
        # Count how far from the end of the river
        for cell in self.labyrinth.river:
            if cell == self.labyrinth.cells[walker.position]:
                break
            idx += 1

        # if it is in the end (or almost) of the river - so don`t move the player
        if idx == len(self.labyrinth.river) - 1:
            if isinstance(walker, Enemy):
                return 0
            print('The strong current shakes you but you stay in place.')
            return 0

        # move player down for 2 cells
        for i in range(2):
            if idx < len(self.labyrinth.river) - 1:
                if(isinstance(walker, Player)):
                    walker.move(self.labyrinth.river[(idx)].position)
                    walker.move(self.labyrinth.river[(idx + 1)].position)
                walker.position = self.labyrinth.river[(idx + 1)].position
                idx += 1
        if isinstance(walker, Enemy):
            return 0
        print('Woooo, So wet!')

    def is_game_over(self):
        """
        Check if the game is over: player is dead OR
        In the exit room with treasure

        Returns
        -------
        Reason : str
        """
        # Check if a player has escaped with the treasure and describes it if so.
        if self.player.position == self.labyrinth.exit_cell.position and self.player.have_treasure:
            reason = f'{self.player} escapes with the treasure and wins!'
            return True, reason
        if self.player.health <= 0:
            reason = 'You are Dead'
            return True, reason

        reason = ''
        return False, reason
