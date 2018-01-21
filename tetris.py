""" Simple tetris engine"""
import random
import copy

class GameOverError(Exception):
    pass

class Tetris:
    "Class for tetris engine"
    __figures = [[[1,1],
                  [1,1]],
                  [[1, 1, 0],
                   [0, 1, 1]],
                  [[0, 1, 1],
                   [1, 1, 0]],
                  [[1, 1, 1],
                   [1, 0, 0]],
                  [[1, 1, 1],
                   [0, 0, 1]],
                  [[1, 1, 1, 1]]]

    def __init__(self, columns_num = 10, rows_num = 20):
        self.__columns_num = columns_num
        self.__rows_num = rows_num
        self.__well = [[0] * self.__columns_num for i in range(self.__rows_num)]
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

        if self.__check_is_intersection(self.__figure_row + 1, self.__figure_column):
            if self.__figure_row < 0:
                # Game over
                self.__is_game_over = True
            else:
                self.__freeze_figure(self.__well)
                self.__remove_full_rows()
                self.__place_new_figure()
            return copy.deepcopy(self.__well), self.__score, self.__is_game_over
        else:   
            self.__apply_command(command)
            self.__figure_row = self.__figure_row + 1
        
        return self._compose_well(), self.__score, False 

    def __place_new_figure(self):
        "Set position for new figure"
        self.__figure = copy.deepcopy(self.__figures[random.randrange(len(self.__figures))])
        self.__figure_row = -1
        self.__figure_column = (self.__columns_num - len(self.__figures[0])) // 2

    def __check_is_intersection(self, row_num, column_num):
        # Check bottom 
        if row_num + len(self.__figure) > self.__rows_num:
            return True
        # Check sides
        if column_num < 0 or column_num + len(self.__figure[0]) > self.__columns_num:
            return True
        # Check intersetion with well
        for i in range(len(self.__figure)):
            for j in range(len(self.__figure[i])):
                if self.__well[row_num + i][column_num + j] > 0 and self.__figure[i][j] > 0:
                    return True
        return False

    def __freeze_figure(self, well, coef = 1):
        for i in range(len(self.__figure)):
            for j in range(len(self.__figure[i])):
                well[self.__figure_row + i][self.__figure_column + j] = self.__figure[i][j] * coef

    def __apply_command(self, command):
        if command == 0:
            return
        if command in [1,2]:
            shift = -1 if command == 1 else 1
            if not self.__check_is_intersection(self.__figure_row, self.__figure_column + shift):
                self.__figure_column = self.__figure_column + shift

    def __remove_full_rows(self):
        pass

    def _compose_well(self):
        well = copy.deepcopy(self.__well)
        self.__freeze_figure(well, 2)
        return well

def print_well(well):
    for i in range(len(well)):
        row = '|' + ''.join([(' ' if x == 0 else 'X') for x in well[i]]) + '|'
        print(row)
    print('+' + '-' * len(well[0]) + '+')

t = Tetris()
while True:
    print('Command (0-3)?')
    r = t.step(int(input()))
    if r[2]:
        print('GAME OVER')
        break
    print_well(r[0])
    print('Score: ', r[1])

