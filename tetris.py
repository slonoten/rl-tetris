""" Simple tetris engine"""
import random
import copy


class GameOverError(Exception):
    "Game over exeption"
    pass


class Tetris:
    "Class for tetris engine"
    __figure_patterns = [[[1, 1],
                  [1, 1]],
                 [[1, 1, 0],
                  [0, 1, 1]],
                 [[0, 1, 1],
                  [1, 1, 0]],
                 [[1, 1, 1],
                  [1, 0, 0]],
                 [[1, 1, 1],
                  [0, 0, 1]],
                 [[1, 1, 1, 1]]]

    def __init__(self, columns_num=10, rows_num=20):
        self.__build_figures()
        self.__figure = None
        self.__columns_num = columns_num
        self.__rows_num = rows_num
        self.__well = [
            [0] * self.__columns_num for i in range(self.__rows_num)]
        self.__figure_row = -1
        self.__figure_column = 0
        self.__place_new_figure()
        self.__is_game_over = False
        self.__score = 0

    def step(self, command):
        """ Executes command.

        Args:
            command: integer representig a command
                0 - no command
                1 - move figure to left
                2 - move figure to right
                3 - rotate figure
                4 - drop figure

        Returns: Tuple of well as 2D array, game score and flag game over.
        """
        if self.__is_game_over:
            raise GameOverError()

        self.__apply_command(command)

        if self.__check_is_intersection(self.__figure, self.__figure_row + 1, self.__figure_column):
            if self.__figure_row < 0:
                # Game over
                self.__is_game_over = True
            else:
                self.__freeze_figure(self.__well)
                self.__remove_full_rows()
                self.__place_new_figure()
            return copy.deepcopy(self.__well), self.__score, self.__is_game_over
        else:
            self.__figure_row = self.__figure_row + 1

        return self._compose_well(), self.__score, False

    @staticmethod
    def rotate(figure):
        new_figure = [[0] * len(figure) for i in range(len(figure[0]))]
        width = len(figure[0])
        for i in range(len(figure)):
            for j in range(width):
                new_figure[j][i] = figure[i][width - j - 1]
        return new_figure

    def __build_figures(self):
        self.__figures = []
        for figure in self.__figure_patterns:
            figures = [figure]
            for i in range(3):
                figures.append(Tetris.rotate(figures[i]))
            self.__figures.append(figures)

    def __place_new_figure(self):
        "Set position for new figure"
        self.__figure_idx = random.randrange(len(self.__figures))
        self.__figure_angle = 0
        self.__figure = self.__figures[self.__figure_idx][self.__figure_angle]
        self.__figure_row = -1
        self.__figure_column = (self.__columns_num -
                                len(self.__figures[0])) // 2

    def __check_is_intersection(self, figure, row_num, column_num):
        # Check bottom
        if row_num + len(figure) > self.__rows_num:
            return True
        # Check sides
        if column_num < 0 or column_num + len(figure[0]) > self.__columns_num:
            return True
        # Check intersetion with well
        for i in range(len(figure)):
            for j in range(len(figure[i])):
                if self.__well[row_num + i][column_num + j] > 0 and figure[i][j] > 0:
                    return True
        return False

    def __freeze_figure(self, well, fill_with=1):
        for i in range(len(self.__figure)):
            for j in range(len(self.__figure[i])):
                if self.__figure[i][j] > 0:
                    well[self.__figure_row + i][self.__figure_column + j] = fill_with

    def __apply_command(self, command):
        if command in [1, 2]:
            # move
            shift = -1 if command == 1 else 1
            if not self.__check_is_intersection(self.__figure, self.__figure_row, self.__figure_column + shift):
                self.__figure_column = self.__figure_column + shift
        elif command == 3:
            # rotate
            new_angle = (self.__figure_angle + 1) & 3
            new_figure = self.__figures[self.__figure_idx][new_angle]
            if not self.__check_is_intersection(new_figure, self.__figure_row, self.__figure_column):
                self.__figure = new_figure
                self.__figure_angle = new_angle
        elif command == 4:
            while not self.__check_is_intersection(self.__figure, self.__figure_row + 1, self.__figure_column):
                self.__figure_row = self.__figure_row + 1


    def __remove_full_rows(self):
        rows_removed = 0
        figure_height = len(self.__figure)
        for i in range(figure_height):
            row_to_check = self.__figure_row + figure_height - i - 1
            if sum(self.__well[row_to_check]) == self.__columns_num:
                self.__well.pop(row_to_check)
                rows_removed = rows_removed + 1
        self.__score = self.__score + rows_removed * 100
        for i in range(rows_removed):
            self.__well.insert(0, [0] * self.__columns_num)

    def _compose_well(self):
        well = copy.deepcopy(self.__well)
        self.__freeze_figure(well, 2)
        return well


t = Tetris()
