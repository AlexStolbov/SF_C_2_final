import random
from board import Board


class Game:
    """
    Основной класс игры.
    Создает остальные классы игры.
    Управляет ходами игроков.
    """
    def __init__(self):
        self.next_turn = True  # переход хода следующему игроку
        self.boardHuman = Board("Human")  # доска человека
        self.boardAI = Board("AI")  # доска компьютера

    def start(self):
        """
        Интерфейс с пользователем.
        Общая логика игры.
        """
        print("Start game")
        for current_turn in self.get_next_turn():
            self.boardAI.print()
            self.boardHuman.print()
            player_name, opponent_board, turn_result = current_turn()
            if turn_result == "e":
                print("Exit...")
                break
            next_turn = opponent_board.make_move(turn_result)
            if next_turn:
                if opponent_board.is_capitulate():
                    print(f"{player_name} is win!!!")
                    opponent_board.print()
                    break
            else:
                print("!!! Try again !!!")

        print("Game over")

    def turn_player_ai(self):
        """
        Ход компьютера.
        :return: Результат хода.
        """
        player_name = self.boardAI.player_name
        free_cells = self.boardHuman.get_cells_not_attacked()
        random.shuffle(free_cells)
        data = self.boardHuman.get_coordinates_by_cell(free_cells[random.randint(0, len(free_cells) - 1)])
        data = str(data[0] + 1) + str(data[1] + 1)
        return player_name, self.boardHuman, data

    def turn_player_human(self):
        """
        Ход человека.
        :return: Результат хода.
        """
        player_name = self.boardHuman.player_name
        data = input(f'Player {player_name} (RowColumn): ("e"-exit): ')
        return player_name, self.boardAI, data

    def get_next_turn(self):
        """
        Генерирует последовательность ходов.
        next_turn - передать ход следующему игроку, иначе, повтор хода.
        :return: Результат очередного хода игрока.
        """
        order = [self.turn_player_ai, self.turn_player_human]
        current = int(random.randint(1, 10) <= 5)
        while True:
            yield order[current]
            if self.next_turn:
                current = 0 if current == 1 else 1


if __name__ == "__main__":
    game = Game()
    game.start()
