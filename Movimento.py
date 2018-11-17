import math

################################################################################MOVIMENTO

class Movimento:

    def __init__(self, vertices, norte):
        self.vertices = vertices
        self.norte = norte

    def centroid(self):
        x_coords = [x for x,y in self.vertices]
        y_coords = [y for x,y in self.vertices]
        centroid_x = sum(x_coords) / len(x_coords)
        centroid_y = sum(y_coords) / len(y_coords)
        return [centroid_x, centroid_y]

    def direcao(self):
        dx, dy = self.norte
        if (dx < len(self.vertices) and dy < len(self.vertices)):
            anguloF1 = sum( [x for x,y in [self.vertices[dx] , self.vertices[dy]] ]) / len([x for x,y in [self.vertices[dx] , self.vertices[dy]] ])
            anguloF2 = sum( [y for x,y in [self.vertices[dx] , self.vertices[dy]] ]) / len([y for x,y in [self.vertices[dx] , self.vertices[dy]] ])

            anguloL1 = sum( [x for x,y in [self.vertices[dx+1] , self.vertices[dy+1]] ]) / len([x for x,y in [self.vertices[dx+1] , self.vertices[dy+1]] ])
            anguloL2 = sum( [y for x,y in [self.vertices[dx+1] , self.vertices[dy+1]] ]) / len([y for x,y in [self.vertices[dx+1] , self.vertices[dy+1]] ])
            return [[anguloF1 , anguloF2] , [anguloL1 , anguloL2]]
        else:
            print("valores precisam ser menores que o total de pontos")#########

    def rotacao(self, angulo):
        angulo  = math.radians(angulo)
        cos_val = math.cos(angulo)
        sin_val = math.sin(angulo)
        cx, cy  = self.centroid()
        new_points = []
        for x_old, y_old in self.vertices:
            x_old -= cx
            y_old -= cy
            x_new = x_old * cos_val - y_old * sin_val
            y_new = x_old * sin_val + y_old * cos_val
            new_points.append([x_new + cx, y_new + cy])
        self.vertices = new_points

    def posicao(self, x, y):
        center = self.centroid()
        new_vertices = []
        for coord in self.vertices:
            new_vertices.append([(coord[0] - center[0]) + x,(coord[1] - center[1]) + y])
        self.vertices = new_vertices

    def mover(self, x, y):
        c_x, c_y = self.centroid()
        self.posicao(c_x + x, c_y + y)

    def orientacao(self):
        frente = []
        lado   = []
        dir    = self.direcao()
        centro = self.centroid()
        for d in range (0, len(dir)):
            frente_aux = dir[0][d] - centro[d]
            lado_aux   = dir[1][d] - centro[d]
            if(frente_aux != 0):
                frente_aux = frente_aux/10
            if(lado_aux != 0):
                lado_aux = lado_aux/10
            frente.append(frente_aux)
            lado.append(lado_aux)
        return {"Frente" : frente, "Lado" : lado}

################################################################################COL_HANDLER

class COL_HANDLER:

    def __init__(self, vertices):
        self.hitbox  = self.make_hitbox(vertices)

    def make_hitbox(self, vert):
        resultado = []
        for c in range(1, len(vert)):
            resultado.append([vert[c-1], vert[c]])
        resultado.append([vert[-1], vert[0]])
        return resultado

    def exists_intersection(self, line1, line2):

        def ccw(A,B,C):
            return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

        def intersect(line1, line2):
            A,B = line1
            C,D = line2
            bol1 = ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
            bol2 = (A == C or A == D) or (B == C or B == D)
            return bol1 or bol2

        resultado = []

        x1, y1 = line1[0]
        x2, y2 = line1[1]

        x3, y3 = line2[0]
        x4, y4 = line2[1]

        px_a, px_b = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)), ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        py_a, py_b = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)), ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

        if ([px_a, px_b] != [0, 0] and [px_b, py_b] != [0, 0]):
            if intersect(line1, line2):
                px, py = px_a/px_b , py_a/py_b
                resultado = [px, py]

        return resultado

    def hit_detection(self, sol_objects):
        resultado = []
        for p in sol_objects:
            for lin in self.hitbox:
                col = self.exists_intersection(lin, p)
                if col != []:
                    resultado.append(col)
        return resultado

    def intrusion(self, intruder, center):
        resultado = []
        for x_obj, y_obj in intruder:
            x_c, y_c = center
            if ((x_obj < x_c + 50 and x_obj > x_c - 50) and (y_obj < y_c + 50 and y_obj > y_c - 50)):
                resultado.append([x_obj, y_obj])
        if len(resultado) == len(intruder):
            return True
        else:
            return False
