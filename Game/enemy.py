from walker import Walker


class Enemy(Walker):
    """
    This class describes enemy (3 types exactly)
    """

    def __init__(self, position=None, enemy_type=1):
        """

        Parameters
        ----------
        position
        enemy_type
        """
        super().__init__(position)
        self.enemy_type = enemy_type
        if self.enemy_type == 1:
            # Bear
            self.prin = 'Bear is roaring somewhere'
            self.damage = 1
            self.speed = 1

        elif self.enemy_type == 2:
            # Horn (something strange...)
            self.prin = 'Horn is near'
            self.damage = 1
            self.speed = 1

        elif self.enemy_type == 3:
            # Alien killer
            self.prin = 'IT IS THERE'
            self.damage = 2
            self.speed = 1
