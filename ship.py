class Ship:
    """
    Корабль.
    Имеет размер и остаток 'жизни'.
    """

    def __init__(self, size):
        self.size = size
        self.health = size

    def attacked(self):
        if self.health > 0:
            self.health -= 1
        else:
            raise ValueError("Корабль уже был уничтожен")
