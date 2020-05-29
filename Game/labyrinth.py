""" File containing the labyrinth object. """

from random import random, choice, sample

from cell import Cell
from cfg import *
from player import Player

import pygame


class Labyrinth:
    """ Make a labyrinth."""
    cells: dict

    def __init__(self, player: Player, enemies, size: int, scale: int, n_enemies: int):
        """ Initialize a labyrinth.
        
        Make a square labyrinth of the specified size containing one treasure and one exit.
        The parameter options must be a dictionary if specified.
        """
        self.player = player
        self.enemies = enemies

        # Display
        self.size = size
        self.scale = scale
        pygame.DOUBLEBU = True

        # Objects
        self.n_enemies = n_enemies
        self.wormholes = []
        self._init_cells()
        self.river = self._init_river()
        self.junctions = self._init_junctions(.9)
        self._init_objects()

        self._init_display()

    def _init_display(self):
        self.img_scale = int(self.scale * 0.95)
        self.distance = int(self.scale * 1.2)
        self.padding = int(self.scale * 1.8)
        self.shift = self.padding // 2 + self.scale // 2
        self.lab_size = self.padding + self.distance * (self.size - 1) + 2 * self.scale
        self.display_width = self.lab_size
        self.display_height = self.lab_size

        self.wall_shift = int((self.distance + self.scale) / 2)

        pygame.font.init()
        self.screen = pygame.display.set_mode((self.display_width, self.display_height))  # set application dimensions
        pygame.display.set_caption(TITLE)
        self.screen.fill(BLACK)  # set application background color

        # TEXT
        self.right_font = pygame.font.SysFont('Comic Sans MS', int(self.scale / 1.2))
        self.left_font = pygame.font.SysFont('Comic Sans MS', int(self.scale / 1.6))

        pygame.display.flip()

    def _init_cells(self):
        # Create all cells as empty.
        self.cells = {(x, y): Cell(position=(x, y)) for x in range(self.size)
                      for y in range(self.size)}

    def _init_river(self):
        river_size_min = ((self.size - 1) ** 2 // 4) - 1
        river_size_max = self.size ** 2 // 4
        river_sizes = list(range(river_size_min - 1, river_size_max + 1))
        possible_source_cells = [cell for cell in self.cells.values()
                                 if self._is_edge_cell(cell)]
        river = [choice(possible_source_cells)]
        while True:
            if len(river) in river_sizes:
                cell_can_be_edge = True
            else:
                cell_can_be_edge = False

            cell = self._choose_next_river_cell(river, cell_can_be_edge=cell_can_be_edge)

            if cell == None or len(river) > river_size_max:
                river = [river[0]]
                continue
            river.append(cell)
            if cell_can_be_edge and self._is_edge_cell(cell):
                break

        for c in river:
            self.cells[c.position].content = 'river'
        return river

    def _init_junctions(self, wall_p: float):

        junctions = {(c1, c2): 'nothing' for c1 in self.cells.values()
                     for c2 in self.cells.values()
                     if c1 != c2}
        junctions_to_del = []
        for c1, c2 in junctions.keys():
            x1, y1 = c1.position
            x2, y2 = c2.position

            if abs(x2 - x1) + abs(y2 - y1) == 1:
                if random() < wall_p and c1 not in self.river and c2 not in self.river:
                    junctions[c1, c2] = 'wall'
                    junctions[c2, c1] = junctions[c1, c2]
            else:
                junctions_to_del.append((c1, c2))

        for c1, c2 in junctions_to_del: del junctions[c1, c2]

        visited = []
        stack = []
        x = 0
        y = 0
        stack.append((x, y))  # place starting cell into stack
        visited.append((x, y))  # add starting cell to visited list
        while len(stack) > 0:  # loop until stack is empty
            cell = []  # define cell list

            if (x + 1, y) not in visited and (x + 1, y) in self.cells.keys():  # right cell available?
                cell.append("right")  # if yes add to cell list

            if (x - 1, y) not in visited and (x - 1, y) in self.cells.keys():  # left cell available?
                cell.append("left")

            if (x, y + 1) not in visited and (x, y + 1) in self.cells.keys():  # down cell available?
                cell.append("down")

            if (x, y - 1) not in visited and (x, y - 1) in self.cells.keys():  # up cell available?
                cell.append("up")

            if len(cell) > 0:  # check to see if cell list is empty
                cell_chosen = (choice(cell))  # select one of the cell randomly
                x_ = x
                y_ = y
                if cell_chosen == "right":  # if this cell has been chosen
                    x_ = x + 1  # make this cell the current cell
                elif cell_chosen == "left":
                    x_ = x - 1
                elif cell_chosen == "down":
                    y_ = y + 1
                elif cell_chosen == "up":
                    y_ = y - 1

                junctions[self.cells[(x, y)], self.cells[(x_, y_)]] = 'nothing'
                junctions[self.cells[(x_, y_)], self.cells[(x, y)]] = junctions[self.cells[(x, y)],
                                                                                self.cells[(x_, y_)]]
                x = x_
                y = y_
                visited.append((x, y))  # add to visited list
                stack.append((x, y))  # place current cell on to stack

            else:
                x, y = stack.pop()  # if no cells are available pop one from the stack

        return junctions

    def _init_objects(self):

        # Set the exit cell..
        exit_position = choice([position for position, cell in self.cells.items()
                                if self._is_edge_cell(cell) and
                                cell.content not in SPECIAL_CONTENT])
        self.cells[exit_position].content = 'exit'
        self.exit_cell = self.cells[exit_position]

        # Set the treasure in a cell.
        treasure_position = choice([position for position, cell in self.cells.items()
                                    if cell.content not in SPECIAL_CONTENT])
        self.cells[treasure_position].content = 'treasure'
        self.treasure_cell = self.cells[treasure_position]

        # Set the map cell.
        map_position = choice([position for position, cell in self.cells.items()
                               if cell.content not in SPECIAL_CONTENT])
        self.cells[map_position].content = 'map'

        # Set wormholes.
        n_wormholes = self.size // 2
        for i in range(n_wormholes):
            content = 'exit'
            while content in SPECIAL_CONTENT:
                position = choice(list(self.cells.keys()))
                content = self.cells[position].content
            self.cells[position].content = 'wormhole'
            self.wormholes.append(self.cells[position])

    def _choose_next_river_cell(self, river: list, cell_can_be_edge=True):

        c0 = river[-1]
        adjacent_c0 = []

        # Get a list of adjacent cells (with or without edge cells).
        if cell_can_be_edge:
            for cell in self.cells.values():
                if self._are_adjacent_cells(cell, c0): adjacent_c0.append(cell)
        else:
            for cell in self.cells.values():
                if self._are_adjacent_cells(cell, c0) and not self._is_edge_cell(cell):
                    adjacent_c0.append(cell)

        # Randomize the order of the list.
        adjacent_c0 = sample(adjacent_c0, k=len(adjacent_c0))

        # Ensure that the adjacent cells are not part of the river.
        for c1 in adjacent_c0:

            adjacent_c1 = []
            for cell in self.cells.values():
                if self._are_adjacent_cells(cell, c1): adjacent_c1.append(cell)

            are_river = [cell in river for cell in adjacent_c1
                         if cell != c0]
            if True in are_river:
                continue
            return c1
        return None

    def _get_exit_cell(self):

        for cell in self.cells.values():
            if cell.content == 'exit': return cell

    def _get_treasure_cell(self):

        for cell in self.cells.values():
            if cell.content == 'treasure': return cell

    def _is_edge_cell(self, cell: Cell):
        """ Return True if the cell is on the edge of the labyrinth, False otherwise. """
        x, y = cell.position
        if x in [0, self.size - 1] or y in [0, self.size - 1]: return True
        return False

    def _is_corner_cell(self, cell: Cell):
        """ Return True if the cell is is a corner of the labyrinth, False otherwise. """
        x, y = cell.position
        if x in [0, self.size - 1] and y in [0, self.size - 1]: return True
        return False

    def _are_adjacent_cells(self, c1: Cell, c2: Cell):
        """ Return True if c2 is above, under, left, or right of c1, False otherwise. """
        x1, y1 = c1.position
        x2, y2 = c2.position

        if abs(x2 - x1) + abs(y2 - y1) == 1:
            return True
        return False

    def display_labyrinth(self):
        """ Display the labyrinth in the terminal. """

        rect = [self.shift, self.shift, self.lab_size, self.lab_size]
        pygame.draw.rect(self.screen, BLACK, rect, 0)
        pygame.display.flip()

        for x in range(self.size):
            for y in range(self.size):
                # define the coordinates of the considered cell
                point_x = x * self.distance + self.shift
                point_y = y * self.distance + self.shift
                if (x, y) in self.player.visited:
                    # if player was there (the tuman of was is implemented there exactly)
                    rect = [point_x, point_y, self.scale, self.scale]
                    pygame.draw.rect(self.screen, WHITE, rect, 1) # draw CELL

                    icon_path = None

                    content = self.cells[x, y].content
                    # draw content
                    if content != 'empty':
                        if content == 'exit': icon_path = IMG_EXIT
                        if content == 'treasure': icon_path = IMG_TREASURE
                        if content == 'map': icon_path = IMG_MAP
                        if content == 'wormhole': icon_path = IMG_HOLE
                        if content == 'river':
                            if self.cells[x, y] == self.river[0]:
                                icon_path = IMG_RIVER_START
                            else:
                                icon_path = IMG_RIVER
                        icon = pygame.image.load(icon_path).convert_alpha()
                        icon = pygame.transform.scale(icon, (self.img_scale, self.img_scale))
                        self.screen.blit(icon, [point_x, point_y])

                    for enemy in self.enemies:
                        if enemy.position == (x, y):
                            if enemy.enemy_type == 1:
                                icon_path = IMG_BEAR
                            elif enemy.enemy_type == 2:
                                icon_path = IMG_HORN
                            elif enemy.enemy_type == 3:
                                icon_path = IMG_ALIEN

                            icon = pygame.image.load(icon_path).convert_alpha()
                            icon = pygame.transform.scale(icon, (self.img_scale, self.img_scale))
                            self.screen.blit(icon, [point_x, point_y])

                if self.player.position == (x, y):
                    icon_path = IMG_PLAYER
                    icon = pygame.image.load(icon_path).convert_alpha()
                    icon = pygame.transform.scale(icon, (self.img_scale, self.img_scale))
                    self.screen.blit(icon, [point_x, point_y])
        #

        start_points = []
        end_points = []

        for c1, c2 in self.junctions.keys():

            if self.junctions[c1, c2] == self.junctions[c2, c1] == 'wall':
                x1, y1 = c1.position
                x2, y2 = c2.position

                if (x1, y1) in self.player.visited or (x2, y2) in self.player.visited:

                    if x1 - x2 != 0:
                        start_point_x = max(x1, x2) * self.distance + int(self.shift * 0.92)
                        start_point_y = y1 * self.distance + self.shift
                        end_point_x = start_point_x
                        end_point_y = start_point_y + self.scale

                    if y1 - y2 != 0:
                        start_point_x = x1 * self.distance + self.shift
                        start_point_y = max(y1, y2) * self.distance + int(self.shift * 0.92)
                        end_point_x = start_point_x + self.scale
                        end_point_y = start_point_y

                    start_points.append((start_point_x, start_point_y))
                    end_points.append((end_point_x, end_point_y))

        for start_point, end_point in zip(start_points, end_points):
            pygame.draw.line(self.screen, RED, start_point, end_point, 5)

        start_points = []
        end_points = []

        for cell in self.cells.values():
            (x, y) = cell.position
            if (x, y) in self.player.visited:
                if x == 0:
                    start_point_x = int(self.shift * 0.92)
                    start_point_y = y * self.distance + self.shift
                    end_point_x = start_point_x
                    end_point_y = start_point_y + self.scale

                    start_points.append((start_point_x, start_point_y))
                    end_points.append((end_point_x, end_point_y))

                if x == self.size - 1:
                    start_point_x = (x + 1) * self.distance + int(self.shift * 0.92)
                    start_point_y = y * self.distance + self.shift
                    end_point_x = start_point_x
                    end_point_y = start_point_y + self.scale

                    start_points.append((start_point_x, start_point_y))
                    end_points.append((end_point_x, end_point_y))

                if y == 0:
                    start_point_x = x * self.distance + self.shift
                    start_point_y = int(self.shift * 0.92)
                    end_point_x = start_point_x + self.scale
                    end_point_y = start_point_y

                    start_points.append((start_point_x, start_point_y))
                    end_points.append((end_point_x, end_point_y))

                if y == self.size - 1:
                    start_point_x = x * self.distance + self.shift
                    start_point_y = (y + 1) * self.distance + int(self.shift * 0.92)
                    end_point_x = start_point_x + self.scale
                    end_point_y = start_point_y

                    start_points.append((start_point_x, start_point_y))
                    end_points.append((end_point_x, end_point_y))

        for start_point, end_point in zip(start_points, end_points):
            pygame.draw.line(self.screen, (0, 100, 148), start_point, end_point, 5)

        pygame.display.flip()

    # def display_log(self):
    #     """
    #     Log Text display
    #
    #     Returns
    #     -------
    #
    #     """
    #     cli_texts = ['Hey there I only want to talk withyou!', 'YOU HAVE DONE THAT DEAR!', '3']
    #     text_cli_texts = [self.left_font.render(f'{cli_text}', True, (25, 180, 200)) for cli_text in cli_texts]
    #     for i, text_cli_text in enumerate(text_cli_texts):
    #         self.screen.blit(text_cli_text,
    #                          (int(self.padding / 2), int(self.scale * i * 0.8) + self.lab_size * 0.9))  # draw text
    #     pygame.display.flip()
    #
    # def display_attributes(self):
    #     """
    #     Display attributes
    #
    #     Returns
    #     -------
    #
    #     """
    #     text_health_value = 0
    #     text_turn_value = 0
    #
    #     text_health = self.right_font.render(f'Health: {str(text_health_value)}', True, (25, 180, 200))
    #     text_turn = self.right_font.render(f'Turn: {str(text_turn_value)}', True, (25, 180, 200))
    #     self.screen.blit(text_health, (self.lab_size, self.padding))  # draw text
    #     self.screen.blit(text_turn, (self.lab_size, self.padding + self.scale))  # draw text
    #     pygame.display.flip()