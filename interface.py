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
        self.paredes = [ [[  0, 120],[200, 120]],
                         [[200,  10],[200, 120]],
                         [[300, 250],[400, 350]],
                         [[300, 250],[400, 150]],
                         [[  0, 350],[200, 350]],
                         [[200, 350],[200, 400]] ]

        self.draw_square(self.c.vertices)
        self.create_parede(self.paredes, fill='red', tag='parede')

        self._animate()
        self._set_bindings()

        self.canvas.focus_set()
        self.canvas.pack()
        mainloop()

################################################################################ DESENHAR

    def draw_square(self, points, color="blue", nome = "player"):
        self.canvas.create_polygon(points, fill=color, tag=nome)
        self.canvas.delete('bola')
        self.exibirCenter(points)
        self.exibirDirecoes()
        c = COL_HANDLER(points, self.paredes)
        self.hit(c.cenario_hit_detection())

    def exibirCenter(self, vertices):
        coords = vertices
        for c in coords:
            self.canvas.create_line(self.c.centroid() , c, fill="white", tag="player")

    def exibirDirecoes(self):
        coords = self.c.direcao()
        self.canvas.create_line(self.c.centroid() , coords[0], fill="yellow", tag="player")
        self.canvas.create_line(self.c.centroid() , coords[1], fill="red"   , tag="player")

    def create_parede(self, parede, **kwargs):
        for p in parede:
            self.canvas.create_line(p, **kwargs)

################################################################################ MOVIMENTACAO

    def rotacionar(self, angle = 1, nome="player"):
        self.c.rotacao(angle)
        self.canvas.delete(nome)
        self.draw_square(self.c.vertices)

    def mover(self, orientacao, vel = 1, nome = "player"):
        x , y = orientacao
        self.c.mover( x * vel, y * vel )
        self.canvas.delete(nome)
        self.draw_square(self.c.vertices)


################################################################################ COLISAO

    def create_circle(self, x, y, r, **kwargs):
        self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def hit(self, vect):
        if vect != []:
            for v in vect:
                x , y = v
                self.create_circle(x, y, 5, fill="yellow", width=1, tag='bola')

################################################################################ CONTROLES

    def _animate(self):
        if self.controles["w"]: self.mover(self.c.orientacao(0))
        if self.controles["a"]: self.rotacionar(-1)
        if self.controles["s"]: self.mover(self.c.orientacao(0), -1)
        if self.controles["d"]: self.rotacionar()
        if self.controles["o"]: self.mover(self.c.orientacao(1))
        if self.controles["k"]: self.mover(self.c.orientacao(1), -1)

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
