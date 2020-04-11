#### TODO
#### Esegue il modello MiniZinc su tutti gli input
#### Per ciascuno mostra input e infomrazioni sulla soluzione trovata
#### con le frecce sx dx si passa all'input precedente o successivo
#### TODO # con le frecce su giu' si passa alla soluzione precedente o successiva
###
#### Usage:
#### python in_out_visualizer.py
###
####import sys
###import my_lib
###
###def get_args():
###    args = sys.argv
###    if len(args) < 2:
###        print("Put pone arguments!! For example")
###        print("python run.py 10")
###        exit(1)
###
###    try:
###        input_num = int(args[1])
###    except:
###        print("ERROR! Input num is not ad int!")
###        exit(2)
###    return input_num
###
###
###
###
#####################################################
#### Main
#####################################################
###def main():
###    input_num = get_args()
###    #my_lib.run_minizinc_model(input_num, show_output=True)
###    my_lib.run_minizinc_model(input_num)
###
###
###if __name__ == "__main__":
###    main()
###
import my_lib

import curses
from curses import textpad, wrapper
import lipsum


#EXIT_KEYS = [ curses.KEY_EXIT , 'q', 'Q' ]
#NEXT_KEYS = [ curses.KEY_RIGHT, 'l', 'L' ]
#PREV_KEYS = [ curses.KEY_LEFT , 'h', 'H' ]

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

    # DEBUG
    print("_h, _w, __uly, __ulx", file=open('tmp.txt', 'w+'))
    print(lh, lw, l_uly, l_ulx, file=open('tmp.txt', 'a+'))
    print(rh, rw, r_uly, r_ulx, file=open('tmp.txt', 'a+'))
    print(bh, bw, b_uly, b_ulx, file=open('tmp.txt', 'a+'))
    # END # DEBUG

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

    #text = lipsum.generate_paragraphs(1)
    text = "Test text"
    l_win.addstr(lt_begin_y, lt_begin_x, text)
    r_win.addstr(rt_begin_y, rt_begin_x, text)
    b_win.addstr(bt_begin_y, bt_begin_x, text)
    #border(l_win)
    #border(r_win)
    border(b_win)

    return l_win, r_win, b_win


def main(stdscr):
    # Init
    curses.curs_set(False)
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)
    stdscr.clear()

    try:
        l_win, r_win, b_win = init_wins()
        num = 0

        #c = b_win.getkey()
        #c = b_win.getch()
        #c = stdscr.getch()
        c = 'a' # uno a caso
        input_text = ""
        output = ""

        while not c in EXIT_KEYS:
            old_num = num
            if c in NEXT_KEYS:
                num +=1
            elif c in PREV_KEYS and num > 0:
                num -=1
            else:
                pass

            try:
                old_input_text = input_text
                old_output = output

                input_text = my_lib.get_input_text(num)
                output = my_lib.get_output(num)
            except:
                input_text = old_input_text
                output = old_output
                num = old_num

            l_win.clear()
            l_win.addstr(0,0, output)
            r_win.clear()
            r_win.addstr(0,0, input_text)
            b_win.clear()
            b_win.addstr(0,0, "Input num={:02d}".format(num))

            #show_input(l_win, num)
            #show_result(r_win, num)

            l_win.refresh()
            r_win.refresh()
            b_win.refresh()
            #c = b_win.getkey()
            #c = b_win.getch()
            c = stdscr.getch()

    #except:
    #    curses.nocbreak()
    #    stdscr.keypad(False)
    #    curses.echo()
    #    curses.endwin()
    #    print("Unspecified Error")

    finally:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()



if __name__ == '__main__':
    wrapper(main)
