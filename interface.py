from tkinter import *
from Movimento import *

WIDTH = 400
HEIGHT = 400
CANVAS_MID_X = WIDTH/2
CANVAS_MID_Y = HEIGHT/2
SIDE = WIDTH/4

class interface:

################################################################################

    def __init__(self):
        self.root   = Tk()
        self.canvas = Canvas(self.root, bg="black", height=HEIGHT, width=WIDTH)

        self.controles = {'w': False,'a': False,'s': False,'d': False,'o': False,'k': False,}

        self.paredes = [ [[  0, 120],[200, 120]],[[200,  10],[200, 120]],
                         [[300, 250],[400, 350]],[[300, 250],[400, 150]],
                         [[  0, 350],[200, 350]],[[200, 350],[200, 400]] ]

        self.vertices = [ [CANVAS_MID_X - SIDE/2, CANVAS_MID_Y - SIDE/2],
                          [CANVAS_MID_X + SIDE/2, CANVAS_MID_Y - SIDE/2],
                          [CANVAS_MID_X + SIDE/2, CANVAS_MID_Y + SIDE/2],
                          [CANVAS_MID_X - SIDE/2, CANVAS_MID_Y + SIDE/2] ]

        self.vertiNpc = [ [CANVAS_MID_X - SIDE/6, CANVAS_MID_Y - SIDE/6],
                          [CANVAS_MID_X + SIDE/6, CANVAS_MID_Y - SIDE/6],
                          [CANVAS_MID_X + SIDE/6, CANVAS_MID_Y + SIDE/6],
                          [CANVAS_MID_X - SIDE/6, CANVAS_MID_Y + SIDE/6] ]

        self.direcao = [0 , 1]
        self.c   = Movimento(self.vertices, self.direcao)
        #self.c.posicao(300, 350)
        self.npc = Movimento(self.vertiNpc, self.direcao)

        self._animate()
        self._set_bindings()

        self.canvas.focus_set()
        self.canvas.pack()
        mainloop()

################################################################################ Player

    def player(self, c, color="blue", nome = "player"):
        char = c

        def exibirCenter():
            coords = char.vertices
            for c in coords:
                self.canvas.create_line(char.centroid() , c, fill="white", tag="player")

        def exibirDirecoes():
            coords = char.direcao()
            self.canvas.create_line(char.centroid() , coords[0], fill="yellow", tag="player")
            self.canvas.create_line(char.centroid() , coords[1], fill="red"   , tag="player")

        self.canvas.create_polygon(char.vertices, fill=color, tag=nome)

        exibirCenter()
        exibirDirecoes()

################################################################################ CENÁRIO

    def create_parede(self, parede, **kwargs):
        for p in parede:
            self.canvas.create_line(p, **kwargs)

################################################################################ COLISAO

    def create_circle(self, x, y, r, **kwargs):
        self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def hit(self, vect):
        if vect != []:
            for v in vect:
                x , y = v
                self.create_circle(x, y, 5, fill="yellow", width=1, tag='bola')

################################################################################ ANIMAÇÃO

    def _animate(self):

        def controles(c, keys):
            char = c
            x0 , y0 = char.orientacao()['Frente']
            x1 , y1 = char.orientacao()['Lado']
            if self.controles[ keys[0] ]: char.mover( x0 , y0 )
            if self.controles[ keys[1] ]: char.mover( x1 * (-1), y1 * (-1) )
            if self.controles[ keys[2] ]: char.mover( x0 * (-1), y0 * (-1) )
            if self.controles[ keys[3] ]: char.mover( x1 , y1 )
            if self.controles[ keys[4] ]: char.rotacao(-1)
            if self.controles[ keys[5] ]: char.rotacao(1)

        def mover_NPC():
            self.npc.mover(-2, 0)
            if(self.npc.centroid()[0] < 0):
                self.npc.posicao(400, self.npc.centroid()[1])

        self.canvas.delete("all")

        self.player(self.c)
        c_col = COL_HANDLER(self.c.vertices)
        controles(self.c, ['w','a','s','d','o','k'])
        npc_cor = "green"
        
        npc_col = COL_HANDLER(self.npc.vertices)
        mover_NPC()

        if (c_col.intrusion(self.npc.vertices, self.c.centroid())):
            npc_cor = "grey"

        self.player(self.npc, npc_cor)

        self.root.after(15, self._animate)

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
i = interface()
