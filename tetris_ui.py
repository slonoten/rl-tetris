"Simple UI to test tetris"

import curses

from time import sleep
from tetris import Tetris


def print_well(stdscr, well):
    bricks = [' ', 'X', '#']
    well_rows_n = len(well)
    for i in range(well_rows_n):
        row = '|' + ''.join([bricks[x] for x in well[i]]) + '|'
        stdscr.addstr(i, 0, row)
    stdscr.addstr(well_rows_n, 0, '+' + '-' * len(well[0]) + '+')


def convert_to_command(ch):
    if ch < 0:
        return 0
    if ch == curses.KEY_LEFT:
        return 1
    if ch == curses.KEY_RIGHT:
        return 2
    if ch == curses.KEY_UP:
        return 3
    if ch == curses.KEY_DOWN:
        return 4
    if ch == 27:
        return -1
    return 0

def game(stdscr):
    stdscr.clear()
    stdscr.nodelay(True)
    tetris = Tetris()
    is_game_over = False
    while not is_game_over:
        command = convert_to_command(stdscr.getch())
        if command < 0:
            break
        well, score, is_game_over = tetris.step(command)
        print_well(stdscr, well)
        well_columns = len(well[0])
        stdscr.addstr(0, well_columns + 4, 'SCORE:')
        stdscr.addstr(1, well_columns + 4, str(score))
        sleep(0.5)
        stdscr.refresh()
    
curses.wrapper(game)
    
#stdscr.getkey()
