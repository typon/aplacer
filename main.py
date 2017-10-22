import pudb

from placer.easygl import easygl


def py_draw():
    for i in range(0, 1000, 100):
        if i > 1000:
            raise ValueError('i is too large!')
        easygl.py_fillrect(50 + i, 50 + i, 100 + i, 10 + i)


if __name__ == '__main__':
    easygl.py_init_world(0., 0., 1000., 1000.)
    easygl.py_init_graphics(b"Stratix 9001", 0)
    easygl.py_event_loop(None, None, None, py_draw)
