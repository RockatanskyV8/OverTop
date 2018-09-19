from tkinter import *
from Movimento import *

WIDTH = 400
HEIGHT = 400
CANVAS_MID_X = WIDTH/2
CANVAS_MID_Y = HEIGHT/2
SIDE = WIDTH/4

vertices = [
    [CANVAS_MID_X - SIDE/2, CANVAS_MID_Y - SIDE/2],
    [CANVAS_MID_X + SIDE/2, CANVAS_MID_Y - SIDE/2],
    [CANVAS_MID_X + SIDE/2, CANVAS_MID_Y + SIDE/2],
    [CANVAS_MID_X - SIDE/2, CANVAS_MID_Y + SIDE/2],
]

class interface:

################################################################################

    def __init__(self, vertices):
        self.root   = Tk()
        self.canvas = Canvas(self.root, bg="black", height=HEIGHT, width=WIDTH)

        self.controles = {'w': False,'a': False,'s': False,'d': False,'o': False,'k': False,}##

        self.direcao = [0 , 1]
        self.c = Movimento(vertices, self.direcao)

        self.draw_square(self.c.Vertices())

        self._animate()
        self._set_bindings()

        self.canvas.focus_set()
        self.canvas.pack()
        mainloop()

################################################################################

    def draw_square(self, points, color="blue", nome = "player"):
        self.canvas.create_polygon(points, fill=color, tag=nome)
        self.exibirCenter(points)
        self.exibirDirecoes()

    def exibirCenter(self, vertices):
        coords = vertices
        for c in coords:
            self.canvas.create_line(self.c.centroid() , c, fill="white", tag="player")

    def exibirDirecoes(self):
        coords = self.c.direcao()
        self.canvas.create_line(self.c.centroid() , coords[0], fill="yellow", tag="player")
        self.canvas.create_line(self.c.centroid() , coords[1], fill="red"   , tag="player")

    def rotacionar(self, angle = 1, nome="player", cor="blue"):
        self.c.rotacao(angle)
        self.canvas.delete(nome)
        self.draw_square(self.c.Vertices() , cor)

    def movFrente(self, vel = 1, nome="player", cor="blue"):
        self.c.mover( 0, (vel) )
        self.canvas.delete(nome)
        self.draw_square(self.c.Vertices() , cor)

    def movLado(self, vel = 1, nome="player", cor="blue"):
        self.c.mover( 1, (vel) )
        self.canvas.delete(nome)
        self.draw_square(self.c.Vertices() , cor)

    def _animate(self):
        if self.controles["w"]: self.movFrente(1)
        if self.controles["a"]: self.rotacionar(-1)
        if self.controles["s"]: self.movFrente(-1)
        if self.controles["d"]: self.rotacionar()
        if self.controles["o"]: self.movLado()
        if self.controles["k"]: self.movLado(-1)

        self.root.after(30, self._animate)

    def _pressed(self, event):
        self.controles[event.char] = True
    def _released(self, event):
        self.controles[event.char] = False

    def _set_bindings(self):
        for char in ['w','a','s','d','o','k']:
            self.root.bind("<KeyPress-%s>" % char, self._pressed)
            self.root.bind("<KeyRelease-%s>" % char, self._released)
            self.controles[char] = False

################################################################################

direcao = [0 , 1]
i = interface(vertices)
