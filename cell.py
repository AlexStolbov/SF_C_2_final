from ship import Ship


class Cell:
    """
    Клетка на игровом поле.
    Хранит наличие части корабля на ней
    и признак, что бы атакована.
    """

    def __init__(self):
        self.ship: Ship = None
        self._attacked: bool = False

    def set_ship(self, ship: Ship):
        """
        Размещает часть корабля на клетке
        :param ship:
        """
        self.ship = ship

    def has_ship(self):
        """
        Проверка расположения части корабля на клетке
        :return: Истина, если на клетке есть корабль
        """
        return self.ship is not None

    def set_attacked(self):
        """
        Отмечает клетку как атакованную.
        Если на клетке есть корабль, сообщает ему об атаке
        """
        self._attacked = True
        if self.has_ship():
            self.ship.attacked()

    def is_attacked(self) -> bool:
        """
        Проверка, что клетка была атакована
        :return: Истина, эта клетка была атакована
        """
        return self._attacked

    def __str__(self):
        if self.has_ship():
            if self._attacked:
                res = 'X'
            else:
                res = chr(0x25A0)  # ■
        else:
            if self._attacked:
                res = 'T'
            else:
                res = chr(0x25EF)  # ◯

        return res
