""" File containing the player object. """

from walker import Walker


class Player(Walker):
    def __init__(self, name: str, position=None, health=5, have_treasure=False):
        """

        Parameters
        ----------
        name
        position
        health
        have_treasure
        """
        super().__init__(position)
        self.name = name
        self.health = health
        self.have_treasure = have_treasure
        self.visited = []

    def __str__(self):
        return self.name

    def move(self, new_position):
        print(self.position, new_position)
        self.position = new_position
        self.visited.append(new_position)
