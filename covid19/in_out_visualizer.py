# Usage:
# python in_out_visualizer.py

# Next/Prev solution with left/right arrows or h/l (from hjkl)
# Quit with q

from my_globals import *
import my_lib

import curses
from curses import textpad, wrapper
import lipsum

error_log_filename = 'in_out_log.txt'

EXIT_KEYS = [ curses.KEY_EXIT , ord('q'), ord('Q') ]
NEXT_KEYS = [ curses.KEY_RIGHT, ord('l'), ord('L') ]
PREV_KEYS = [ curses.KEY_LEFT , ord('h'), ord('H') ]

def border(win, xy_offset=0, dim_offset=0):
    height,width = win.getmaxyx()

    uly = 1 + xy_offset
    ulx = 1 + xy_offset
    lry = height -1 - dim_offset
    lrx = width  -2 - dim_offset

    textpad.rectangle(win, uly, ulx, lry, lrx)


def init_wins():
    btw_gap = 1
    below_gap = 3
    # bottom win
    bh = 4
    bw = curses.COLS -2
    b_uly = curses.LINES - below_gap - bh
    b_ulx = 2
    # left win
    l_uly = 2
    l_ulx = 2
    lh = curses.LINES - l_uly - below_gap - bh
    lw = curses.COLS//2
    # right win
    r_uly = l_uly
    r_ulx = lw + btw_gap
    rw = lw - btw_gap - l_ulx
    rh = lh

    l_win = curses.newwin(lh, lw, l_uly, l_ulx)
    r_win = curses.newwin(rh, rw, r_uly, r_ulx)
    b_win = curses.newwin(bh, bw, b_uly, b_ulx)

    for w in [l_win, r_win, b_win]:
        w.keypad(True)
        w.clear()

    l_win.border(0)

    # left win text
    lt_begin_y = 2
    lt_begin_x = 2
    # right win text
    rt_begin_y = lt_begin_y
    rt_begin_x = lt_begin_x
    # right win text
    bt_begin_y = 2
    bt_begin_x = 2

    text = "Test text"
    l_win.addstr(lt_begin_y, lt_begin_x, text)
    r_win.addstr(rt_begin_y, rt_begin_x, text)
    b_win.addstr(bt_begin_y, bt_begin_x, text)
    border(b_win)

    return l_win, r_win, b_win



def main(stdscr):
    # Init
    curses.curs_set(False)
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)
    stdscr.clear()
    print("DEBUG", file=open(error_log_filename, 'w+')) #DEBUG

    try:
        l_win, r_win, b_win = init_wins()

        num = 0

        c = 'a' # uno a caso
        input_text = "Press a button"
        output = "Press a button"

        while not c in EXIT_KEYS:
            old_num = num
            if c in NEXT_KEYS:
                num +=1
            if c in PREV_KEYS and num > 0:
                num -=1

            try:
                old_input_text = input_text
                old_output = output

                input_text = my_lib.get_input_text(num,INPUT_MZN_DIR)
                print("input_text " + input_text, file=open(error_log_filename, 'a+'))
                mzn_output = my_lib.get_output(num,OUTPUT_MZN_DIR)
                lp_output  = my_lib.get_output(num,OUTPUT_LP_DIR)

            except Exception as inst:
                input_text = old_input_text
                output = old_output
                num = old_num
                print("Exception", file=open(error_log_filename, 'a+'))
                print(type(inst) , file=open(error_log_filename, 'a+'))
                print(inst.args  , file=open(error_log_filename, 'a+'))
                print(inst       , file=open(error_log_filename, 'a+'))

            print(input_text, file=open(error_log_filename, 'a+'))
            print(output, file=open(error_log_filename, 'a+'))

            l_win.clear()
            l_win.addstr(0,0, mzn_output)
            r_win.clear()
            r_win.addstr(0,0, lp_output)
            b_win.clear()
            b_win.addstr(0,0, "Input num={:02d}".format(num))
            inline_input_text = input_text
            inline_input_text = inline_input_text.replace("\n", " ")
            inline_input_text = inline_input_text.replace(";", " ")
            inline_input_text = inline_input_text.replace("M", "\tM")
            b_win.addstr(0,40, "{:s}".format(inline_input_text))

            l_win.refresh()
            r_win.refresh()
            b_win.refresh()
            print("mostro testo", file=open(error_log_filename, 'a+'))
            print("attendo", file=open(error_log_filename, 'a+'))
            c = b_win.getch()
            print("ho atteso", file=open(error_log_filename, 'a+'))

    finally:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()


inst = None
if __name__ == '__main__':
    try:
        wrapper(main)
    except Exception as inst:
        print("Exception", file=open(error_log_filename, 'a+'))
        print(type(inst) , file=open(error_log_filename, 'a+'))
        print(inst.args  , file=open(error_log_filename, 'a+'))
        print(inst       , file=open(error_log_filename, 'a+'))

        print("Guada il file di log oppure")
        print("Prova ad ingrandire il terminale...")
