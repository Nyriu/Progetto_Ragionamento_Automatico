import curses
from curses import textpad, wrapper
import lipsum

def big_rectangle(win, xy_offset=0, dim_offset=0):
    height,width = win.getmaxyx()

    uly = 1 + xy_offset
    ulx = 1 + xy_offset
    lry = height -1 - dim_offset
    lrx = width  -2 - dim_offset

    textpad.rectangle(win, uly, ulx, lry, lrx)


def main(stdscr):
    # Init
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)
    stdscr.clear()

    try:
        # left win
        l_uly = 2
        l_ulx = 2
        h = curses.LINES - l_uly
        w = curses.COLS // 2 -2
        # right win
        r_uly = l_uly
        r_ulx = l_ulx + w +2

        left_half  = curses.newwin(h, w, l_uly, l_ulx)
        right_half = curses.newwin(h, w-2, r_uly, r_ulx)

        # left win text
        lt_begin_y = 1
        lt_begin_x = 1
        # right win text
        rt_begin_y = lt_begin_y
        rt_begin_x = lt_begin_x

        text = lipsum.generate_paragraphs(1)
        left_half.addstr(lt_begin_y, lt_begin_x, text)
        right_half.addstr(rt_begin_y, rt_begin_x, text)



        left_half.refresh()
        right_half.refresh()

        left_half.getkey()

    finally:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()

wrapper(main)
