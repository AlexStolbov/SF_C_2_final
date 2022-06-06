from typing import List

from cell import Cell
from ship import Ship
import random


class Board:
    """
    Игровое поле.
    Состоит из клеток Cell.
    """
    BOARD_SIZE = 6
    ONE_SHIP_COUNT = 4
    TWO_SHIP_COUNT = 2
    THREE_SHIP_COUNT = 1

    def __init__(self, player_name):
        self.player_name: str = player_name
        self.ships = [Ship(3) for _ in range(self.THREE_SHIP_COUNT)]
        self.ships += [Ship(2) for _ in range(self.TWO_SHIP_COUNT)]
        self.ships += [Ship(1) for _ in range(self.ONE_SHIP_COUNT)]
        complete = False
        # Попытки размещения кораблей. (обычно должно получиться !))
        for _ in range(6):
            self.board_field: List[List[Cell]] = self.get_clear_board()
            complete = self.populate_board()
            if complete:
                break
        if not complete:
            raise ValueError(f"Board for {self.player_name} is not ready")

    def get_clear_board(self):
        """
        :return: Пустое игровое поле
        """
        return [[Cell() for column in range(self.BOARD_SIZE)] for row in range(self.BOARD_SIZE)]

    def populate_board(self) -> bool:
        """
        Заполняет доску кораблями в начале игры.
        """
        for ship in self.ships:
            if not self.place_ship_on_board(ship):
                return False
        return True

    def print(self):
        """
        Печатает доску в консоль.
        """
        print('Player: ' + self.player_name)
        column_numbers = [str(column + 1) for column in range(self.BOARD_SIZE)]
        print(' ', self.row_to_print(column_numbers))
        row_number = 1
        for row in self.board_field:
            print(row_number, self.row_to_print(row))
            row_number += 1

    @staticmethod
    def row_to_print(row) -> str:
        """
        Формирует строку игровой доски для ввода на печать.
        :param row: Данные строки игровой доски.
        :return: Строка для печати.
        """
        return "| " + " | ".join(map(str, row)) + " |"

    def make_move(self, position) -> bool:
        """
        Проверяет корректность введенных данных.
        Добавляет ход на доску.
        :param position: Данные хода игрока.
        :return: Истина, если все успешно.
        """
        result = False
        cell = self.check_turn_result(position)
        if cell is not None:
            if not cell.is_attacked():
                cell.set_attacked()
                result = True
        return result

    def check_turn_result(self, turn_result) -> Cell:
        """
        Проверяет правильность координат, введенных пользователем.
        :param turn_result: координаты.
        :return: атакованная ячейка.
        """
        cell: Cell = None
        if turn_result.isdigit():
            if len(turn_result) == 2:
                column = int(turn_result[0]) - 1
                row = int(turn_result[1]) - 1
                if column < self.BOARD_SIZE and row < self.BOARD_SIZE:
                    cell = self.board_field[column][row]
        return cell

    def is_capitulate(self) -> bool:
        """
        Возвращает истину, если все корабли подбиты.
        """
        for row in self.board_field:
            for cell in row:
                if cell.has_ship() and not cell.is_attacked():
                    return False
        return True

    def get_cell_by_coordinates(self, row: int, column: int) -> Cell:
        """
        Возвращает ячейку по ее координатам.
        :param row: Номер строки.
        :param column: Номер колонки.
        :return: Найденная ячейка.
        """
        return self.board_field[row][column]

    def get_coordinates_by_cell(self, cell: Cell) -> (int, int):
        """
        Возвращает координаты ячейки.
        :param cell:
        :return:
        """
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                if cell == self.get_cell_by_coordinates(row=row, column=column):
                    return row, column

    def ship_is_near(self, cell: Cell) -> bool:
        """
        Определяет, находится ли рядом с ячейкой корабль.
        :param cell: Ячейка.
        :return: Истина - если рядом есть корабль.
        """
        row, column = self.get_coordinates_by_cell(cell)
        rows_check = []
        if row > 0:
            rows_check.append(row - 1)
        if row < self.BOARD_SIZE - 1:
            rows_check.append(row + 1)
        columns_check = []
        if column > 0:
            columns_check.append(column - 1)
        if column < self.BOARD_SIZE - 1:
            columns_check.append(column + 1)
        # Соседние по диагонали.
        checks = [(row_check, column_check) for row_check in rows_check for column_check in columns_check]
        # Соседние по строке
        checks += [(row_check, column_check) for row_check in [row] for column_check in columns_check]
        # Соседние по колонке
        checks += [(row_check, column_check) for row_check in rows_check for column_check in [column]]

        for coordinates in checks:
            if self.get_cell_by_coordinates(*coordinates).has_ship():
                return True
        return False

    def get_free_cells_for_ship(self) -> List[Cell]:
        """
        Возвращает клетки на поле, на которых возможно размещение корабля.
        :return: Список с клетками.
        """
        free_cells = []
        for row in self.board_field:
            for cell in row:
                if not cell.has_ship() and not self.ship_is_near(cell):
                    free_cells.append(cell)
        return free_cells

    def get_cells_not_attacked(self) -> List[Cell]:
        """
        Возвращает клетки на поле в которые еще не стреляли.
        :return: Список с клетками.
        """
        cells_not_attacked = []
        for row in self.board_field:
            for cell in row:
                if not cell.is_attacked():
                    cells_not_attacked.append(cell)
        return cells_not_attacked

    def place_ship_on_board(self, ship: Ship) -> bool:
        """
        Размещает корабль на поле.
        :param ship: Корабль кот. нужно разместить.
        :return: Истина -удалось, Ложь - не удалось.
        """
        free_cells: List[Cell] = self.get_free_cells_for_ship()
        random.shuffle(free_cells)
        place_for_ship = []
        for start_cell in free_cells:
            row, column = self.get_coordinates_by_cell(start_cell)
            # to right
            if column + ship.size <= self.BOARD_SIZE:
                place_for_ship = [self.board_field[row][column + i] for i in range(ship.size)]
                if all([_cell in free_cells for _cell in place_for_ship]):
                    break
            # to left
            # to up
            # to down

            place_for_ship = []
        complete = len(place_for_ship) > 0
        if complete:
            for cell in place_for_ship:
                cell.set_ship(ship)
        return complete
