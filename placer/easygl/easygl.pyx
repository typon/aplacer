from cython import float, char, int

cdef extern from "graphics.h":
    void init_world(float xl, float yt, float xr, float yb)
    void init_graphics(const char* window_name, int cindex_background)
    void event_loop(void (*act_on_mousebutton)(float x, float y),
                    void (*act_on_mousemove)(float x, float y),
                    void (*act_on_keypress)(char key_pressed),
                    void (*drawscreen)())
    void drawrect(float x1, float y1, float x2, float y2)
    void fillrect(float x1, float y1, float x2, float y2)
    void setcolor(int cindex)
    void flushinput()

# cdef object f

cdef void c_drawscreen():
    py_drawscreen()


cpdef void py_flushinput():
    py_flushinput()
cpdef void py_setcolor(int cindex):
    setcolor(cindex)
cpdef void py_fillrect(float x1, float y1, float x2, float y2):
    fillrect(x1, y1, x2, y2)

cpdef void py_init_world(float xl, float yt, float xr, float yb):
    init_world(xl,yt,xr,yb)
cpdef void py_init_graphics(window_name, cindex_background):
    init_graphics(window_name, cindex_background)

cpdef void py_event_loop(act_on_mousebutton, act_on_mousemove, act_on_keypress, drawscreen):

    global py_drawscreen
    py_drawscreen = drawscreen

    event_loop(NULL, NULL, NULL, c_drawscreen)

